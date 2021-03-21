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


# import all news sources
from ScrapeRss.rss_sites import NEWS_SOURCES

# NewsParser
from ScrapeRss.NewsParser import NewsParser

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
