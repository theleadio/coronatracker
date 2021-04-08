from ScrapeRss.NewsContent import NewsContent

from ScrapeRss.globals import URL_BLACKLIST_KEYWORDS, CORONA_KEYWORDS
from ScrapeRss.globals import SEED_QUEUE, EXTRACT_QUEUE

from ScrapeRss.helpers import is_valid_url, is_article_uploaded_today
from ScrapeRss.helpers import get_title_from_for_html, get_description_from_for_html
from ScrapeRss.helpers import corona_keyword_exists_in_string
from ScrapeRss.helpers import convert_date_to_datetime_object


from bs4 import BeautifulSoup
import logging
import re


class NewsParser:
    __instance__ = None;
    def __init__(
        self,
        locale="",
        root_url="",
        schema={},
        soup_page="",
        is_xml=True,
        news_list=[],
        custom_blacklist=[],
    ):
        self.locale = locale
        self.root_url = root_url
        self.schema = schema
        self.soup_page = soup_page
        self.is_xml = is_xml
        self.news_list = news_list
        self.custom_blacklist = set(custom_blacklist)

        self.parse_schema()

        if NewsParser.__instance__ is None:
            NewsParser.__instance__ = self
        else:
            raise Exception("Only one instance of NewsParser allowed")

    def parse_schema(self):
        if "not_xml" in self.schema and self.schema["not_xml"] is True:
            self.is_xml = False
        if "custom_blacklist" in self.schema:
            self.custom_blacklist = self.custom_blacklist.union(
                set(self.schema["custom_blacklist"])
            )
            
    def get_instance():
        if not NewsParser.__instance__:
            NewsParser();
        return NewsParser.__insance__;

    def validate_required_values(self):
        error = False
        if not self.root_url.strip():
            logging.error("Empty root url")
            error = True
        if not self.locale.strip():
            logging.error("Empty locale")
            error = True

        if error:
            raise Exception(
                "NewsParser object missing required attributes: root_url, locale"
            )

    def parse_seed_page_content(self, page_content):
        news_list = []
        # Attempt to crawl non xml sites
        if not self.is_xml:
            self.soup_page = BeautifulSoup(page_content, "html.parser")
            self.parse_soup_page_for_html()

        else:
            # xml sites, extract each nodes. Node format example:
            # <url>
            #     <loc>
            #         https://www.aljazeera.com/news/2020/02/infected-coronavirus-200210205212755.html
            #     </loc>
            #     <lastmod>2020-02-15</lastmod>
            # </url>
            self.soup_page = BeautifulSoup(page_content, "xml")
            self.parse_soup_page_for_xml()

    def parse_soup_page_for_html(self):
        for a_tag_node in self.soup_page.findAll("a"):
            include_url = True

            url = a_tag_node.text.strip()
            title = get_title_from_for_html(a_tag_node)
            description = get_description_from_for_html(a_tag_node)

            if not corona_keyword_exists_in_string(url):
                include_url = False

                if (title and not corona_keyword_exists_in_string(title)) and (
                    description and not corona_keyword_exists_in_string(description)
                ):
                    include_url = False
                else:
                    include_url = True

            if not include_url:
                continue

            news_object = NewsContent(seed_source=self)
            try:
                news_object.news_url = a_tag_node["href"]
            except Exception as e:
                continue

            if not is_valid_url(news_object.news_url, self.custom_blacklist):
                continue

            self.news_list.append(news_object)

    def parse_soup_page_for_xml(self):
        # common nodes for sitemaps
        # hardcode? or set in schema?
        url_nodes = self.soup_page.findAll("item")
        if not url_nodes:
            url_nodes = self.soup_page.findAll("url")
        if not url_nodes:
            url_nodes = self.soup_page.findAll("sitemap")

        for node in url_nodes:
            insert_article = True
            news_object = NewsContent(seed_source=self)
            published_at_dt_object = None
            # use date_xml in schema to skip old articles and get published_at
            if "date_xml" in self.schema:
                date_tag_name = self.schema["date_xml"][0]
                date_value_dt_format = self.schema["date_xml"][1]

                try:
                    date_string_value = node.find(date_tag_name).text
                    published_at_dt_object = convert_date_to_datetime_object(
                        date_string_value
                    )
                    insert_article = is_article_uploaded_today(published_at_dt_object)
                except Exception as e:
                    # Potentially sub-sitemap doesn't have datetime even though root sitemap does
                    # "Fail to convert extract date_tag_name. Most likely irregular xml format. date_tag_name: {}, Node: {} Skipping..."
                    # "Fail to convert publishedAt datetime format. Most likely irregular xml format. Value: {}, Format: {} Skipping..."
                    # logging.error("Fail to convert extract date_tag_name or publishedAt datetime format. Skip early catching. URL: {}".format(self.root_url))
                    insert_article = True

            # if datetime exists, use it for early catching
            #   skip if article is not uploaded today
            # else proceed to try other methods
            if not insert_article:
                continue

            # check for xml to feed back into SEED_QUEUE
            news_url = node.find(self.schema["url"]).text.strip()
            check_url = news_url[: news_url.index("?")] if "?" in news_url else news_url
            if check_url.endswith(".xml"):
                seed_object = NewsParser(
                    locale=self.locale, root_url=news_url, schema=self.schema,
                )
                SEED_QUEUE.put(seed_object)
                continue

            # check for empty, non https ,blacklist
            if not is_valid_url(news_url, self.custom_blacklist):
                logging.debug(
                    "url: {}, check: is_valid_url, valid: False".format(news_url)
                )
                continue

            node_title = ""
            node_description = ""
            if "title" not in self.schema and "description" not in self.schema:
                # sitemap doesn't have title or description at all
                # so we have to go through each URL to check if CORONA_KEYWORDS exists
                pass
            elif "keywords" in self.schema:
                keywords_node = node.find(self.schema["keywords"])
                if keywords_node:
                    keywords = keywords_node.text
                    if not corona_keyword_exists_in_string(keywords.lower()):
                        continue
            else:
                # sitemap that contains either title or description
                # early detection if URL contains CORONA_KEYWORDS or not
                if "title" in self.schema:
                    title_node = node.find(self.schema["title"])
                    node_title = title_node.text if title_node else node_title

                if "description" in self.schema:
                    node_description = node.find(self.schema["description"]).text

                # check if any of the CORONA_KEYWORDS occur in title or description
                corona_keywords_exist = corona_keyword_exists_in_string(
                    node_title.lower()
                ) or corona_keyword_exists_in_string(node_description.lower())
                if not corona_keywords_exist:
                    continue

            node_author = ""
            if "author" in self.schema:
                node_author = node.find(self.schema["author"]).text

            news_object.author = node_author
            news_object.news_url = news_url
            news_object.title = node_title
            news_object.description = node_description
            news_object.published_at = published_at_dt_object
            self.news_list.append(news_object)

    def add_news_to_extraction_queue(self):
        for news_object in self.news_list:
            EXTRACT_QUEUE.put(news_object)
