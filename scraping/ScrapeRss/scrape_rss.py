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
# python ScrapeRss/scrape_rss.py  -c -d
#   -d : debug mode, write to output.jsonl, else, write to db. default=True
#   -c : clear cache, default=False
#   -a : get all, skip cache. api uses this to crawl everything
#        - update database doesn't use this, to prevent duplicated entries
#
# Example:
#   - write to db with log messages, doesn't update ./data/<lang>/output.jsonl
#       - python ScrapeRss/scrape_rss.py        # writes to test table
#       - python ScrapeRss/scrape_rss.py  --table  [ TABLE NAME ]
#   - debug only
#       d flag so it doesn't write to db (prints output and write to output.jsonl)
#       a flag will skip read and write to cache
#       - python ScrapeRss/scrape_rss.py  -d -a
#
# NOTE:
#   - Using black to format the code. Feel free to use it (https://black.readthedocs.io/en/stable/)
#

import sys
import os

# The root class of the aggregate
# Individual scrape_rss entities are identified by their scraperID

class scrape_rss:
    def __init__(self, scraperID):
        self.scraperID = scraperID;

# Below is the original code for scrape_rss.py

# Connect to db_connector from parent directory
PARENT_DIR = ".."
CURRENT_DIR = os.path.dirname(
    os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__)))
)
sys.path.append(os.path.normpath(os.path.join(CURRENT_DIR, PARENT_DIR)))

from datetime import datetime
from dateutil.parser import parse
import threading
import argparse
import logging
import json
import re

# nltk updates
import nltk

nltk.download("punkt")

# # Global
RSS_STACK = {}
CACHE = set()

# Database configurations
from DatabaseConnector.db_connector import DatabaseConnector

db_connector = DatabaseConnector(config_path="./db.json")
db_connector.connect()

# temporary solution as migrating to new db prod instance
db_connector_prodv2 = DatabaseConnector(config_path="./db.prodv2.json")
db_connector_prodv2.connect()

# NewsContent
from ScrapeRss.NewsContent import NewsContent

# Constant values
from ScrapeRss.globals import CACHE_FILE, OUTPUT_FILENAME
from ScrapeRss.globals import HEADER, THREAD_LIMIT
from ScrapeRss.globals import DATE_FORMAT, CORONA_KEYWORDS, SPECIAL_LANG
from ScrapeRss.globals import SEED_QUEUE, EXTRACT_QUEUE

# Helper functions
from ScrapeRss.helpers import (
    get_seed_page,
    get_title_from_article,
    get_published_at_value,
    get_author_value,
)
from ScrapeRss.helpers import (
    attempt_extract_from_meta_data,
    corona_keyword_exists_in_string,
    extract_article,
)

global READ_ALL_SKIP_CACHE

# LOGGER CONFIG
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


def seed_worker():
    while True:
        seed_object = SEED_QUEUE.get()
        if seed_object is None:
            break

        root_url = seed_object.root_url

        try:
            seed_object.validate_required_values()
            res = get_seed_page(root_url)
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
        rss_record["title"] = get_title_from_article(article, news_object)

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
        rss_record["language"] = (
            lang
            if (lang, country) not in SPECIAL_LANG
            else SPECIAL_LANG[(lang, country)]
        )
        rss_record["countryCode"] = country

        # Get siteName
        rss_record["siteName"] = re.sub(r"https?://(www\.)?", "", article.source_url)

        # Get the authors
        rss_record["author"] = get_author_value(news_object.author, article)

        # Get the publish date
        rss_record["publishedAt"] = get_published_at_value(
            news_object.published_at, article, news_object.seed_source.soup_page
        )

        # Set addedOn after publish date
        rss_record["addedOn"] = datetime.utcnow().strftime(DATE_FORMAT)

        rss_record["content"] = (
            article.text if article.text else rss_record["description"]
        )
        # Get the top image
        rss_record["urlToImage"] = article.top_image

        if locale not in RSS_STACK:
            RSS_STACK[locale] = []
        RSS_STACK[locale].append(rss_record)

        EXTRACT_QUEUE.task_done()


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
        with open("data/{}/{}".format(locale, OUTPUT_FILENAME), "w") as fh:
            for rss_record in rss_records:
                json.dump(rss_record, fh)
                fh.write("\n")


def save_to_db(table_name):
    logging.debug("Saving to db to {} table".format(table_name))
    for locale, rss_records in RSS_STACK.items():
        for rss_record in rss_records:
            db_connector.insert_news_article(rss_record, table_name)
            db_connector_prodv2.insert_news_article(rss_record, table_name)


def parser():
    parser = argparse.ArgumentParser(description="Scrape XML sources")
    parser.add_argument("-d", "--debug", action="store_true", help="Debugging")
    parser.add_argument("-c", "--clear", action="store_true", help="Clear Cache")
    parser.add_argument(
        "-t",
        "--table",
        help="Database table name to write to.",
        default="newsapi_n_temp",
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
    debug_mode = args.debug
    database_table_name = args.table

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
    for locale, list_url_schema in NEWS_SOURCES.items():
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
            seed_object = NewsParser(locale=locale, root_url=url, schema=schema)
            SEED_QUEUE.put(seed_object)

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

    if debug_mode:
        # print output and write to jsonl file
        print_pretty()
        write_output()
    else:
        # Store to DB
        save_to_db(database_table_name)

    count = 0
    for lang, rss_records in RSS_STACK.items():
        count += len(rss_records)
    logging.debug("Total feeds: {}".format(count))
    logging.debug("Done scraping.")

    # rss_sites entity
    # Code added from rss_sites.py to avoid deep references

    from ScrapeRss.globals import (
        ISO_8601_DATE_FORMAT,
        ISO_8601_DATE_WITHOUT_SEC_FORMAT,
        YEAR_MONTH_DAY_FORMAT,
    )

    NEWS_SOURCES = {
        "de_DE": [
            (
                "https://www.welt.de/sitemaps/newssitemap/newssitemap.xml",
                {
                    "url": "loc",
                    "title": "news:title",
                    "keywords": "news:keywords",
                    "date_xml": ("news:publication_date", ISO_8601_DATE_FORMAT),
                },
            ),
            (
                "https://www.welt.de/sitemaps/sitemap/today.xml",
                {
                    "url": "loc",
                    "title": "image:title",
                    "date_xml": ("lastmod", ISO_8601_DATE_FORMAT),
                },
            ),
            ("https://www.focus.de/", {"not_xml": True, },),
            ("https://www.faz.net/aktuell/", {"not_xml": True, },),
        ],
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
                {"title": "title", "description": "description", "url": "link", },
            ),
            # (
            #     "http://www.dailytelegraph.com.au/news/national/rss",
            #     {"title": "title", "description": "description", "url": "link",},
            # ),
            (
                "http://www.dailytelegraph.com.au/newslocal/rss",
                {"title": "title", "description": "description", "url": "link", },
            ),
            # (
            #     "http://www.dailytelegraph.com.au/news/world/rss",
            #     {"title": "title", "description": "description", "url": "link",},
            # ),
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
        "en_IN": [
            (
                "https://www.thehindu.com/sitemap/googlenews.xml",
                {
                    "title": "news:title",
                    "url": "loc",
                    "keywords": "news:keywords",
                    "date_xml": ("lastmod", ISO_8601_DATE_FORMAT),
                },
            ),
        ],
        "en_TW": [
            (
                "http://www.taipeitimes.com/sitemap.xml",
                {"url": "loc", "date_xml": ("lastmod", ISO_8601_DATE_FORMAT), },
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
        "en_KR": [
            (
                "http://english.chosun.com/site/data/rss/rss.xml",
                {
                    "title": "title",
                    "description": "description",
                    "url": "link",
                    "date_xml": ("dc:date", ISO_8601_DATE_FORMAT),
                },
            ),
            (
                "http://www.koreatimes.co.kr/www/rss/world.xml",
                {
                    "title": "title",
                    "description": "description",
                    "url": "link",
                    "author": "author",
                },
            ),
            (
                "http://www.koreatimes.co.kr/www/rss/nation.xml",
                {
                    "title": "title",
                    "description": "description",
                    "url": "link",
                    "author": "author",
                },
            ),
            (
                "http://koreajoongangdaily.joins.com/sitemap_google_news.xml",
                {
                    "title": "news:title",
                    "url": "loc",
                    "date_xml": ("news:publication_date", YEAR_MONTH_DAY_FORMAT),
                },
            ),
        ],
        "hi_IN": [
            (
                "https://www.livehindustan.com/news-sitemap.xml",
                {
                    "title": "news:title",
                    "url": "loc",
                    "keywords": "news:keywords",
                    "date_xml": ("lastmod", ISO_8601_DATE_FORMAT),
                },
            ),
            (
                "https://www.bhaskar.com/sitemapgoogle/topnews_1.xml",
                {
                    "title": "news:title",
                    "url": "loc",
                    "keywords": "news:keywords",
                    "date_xml": ("news:publication_date", ISO_8601_DATE_FORMAT),
                },
            ),
            (
                "https://www.jagran.com/news-sitemap.xml",
                {
                    "title": "news:title",
                    "url": "loc",
                    "keywords": "news:keywords",
                    "date_xml": ("news:publication_date", ISO_8601_DATE_FORMAT),
                },
            ),
        ],
        "ko_KR": [
            (
                "https://news.chosun.com/google/rss.html",
                {
                    "title": "title",
                    "description": "description",
                    "url": "link",
                    "date_xml": ("pubDate", None),
                },
            ),
            (
                "https://news.chosun.com/site/data/rss/rss.xml",
                {
                    "title": "title",
                    "description": "description",
                    "url": "link",
                    "author": "author",
                    "date_xml": ("dc:date", ISO_8601_DATE_FORMAT),
                },
            ),
            (
                "https://news.joins.com/sitemap/latest-articles",
                {
                    "title": "news:title",
                    "url": "loc",
                    "keywords": "news:keywords",
                    "date_xml": ("news:publication_date", ISO_8601_DATE_FORMAT),
                },
            ),
            (
                "http://www.donga.com/sitemap/donga-newsmap.xml",
                {
                    "title": "news:title",
                    "url": "loc",
                    "date_xml": ("news:publication_date", ISO_8601_DATE_FORMAT),
                },
            ),
            (
                "http://www.hani.co.kr/arti/RSS/sitemap_www.xml",
                {
                    "title": "news:title",
                    "url": "loc",
                    "date_xml": ("news:publication_date", ISO_8601_DATE_WITHOUT_SEC_FORMAT),
                },
            ),
        ],
        "en_QA": [
            (
                "https://www.aljazeera.com/xml/sslsitemaps/sitemap2020_1.xml",
                {"url": "loc", "date_xml": ("lastmod", YEAR_MONTH_DAY_FORMAT), },
            ),
        ],
        "id_ID": [("https://news.kompas.com/web/sitemap.xml", {"url": "loc", },), ],
        "it_IT": [
            (
                "https://www.ilmessaggero.it/?sez=XML&p=MapNews",
                {
                    "title": "news:title",
                    "url": "loc",
                    "keywords": "news:keywords",
                    "date_xml": ("news:publication_date", ISO_8601_DATE_FORMAT),
                },
            ),
            (
                "https://www.leggo.it/?sez=XML&p=MapNews",
                {
                    "title": "news:title",
                    "url": "loc",
                    "keywords": "news:keywords",
                    "date_xml": ("news:publication_date", ISO_8601_DATE_FORMAT),
                },
            ),
            (
                "https://www.lastampa.it/sitemap.xml",
                {"url": "loc", "date_xml": ("lastmod", ISO_8601_DATE_FORMAT), },
            ),
        ],
        "ja_JP": [
            (
                "https://toyokeizai.net/sitemap.xml",
                {"url": "loc", "date_xml": ("lastmod", ISO_8601_DATE_FORMAT), },
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
        "ta_IN": [
            (
                "https://www.dailythanthi.com/Sitemap/googlesitemap.xml",
                {
                    "title": "news:title",
                    "url": "loc",
                    "keywords": "news:keywords",
                    "date_xml": ("lastmod", ISO_8601_DATE_FORMAT),
                },
            ),
            (
                "https://www.maalaimalar.com/Sitemap/googlesitemap.xml",
                {
                    "title": "news:title",
                    "url": "loc",
                    "keywords": "news:keywords",
                    "date_xml": ("lastmod", ISO_8601_DATE_FORMAT),
                },
            ),
            (
                "https://www.hindutamil.in/feed/news-corona-virus-518.xml",
                {
                    "title": "news:title",
                    "url": "loc",
                    "keywords": "news:keywords",
                    "date_xml": ("lastmod", ISO_8601_DATE_FORMAT),
                },
            ),
            ("https://www.timestamilnews.com/", {"not_xml": True, },),
        ],
        "th_TH": [
            ("https://thestandard.co/coronavirus-coverage/", {"not_xml": True, },),
            (
                "https://www.thairath.co.th/sitemap-daily.xml",
                {"url": "loc", "title": "image:title", },
            ),
            (
                "https://rss.komchadluek.net/latest_news_google_news.xml",
                {
                    "url": "loc",
                    "title": "news:title",
                    "keywords": "news:keywords",
                    "date_xml": ("news:publication_date", ISO_8601_DATE_FORMAT),
                },
            ),
            (
                "https://rss.komchadluek.net/latest_news_google_news.xml",
                {
                    "url": "loc",
                    "title": "news:title",
                    "keywords": "news:keywords",
                    "date_xml": ("news:publication_date", ISO_8601_DATE_FORMAT),
                },
            ),
        ],
        "en_MY": [
            (
                "https://www.malaymail.com/sitemap.xml",
                {
                    "url": "loc",
                    "title": "news:title",
                    "keywords": "news:keywords",
                    "date_xml": ("news:publication_date", ISO_8601_DATE_FORMAT),
                },
            ),
        ],
        "ms_MY": [
            (
                "https://www.projekmm.com/sitemap.xml",
                {
                    "url": "loc",
                    "title": "news:title",
                    "keywords": "news:keywords",
                    "date_xml": ("news:publication_date", ISO_8601_DATE_FORMAT),
                },
            ),
        ],
        "nl_NL": [
            (
                "https://www.nu.nl/sitemap_news.xml",
                {
                    "url": "loc",
                    "title": "news:title",
                    "keywords": "news:keywords",
                    "date_xml": ("news:publication_date", ISO_8601_DATE_FORMAT),
                },
            ),
            (
                "https://www.rivm.nl/sitemap.xml",
                {
                    "url": "loc",
                    "date_xml": ("lastmod", ISO_8601_DATE_FORMAT),
                    "custom_blacklist": ["/en/"],
                },
            ),
            (
                "https://www.nrc.nl/sitemap/index.xml",
                {"url": "loc", "date_xml": ("lastmod", ISO_8601_DATE_FORMAT), },
            ),
        ],
        "zh_MY": [
            (
                "https://www.orientaldaily.com.my/sitemap.xml",
                {
                    "url": "loc",
                    "title": "news:title",
                    "date_xml": ("news:publication_date", ISO_8601_DATE_FORMAT),
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
                {"url": "loc", "date_xml": ("lastmod", YEAR_MONTH_DAY_FORMAT), },
            ),
        ],
        "zh_CN": [
            (
                "http://www.gov.cn/google.xml",
                {"url": "loc", "date_xml": ("lastmod", ISO_8601_DATE_FORMAT), },
            ),
        ],
        "zh_TW": [
            (
                "https://news.cts.com.tw/sitemap.xml",
                {"url": "loc", "date_xml": ("lastmod", YEAR_MONTH_DAY_FORMAT), },
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

    # NewsParser entity
    # Code from NewsParser.py added to the root class to avoid deep references

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

        def parse_schema(self):
            if "not_xml" in self.schema and self.schema["not_xml"] is True:
                self.is_xml = False
            if "custom_blacklist" in self.schema:
                self.custom_blacklist = self.custom_blacklist.union(
                    set(self.schema["custom_blacklist"])
                )

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
