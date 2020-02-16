#!/usr/bin/env python3
#
# -*- coding: utf-8 -*-
#
# Last update: 2/2/2020
# Authors:
#   - dipto.pratyaksa@carltondigital.com.au
#   - samueljklee@gmail.com
#
# REF:
# https://santhoshveer.com/rss-feed-reader-using-python/
# https://medium.com/@ankurjain_79625/how-did-i-scrape-news-article-using-python-6eff936b3c8c
# https://medium.com/@randerson112358/scrape-summarize-news-articles-using-python-51a48af1b4e2
#
# TO DO:
# Store the relevant RSS feed into shared repo, like Google sheet
# Algo to extract the casualty stats from linked news article
#
# USAGE:
# python scrape_rss.py -c -d
#   -d : debug mode, write to output.jsonl, else, write to db. default=True
#   -c : clear cache, default=False
#   -a : get all, skip cache. api uses this to crawl everything
#        - update database doesn't use this, to prevent duplicated entries
#
# Example:
#   - write to db with log messages, doesn't update ./data/<lang>/output.jsonl
#       - python scrape_rss.py       # writes to test table
#       - python scrape_rss.py -p    # writes to production table
#   - debug only
#       d flag so it doesn't write to db (prints output and write to output.jsonl)
#       a flag will skip read and write to cache
#       - python scrape_rss.py -d -a
#
# NOTE:
#   - Using black to format the code. Feel free to use it (https://black.readthedocs.io/en/stable/)
#

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from dateutil.parser import parse
import re

import nltk
from newspaper import Article
import threading
import queue

import argparse
import json
import os

import db_connector
import logging


"""
Crawling:
https://www.ettoday.net/news-sitemap.xml
https://www.taiwannews.com.tw/ch/sitemap.xml
http://www.taipeitimes.com/sitemap.xml
https://www.taiwannews.com.tw/en/sitemap.xml
https://www.shine.cn/sitemap-news.xml
https://www.scmp.com/rss/318208/feed
https://www.theage.com.au/rss/feed.xml
https://www.news.com.au/content-feeds/latest-news-world/
https://www.news.com.au/content-feeds/latest-news-national/
http://www.dailytelegraph.com.au/news/breaking-news/rss
http://www.dailytelegraph.com.au/news/national/rss
http://www.dailytelegraph.com.au/newslocal/rss
http://www.dailytelegraph.com.au/news/world/rss
https://www.sbs.com.au/news/topic/latest/feed
https://www.channelnewsasia.com/googlenews/cna_news_sitemap.xml

Don't crawl:
https://www.theage.com.au/rss/world.xml
http://www.heraldsun.com.au/news/breaking-news/rss
http://www.heraldsun.com.au/rss

"""

# nltk updates
nltk.download("punkt")

# CONSTANT VALUES
# "Sat, 25 Jan 2020 01:52:22 +0000"
DATE_RFC_2822_REGEX_RULE = r"[\d]{1,2} [ADFJMNOS]\w* [\d]{4} \b(?:[01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9] [\+]{1}[0-9]{4}\b"
DATE_RFC_2822_DATE_FORMAT = "%d %b %Y %H:%M:%S %z"
# ISO 8601 | 2020-01-31T22:10:38+0800 | 2020-02-05T08:13:54.000Z | 2017-04-17T22:23:24+00:00
DATE_ISO_8601_REGEX_RULE = (
    r"\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:?\d{0,2}[\+\.]\d{2,4}\:?[0-9]{0,2}Z?"
)
ISO_8601_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
ISO_8601_DATE_WITHOUT_SEC_FORMAT = "%Y-%m-%dT%H:%M%z"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
YEAR_MONTH_DAY_FORMAT = "%Y-%m-%d"

URL_BLACKLIST_KEYWORDS = set(["/archives/", "/videos/", "/images/", "/author/"])
CORONA_KEYWORDS = set(
    [
        "covid-19",
        "corona virus",
        "coronavirus",
        "武漢肺炎",
        "冠状病毒",
        "virus corona",
        "viêm phổi",  # pneumonia
        "コロナウィルス",  # coronavirus
        "新型肺炎",  # new pneumonia
        "新型コロナ",  # new corona
    ]
)
SPECIAL_LANG = set(["zh_TW", "zh_CN"])

# some sitemap contains different attributes
NEWS_URLs = {
    "en_AU": [
        (
            "https://www.theage.com.au/rss/feed.xml",
            {
                "title": "title",
                "description": "description",
                "url": "link",
                "date_xml": ("pubDate", None),
            },
        ),
        # Doesn't work anymore, couldn't access rss feed
        # (
        #     "https://www.theage.com.au/rss/world.xml",
        #     {"title": "title", "description": "description", "url": "link",},
        # ),
        # Remove heraldsun rss to prevent scraping the same content as other rss
        # > as it's a smaller newspaper that is likely syndicating news from bigger news
        #         (
        #             "http://www.heraldsun.com.au/news/breaking-news/rss",
        #             {"title": "title", "description": "description", "url": "link",},
        #         ),
        #         (
        #             "http://www.heraldsun.com.au/rss",
        #             {"title": "title", "description": "description", "url": "link",},
        #         ),
        (
            "https://www.news.com.au/content-feeds/latest-news-world/",
            {
                "title": "title",
                "description": "description",
                "url": "link",
                "date_xml": ("pubDate", None),
            },
        ),
        (
            "https://www.news.com.au/content-feeds/latest-news-national/",
            {
                "title": "title",
                "description": "description",
                "url": "link",
                "date_xml": ("pubDate", None),
            },
        ),
        (
            "http://www.dailytelegraph.com.au/news/breaking-news/rss",
            {"title": "title", "description": "description", "url": "link",},
        ),
        (
            "http://www.dailytelegraph.com.au/news/national/rss",
            {"title": "title", "description": "description", "url": "link",},
        ),
        (
            "http://www.dailytelegraph.com.au/newslocal/rss",
            {"title": "title", "description": "description", "url": "link",},
        ),
        (
            "http://www.dailytelegraph.com.au/news/world/rss",
            {"title": "title", "description": "description", "url": "link",},
        ),
        (
            "https://www.sbs.com.au/news/topic/latest/feed",
            {
                "title": "title",
                "description": "description",
                "url": "link",
                "date_xml": ("pubDate", None),
            },
        ),
    ],
    "en_CN": [
        (
            "https://www.shine.cn/sitemap-news.xml",
            {
                "title": "news:title",
                "url": "loc",
                "date_xml": ("news:publication_date", ISO_8601_DATE_FORMAT),
            },
        ),
    ],
    "en_TW": [
        (
            "http://www.taipeitimes.com/sitemap.xml",
            {"url": "loc", "date_xml": ("lastmod", ISO_8601_DATE_FORMAT),},
        ),
        (
            "https://www.taiwannews.com.tw/en/sitemap.xml",
            {
                "title": "news:title",
                "url": "loc",
                "date_xml": ("news:publication_date", YEAR_MONTH_DAY_FORMAT),
            },
        ),
    ],
    "en_SG": [
        (
            "https://www.channelnewsasia.com/googlenews/cna_news_sitemap.xml",
            {
                "title": "title",
                "description": "news:keywords",
                "url": "loc",
                "date_xml": ("news:publication_date", ISO_8601_DATE_FORMAT),
            },
        ),
    ],
    "en_HK": [
        (
            "https://www.scmp.com/rss/318208/feed",
            {
                "title": "title",
                "description": "description",
                "url": "link",
                "date_xml": ("pubDate", None),
            },
        ),
    ],
    "en_QA": [
        (
            "https://www.aljazeera.com/xml/sslsitemaps/sitemap2020_1.xml",
            {"url": "loc", "date_xml": ("lastmod", YEAR_MONTH_DAY_FORMAT),},
        ),
    ],
    "id_ID": [("https://news.kompas.com/web/sitemap.xml", {"url": "loc",},)],
    "ja_JP": [
        (
            "https://toyokeizai.net/sitemap.xml",
            {"url": "loc", "date_xml": ("lastmod", ISO_8601_DATE_FORMAT),},
        ),
        (
            "http://www.news24.jp/sitemap_society.xml",
            {
                "url": "loc",
                # don't include title even though xml has it
                # title doesn't have enough info, crawl each instead
                # "title": "news:title",
                "date_xml": ("news:publication_date", ISO_8601_DATE_WITHOUT_SEC_FORMAT),
            },
        ),
        (
            "http://www.news24.jp/sitemap_economy.xml",
            {
                "url": "loc",
                # don't include title even though xml has it
                # title doesn't have enough info, crawl each instead
                # "title": "news:title",
                "date_xml": ("news:publication_date", ISO_8601_DATE_WITHOUT_SEC_FORMAT),
            },
        ),
        (
            "http://www.news24.jp/sitemap_international.xml",
            {
                "url": "loc",
                # don't include title even though xml has it
                # title doesn't have enough info, crawl each instead
                # "title": "news:title",
                "date_xml": ("news:publication_date", ISO_8601_DATE_WITHOUT_SEC_FORMAT),
            },
        ),
    ],
    "vi_VN": [
        ("https://www.tienphong.vn/event/virus-covid19-2302.tpo", {"not_xml": True}),
        (
            "https://baomoi.com/sitemaps/sitemap-news.xml",
            {
                "url": "loc",
                "title": "news:title",
                "keywords": "news:keywords",
                "date_xml": ("news:publication_date", ISO_8601_DATE_WITHOUT_SEC_FORMAT),
            },
        ),
        (
            "https://vnexpress.net/google-news-sitemap.xml",
            {
                "url": "loc",
                "title": "news:title",
                "keywords": "news:keywords",
                "date_xml": ("news:publication_date", ISO_8601_DATE_FORMAT),
            },
        ),
        (
            "https://vietnamnews.vn/sitemap.xml",
            {"url": "loc", "date_xml": ("lastmod", YEAR_MONTH_DAY_FORMAT),},
        ),
    ],
    "zh_TW": [
        (
            "https://news.cts.com.tw/sitemap.xml",
            {"url": "loc", "date_xml": ("lastmod", YEAR_MONTH_DAY_FORMAT),},
        ),
        ("https://news.pts.org.tw/dailynews.php", {"not_xml": True},),
        (
            "https://www.taiwannews.com.tw/ch/sitemap.xml",
            {
                "title": "news:title",
                "url": "loc",
                "date_xml": ("news:publication_date", YEAR_MONTH_DAY_FORMAT),
            },
        ),
        (
            "https://www.ettoday.net/news-sitemap.xml",
            {
                "title": "news:title",
                "url": "loc",
                "date_xml": ("news:publication_date", ISO_8601_DATE_WITHOUT_SEC_FORMAT),
            },
        ),
    ],
}

global READ_ALL_SKIP_CACHE
global WRITE_TO_PROD_TABLE
global WRITE_TO_DB_MODE

### LOGGER CONFIG
if not os.path.isdir("logs"):
    os.mkdir("logs")

# https://docs.python.org/3/howto/logging-cookbook.html
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(name)-12s %(lineno)-8s %(levelname)-8s %(message)s",
    datefmt="%Y-%m-%d-%H-%M-%S",
    filename="./logs/scraper-rss-{}.log".format(
        datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    ),
    filemode="w",
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter("%(name)-12s: %(levelname)-8s %(message)s")
console.setFormatter(formatter)
logging.getLogger("").addHandler(console)


CACHE_FILE = "cache.txt"
OUTPUT_FILENAME = "output.jsonl"
THREAD_LIMIT = 10
THREAD_TIMEOUT = 180  # seconds

REQUEST_TIMEOUT = 5

HEADER = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
}
CACHE = set()
SEED_QUEUE = queue.Queue()
EXTRACT_QUEUE = queue.Queue()
RSS_STACK = {}


class SeedUrlContent:
    def __init__(
        self, locale="", root_url="", schema={}, soup_page="", is_xml=True, news_list=[]
    ):
        self.locale = locale
        self.root_url = root_url
        self.schema = schema
        self.soup_page = soup_page
        self.is_xml = is_xml
        self.news_list = news_list

        self.parse_schema()

    def parse_schema(self):
        if "not_xml" in self.schema and self.schema["not_xml"] is True:
            self.is_xml = False

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
                "SeedUrlContent object missing required attributes: root_url, locale"
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
            title = self.get_title_from_for_html(a_tag_node)
            description = self.get_description_from_for_html(a_tag_node)

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

            if not self.is_valid_url(news_object.news_url):
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

                if date_tag_name in set(["pubDate", "published_date"]):
                    date_tag = node.find(date_tag_name)
                    if date_tag:
                        date_string_value = date_tag.text
                        published_at_dt_object = convert_date_to_datetime_object(
                            date_string_value
                        )

                else:
                    try:
                        date_string_value = node.find(date_tag_name).text
                    except Exception as e:
                        # "Fail to convert extract date_tag_name. Most likely irregular xml format. date_tag_name: {}, Node: {} Skipping..."
                        continue

                    try:
                        published_at_dt_object = datetime.strptime(
                            date_string_value, date_value_dt_format
                        )
                    except Exception as e:
                        # "Fail to convert publishedAt datetime format. Most likely irregular xml format. Value: {}, Format: {} Skipping..."
                        continue

                insert_article = is_article_uploaded_today(published_at_dt_object)

            if not insert_article:
                continue

            # process time before URL for early catching
            news_url = node.find(self.schema["url"]).text.strip()
            if news_url.endswith(".xml"):
                SEED_QUEUE.put(
                    SeedUrlContent(
                        locale=self.locale, root_url=news_url, schema=self.schema,
                    )
                )
                continue

            if not self.is_valid_url(news_url):
                continue

            node_title = ""
            node_description = ""
            if "title" not in self.schema and "description" not in self.schema:
                # sitemap doesn't have title or description at all
                # so we have to go through each URL to check if CORONA_KEYWORDS exists
                pass
            elif "keywords" in self.schema:
                keywords = node.find(self.schema["keywords"]).text
                if not corona_keyword_exists_in_string(keywords.lower()):
                    continue
            else:
                # sitemap that contains either title or description
                # early detection if URL contains CORONA_KEYWORDS or not
                if "title" in self.schema:
                    node_title = node.find(self.schema["title"]).text

                if "description" in self.schema:
                    node_description = node.find(self.schema["description"]).text

                # check if any of the CORONA_KEYWORDS occur in title or description
                corona_keywords_exist = corona_keyword_exists_in_string(
                    node_title.lower()
                ) or corona_keyword_exists_in_string(node_description.lower())
                if not corona_keywords_exist:
                    continue

            news_object.news_url = news_url
            news_object.title = node_title
            news_object.description = node_description
            news_object.published_at = published_at_dt_object
            self.news_list.append(news_object)

    def is_valid_url(self, url):
        if len(url.strip()) == 0:
            return False
        if not re.findall(
            r"^http[s]?://", url, re.IGNORECASE
        ) or self.is_blacklist_keywords_in_url(url):
            return False
        return True

    def is_blacklist_keywords_in_url(self, url):
        for keyword in URL_BLACKLIST_KEYWORDS:
            if keyword in url:
                return True
        return False

    def get_title_from_for_html(self, node):
        title = node.find("title")
        if not title:
            title = node.find("h1")
        if not title:
            title = node.find("h2")
        return title.text if title else ""

    def get_description_from_for_html(self, node):
        description = node.find("p")
        return description.text if description else ""

    def add_news_to_extraction_queue(self):
        for news_object in self.news_list:
            EXTRACT_QUEUE.put(news_object)

    @staticmethod
    def get_seed_page(url):
        try:
            logging.debug("Get seed url: {}".format(url))
            res = requests.get(url, headers=HEADER, timeout=REQUEST_TIMEOUT)
            return res
        except Exception as e:
            logging.error("Fail to get url: {}".format(url))
            raise e


class NewsContent:
    def __init__(
        self,
        news_url="",
        title="",
        description="",
        published_at=None,
        seed_source=None,
    ):
        self.news_url = news_url
        self.title = title
        self.description = description
        self.published_at = published_at
        self.seed_source = seed_source


def seed_worker():
    while True:
        seed_object = SEED_QUEUE.get()
        if seed_object is None:
            break

        root_url = seed_object.root_url

        try:
            seed_object.validate_required_values()
            res = seed_object.get_seed_page(root_url)
        except Exception as e:
            logging.error(e)
            SEED_QUEUE.task_done()
            continue

        page_content = res.content
        seed_object.parse_seed_page_content(page_content)
        seed_object.add_news_to_extraction_queue()
        SEED_QUEUE.task_done()


def extract_worker():
    while True:
        approx_queue_size = EXTRACT_QUEUE.qsize()
        if approx_queue_size % 10 == 0:
            logging.debug(
                "===> Approximately {} item(s) in the queue ...".format(
                    approx_queue_size
                )
            )

        news_object = EXTRACT_QUEUE.get()

        if news_object is None:
            break

        rss_record = {}
        rss_record["url"] = news_object.news_url

        # early catching, capture cached url or blacklist keywords. eg: "/archives/"
        if rss_record["url"] in CACHE:
            EXTRACT_QUEUE.task_done()
            continue

        if not READ_ALL_SKIP_CACHE:
            write_to_cache(rss_record["url"])
        CACHE.add(rss_record["url"])

        # Process article
        article, status = extract_article(rss_record["url"])
        if not status:
            EXTRACT_QUEUE.task_done()
            continue

        # Overwrite description if exists in meta tag
        rss_record["description"] = attempt_extract_from_meta_data(
            article.meta_data, "description", news_object.description
        )
        rss_record["title"] = attempt_extract_from_meta_data(
            article.meta_data, "title", news_object.title
        )

        keywords = attempt_extract_from_meta_data(article.meta_data, "keywords", "")
        if not isinstance(keywords, str):
            print("keywords not string: {}".format(keywords))
            keywords = " ".join(keywords)

        # If keyword doesn't exists in article, skip
        if (
            not corona_keyword_exists_in_string(rss_record["description"].lower())
            and not corona_keyword_exists_in_string(rss_record["title"].lower())
            and not corona_keyword_exists_in_string(keywords.lower())
        ):
            EXTRACT_QUEUE.task_done()
            continue

        # Get language and country
        locale = news_object.seed_source.locale
        lang_locale = locale.split("_")
        if len(lang_locale) < 2:
            logging.error(
                "Locale format in seed is incorrect, should be in xx_YY format. Eg: ms_MY (malay, Malaysia)."
            )
            EXTRACT_QUEUE.task_done()
            continue

        lang, country = lang_locale[0], lang_locale[1]
        rss_record["language"] = lang if locale not in SPECIAL_LANG else locale
        rss_record["countryCode"] = country

        # Get siteName
        rss_record["siteName"] = re.sub(r"https?://(www\.)?", "", article.source_url)

        # Get the authors
        rss_record["author"] = ", ".join(article.authors)

        # Get the publish date
        rss_record["publishedAt"] = get_published_at_value(
            news_object.published_at, article, news_object.seed_source.soup_page
        )

        # Set addedOn after publish date
        rss_record["addedOn"] = datetime.utcnow().strftime(DATE_FORMAT)

        rss_record["content"] = article.text
        # Get the top image
        rss_record["urlToImage"] = article.top_image

        if locale not in RSS_STACK:
            RSS_STACK[locale] = []
        RSS_STACK[locale].append(rss_record)

        EXTRACT_QUEUE.task_done()


def is_article_uploaded_today(dt_object):
    if dt_object is None:
        return True
    time_difference_days = (datetime.utcnow() - dt_object.replace(tzinfo=None)).days
    if time_difference_days > 0:
        # difference > 1 day, skip
        return False
    return True


def get_published_at_value(published_at_dt_object, article, soup_page):
    published_at_value = ""
    published_at_source = ""
    dt_object = published_at_dt_object
    if dt_object and valid_dt_value(dt_object):
        dt_object = convert_date_to_datetime_object(dt_object)
        source = "from seed page"

    elif attempt_extract_from_meta_data(article.meta_data, "published_time", dt_object):
        dt_object = convert_date_to_datetime_object(
            attempt_extract_from_meta_data(
                article.meta_data, "published_time", dt_object
            )
        )
        source = "meta_data -> published_time"

    elif attempt_extract_from_meta_data(article.meta_data, "modified_time", dt_object):
        dt_object = convert_date_to_datetime_object(
            attempt_extract_from_meta_data(
                article.meta_data, "modified_time", dt_object
            )
        )
        source = "meta_data -> modified_time"

    elif soup_page.lastBuildDate:
        dt_object = convert_date_to_datetime_object(soup_page.lastBuildDate.text)
        source = "soup_page -> lastBuildDate"

    else:
        # Worst case: put current date and tmie
        # Reason: since we're constantly crawling (on cron)
        #           sites that publishes latest articles only
        #           it's highly likely we're getting today's article
        dt_object = datetime.utcnow()
        source = "None, using current time."

    published_at_log_msg = "Found publishedAt in: {} with unix timestamp value: {} | Current unix timestamp: {} | Is timestamp > current timestamp: {}"
    unix_extracted = datetime.timestamp(dt_object)
    unix_now = datetime.timestamp(datetime.utcnow())
    if unix_extracted < unix_now:
        logging.debug(
            published_at_log_msg.format(
                source, unix_extracted, unix_now, unix_extracted > unix_now,
            )
        )
    else:
        logging.warning(
            published_at_log_msg.format(
                "meta_data -> modified_time",
                unix_extracted,
                unix_now,
                unix_extracted > unix_now,
            )
        )

    # reset if extracted time is greater than current time
    if unix_extracted > unix_now:
        logging.warning(
            "Extracted timestamp is greater than current timestamp. Resetting to current timestamp"
        )
        dt_object = datetime.utcnow()
    return str(dt_object.strftime(DATE_FORMAT))


def valid_dt_value(dt_object):
    # this function is to capture if we got the dt object from
    # %Y-%m-%d (without any timezone information)
    # if no timezone, return invalid, try to find from soup page or meta
    if dt_object.hour == 0 and dt_object.minute == 0 and dt_object.second == 0:
        return False
    return True


def corona_keyword_exists_in_string(string):
    # this works well if for words that are split by space/comma
    # fails for languages that doesn't need space/comma
    # hence, do brute force to check keyword in string
    # eg: 武漢肺炎中國確診逾, where 武漢肺炎 is coronavirus
    if len(set(re.findall(r"\w+", string)).intersection(CORONA_KEYWORDS)) != 0:
        return True
    # Fallback: if can't find, search each keyword in string, brute force
    for keyword in CORONA_KEYWORDS:
        if keyword in string:
            return True
    return False


def attempt_extract_from_meta_data(meta_data, attribute, original_value):
    logging.debug(
        "Start attempt look for attribute: {}. Original value: {}".format(
            attribute, original_value if original_value else "None"
        )
    )
    if attribute in meta_data and isinstance(meta_data[attribute], str):
        logging.debug(
            "Found attribute: {} in meta_data. value: {}".format(
                attribute, meta_data[attribute]
            )
        )
        return meta_data[attribute]

    # try og tag
    if (
        "og" in meta_data
        and attribute in meta_data["og"]
        and len(meta_data["og"][attribute].strip())
    ):
        logging.debug(
            "Found attribute: {} in og. value: {}".format(
                attribute, meta_data["og"][attribute]
            )
        )
        return meta_data["og"][attribute]

    # article tag
    if (
        "article" in meta_data
        and attribute in meta_data["article"]
        and len(meta_data["article"][attribute].strip())
    ):
        logging.debug(
            "Found attribute: {} in article. value: {}".format(
                attribute, meta_data["article"][attribute]
            )
        )
        return meta_data["article"][attribute]

    # if all fails, return default value
    logging.debug(
        "Fail to find attribute: {} using default value: {}".format(
            attribute, original_value
        )
    )
    return original_value


def convert_date_to_datetime_object(date_string):
    if not isinstance(date_string, str):
        # could already be a datetime object as initial value extracted in SeedUrlContent
        logging.debug(
            "Input date already in datetime value: {}. UTC: {}. Skipping convertion...".format(
                date_string, date_string.astimezone(timezone.utc)
            )
        )
        return date_string.astimezone(timezone.utc)

    logging.debug("Input date: {}".format(date_string))
    if len(re.findall(DATE_RFC_2822_REGEX_RULE, date_string,)) > 0:
        match_dateformat = re.findall(DATE_RFC_2822_REGEX_RULE, date_string,)
        datetime_str = match_dateformat[0].strip()
        original_datetime_format = datetime.strptime(
            datetime_str, DATE_RFC_2822_DATE_FORMAT
        )

    elif len(re.findall(DATE_ISO_8601_REGEX_RULE, date_string,)) > 0:
        # Fall back to try datetime ISO 8601 format
        match_dateformat = re.findall(DATE_ISO_8601_REGEX_RULE, date_string,)
        datetime_str = match_dateformat[0].strip()
        if datetime_str.endswith("Z"):
            # seen 2020-02-05T08:13:54.000Z
            right_index = len(datetime_str) - 1
            while right_index > 0 and datetime_str[right_index] != ".":
                right_index -= 1
            datetime_str = datetime_str[:right_index] + "+0000"
        original_datetime_format = datetime.strptime(datetime_str, ISO_8601_DATE_FORMAT)

    else:
        # if fail to extract, log here, figure out the pattern offline
        # use current time for now
        logging.error(
            "Fail to extract date format. Fix required for date_string: {}".format(
                date_string
            )
        )
        original_datetime_format = datetime.utcnow()

    return original_datetime_format.astimezone(timezone.utc)


def extract_article(link):
    logging.debug("Extracting from: {}".format(link))
    try:
        article = Article(link, headers=HEADER)
        # Do some NLP
        article.download()  # Downloads the link's HTML content
        article.parse()  # Parse the article
        article.nlp()  #  Keyword extraction wrapper
    except Exception as e:
        logging.error("Fail to extract Article. Error: {}".format(e))
        return None, False
    return article, True


def print_pretty():
    for locale, rss_records in RSS_STACK.items():
        for rss_record in rss_records:
            to_print = ""
            to_print += "\ntitle:\t" + rss_record["title"]
            to_print += "\ndescription:\t" + rss_record["description"]
            to_print += "\nurl:\t" + rss_record["url"]
            to_print += "\npublishedAt:\t" + rss_record["publishedAt"]
            to_print += "\naddedOn:\t" + rss_record["addedOn"]
            to_print += "\nauthor:\t" + rss_record["author"]
            to_print += "\ncontent:\n" + rss_record["content"]
            to_print += "\nurlToImage:\t" + rss_record["urlToImage"]
            to_print += "\nlanguage:\t" + rss_record["language"]
            to_print += "\ncountryCode:\t" + rss_record["countryCode"]
            to_print += "\nsiteName:\t" + rss_record["siteName"]
            to_print += ""
            try:
                print(to_print.expandtabs())
            except:
                pass


def write_output():
    for locale, rss_records in RSS_STACK.items():
        with open("data/{}/output.jsonl".format(locale), "w") as fh:
            for rss_record in rss_records:
                json.dump(rss_record, fh)
                fh.write("\n")


def save_to_db():
    logging.debug(
        "Saving to db to {} table".format("Prod" if WRITE_TO_PROD_TABLE else "Test")
    )
    db_connector.connect()
    for locale, rss_records in RSS_STACK.items():
        for rss_record in rss_records:
            db_connector.insert(rss_record, "prod" if WRITE_TO_PROD_TABLE else "test")


def parser():
    parser = argparse.ArgumentParser(description="Scrape XML sources")
    parser.add_argument("-d", "--debug", action="store_true", help="Debugging")
    parser.add_argument("-c", "--clear", action="store_true", help="Clear Cache")
    parser.add_argument(
        "-p", "--production", action="store_true", help="Writes to production table"
    )
    parser.add_argument(
        "-a", "--all", action="store_true", help="Skip read and write on cache"
    )
    return parser.parse_args()


def read_cache():
    with open(CACHE_FILE, "r") as fh:
        stream = fh.read()
        for row in stream.split("\n"):
            CACHE.add(row)


def write_to_cache(url):
    with open(CACHE_FILE, "a+") as fh:
        fh.write(url + "\n")


if __name__ == "__main__":
    # arguments
    args = parser()

    READ_ALL_SKIP_CACHE = args.all
    WRITE_TO_DB_MODE = not args.debug
    WRITE_TO_PROD_TABLE = args.production

    # create required folders
    if not os.path.isdir("data"):
        logging.debug("Creating ./data directory")
        os.mkdir("./data")

    # reset cache
    if args.clear:
        logging.debug("Clearing cache file {}".format(CACHE_FILE))
        os.system("rm {}".format(CACHE_FILE))

    # check cache file exists
    if not os.path.isfile(CACHE_FILE):
        logging.debug("Creating cache file {}".format(CACHE_FILE))
        os.system("touch {}".format(CACHE_FILE))

    # if set READ_ALL_SKIP_CACHE, skip reading cache
    if not READ_ALL_SKIP_CACHE:
        logging.debug("Reading cache file...")
        read_cache()

    # initialize threads
    THREADS = []

    # extract all xml data
    for i in range(THREAD_LIMIT):
        t = threading.Thread(target=seed_worker)
        t.start()
        THREADS.append(t)

    # place initial seed urls to seed queue to process
    for locale, list_url_schema in NEWS_URLs.items():
        logging.debug(
            "locale: {}, Number of websites: {}".format(locale, len(list_url_schema))
        )
        if not os.path.isdir("./data/{}".format(locale)):
            os.mkdir("./data/{}".format(locale))
        for url_schema in list_url_schema:
            url, schema = url_schema
            logging.debug(
                "Adding seed url to queue: {}. Schema: {}".format(url, schema)
            )
            SEED_QUEUE.put(SeedUrlContent(locale=locale, root_url=url, schema=schema))

    # end seed workers
    SEED_QUEUE.join()
    for i in range(len(THREADS)):
        SEED_QUEUE.put(None)

    logging.debug(
        "Done extracting all root urls. Approximately {} work to crunch.".format(
            EXTRACT_QUEUE.qsize()
        )
    )

    # process extracted urls
    for i in range(len(THREADS)):
        THREADS[i] = threading.Thread(target=extract_worker)
        THREADS[i].start()

    # end extract workers
    EXTRACT_QUEUE.join()
    for i in range(len(THREADS)):
        EXTRACT_QUEUE.put(None)

    logging.debug("Done extracting all feed data")

    if not RSS_STACK:
        logging.debug("RSS Stack is empty. Exiting...")
        exit()

    if WRITE_TO_DB_MODE:
        # Store to DB
        save_to_db()
    else:
        # print output and write to jsonl file
        print_pretty()
        write_output()

    count = 0
    for lang, rss_records in RSS_STACK.items():
        count += len(rss_records)
    logging.debug("Total feeds: {}".format(count))
    logging.debug("Done scraping.")
