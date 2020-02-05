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
https://www.theage.com.au/rss/world.xml
https://www.news.com.au/content-feeds/latest-news-world/
https://www.news.com.au/content-feeds/latest-news-national/
http://www.dailytelegraph.com.au/news/breaking-news/rss
http://www.dailytelegraph.com.au/news/national/rss
http://www.dailytelegraph.com.au/newslocal/rss
http://www.dailytelegraph.com.au/news/world/rss
https://www.sbs.com.au/news/topic/latest/feed
https://www.channelnewsasia.com/googlenews/cna_news_sitemap.xml

Don't crawl:
http://www.heraldsun.com.au/news/breaking-news/rss
http://www.heraldsun.com.au/rss

"""

# some sitemap contains different attributes
NEWS_URLs = {
    "en": [
        (
            "https://www.scmp.com/rss/318208/feed",
            {"title": "title", "description": "description", "url": "link",},
        ),
        (
            "https://www.theage.com.au/rss/feed.xml",
            {"title": "title", "description": "description", "url": "link",},
        ),
        (
            "https://www.theage.com.au/rss/world.xml",
            {"title": "title", "description": "description", "url": "link",},
        ),
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
            {"title": "title", "description": "description", "url": "link",},
        ),
        (
            "https://www.news.com.au/content-feeds/latest-news-national/",
            {"title": "title", "description": "description", "url": "link",},
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
            {"title": "title", "description": "description", "url": "link",},
        ),
        (
            "https://www.channelnewsasia.com/googlenews/cna_news_sitemap.xml",
            {
                "title": "title",
                "description": "news:keywords",
                "url": "loc",
                "publish_date": "news:publication_date",
            },
        ),
        (
            "https://www.shine.cn/sitemap-news.xml",
            {
                "title": "news:title",
                "url": "loc",
                "publish_date": "news:publication_date",
            },
        ),
        (
            "http://www.taipeitimes.com/sitemap.xml",
            {
                "url": "loc",
                "publish_date": "lastmod",
            }
        ),
        (
            "https://www.taiwannews.com.tw/en/sitemap.xml",
            {
                "title": "news:title",
                "url": "loc",
            },
        ),
    ],
    "zh_TW": [
        ("https://news.cts.com.tw/sitemap.xml", {"url": "loc"},),
        ("https://news.pts.org.tw/dailynews.php", {"not_xml": True},),
        (
            "https://www.taiwannews.com.tw/ch/sitemap.xml",
            {
                "title": "news:title",
                "url": "loc",
            },
        ),
        (
            "https://www.ettoday.net/news-sitemap.xml",
            {
                "title": "news:title",
                "url": "loc",
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

# CONSTANT VALUES
CACHE_FILE = "cache.txt"
OUTPUT_FILENAME = "output.jsonl"

# "Sat, 25 Jan 2020 01:52:22 +0000"
DATE_RFC_2822_REGEX_RULE = r"[\d]{1,2} [ADFJMNOS]\w* [\d]{4} \b(?:[01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9] [\+]{1}[0-9]{4}\b"
DATE_RFC_2822_DATE_FORMAT = "%d %b %Y %H:%M:%S %z"
# ISO 8601 | 2020-01-31T22:10:38+0800 | 2020-02-05T08:13:54.000Z | 2017-04-17T22:23:24+00:00
DATE_ISO_8601_REGEX_RULE = (
    r"\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:?\d{0,2}[\+\.]\d{2,4}\:?[0-9]{0,2}Z?"
)
ISO_8601_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

CORONA_KEYWORDS = set(["corona", "coronavirus", "武漢肺炎", "冠状病毒"])
THREAD_LIMIT = 10

CACHE = set()
THREADS = []
XML_QUEUE = queue.Queue()
EXTRACT_FEED_QUEUE = queue.Queue()
RSS_STACK = {}


def news():
    while not XML_QUEUE.empty():
        try:
            lang, root_url_schema = XML_QUEUE.get()
        except queue.Empty:
            logging.error("Root/XML queue is empty.")
            return

        root_url, schema = root_url_schema
        logging.debug("Getting {}".format(root_url))
        header = {"User-Agent": "Mozilla/5.0"}
        news_list = []

        try:
            res = requests.get(root_url, headers=header, timeout=5)
        except:
            logging.error("Fail to get url: {}".format(root_url))
            return
        page = res.content

        # Attempt to crawl non xml sites
        if "not_xml" in schema and schema["not_xml"]:
            soup_page = BeautifulSoup(page, "html.parser")
            for url in soup_page.findAll("a"):
                if corona_keyword_exists_in_string(url.text):
                    news_list.append(url["href"])

        else:
            # xml sites
            soup_page = BeautifulSoup(page, "xml")
            news_list = soup_page.findAll("item")

        if not news_list:
            news_list = soup_page.findAll("url")

        for getfeed in news_list:
            EXTRACT_FEED_QUEUE.put((lang, root_url, soup_page, getfeed, schema))


def extract_feed_data():
    while not EXTRACT_FEED_QUEUE.empty():
        try:
            lang, root_url, soup_page, feed_source, schema = EXTRACT_FEED_QUEUE.get()
        except queue.Empty:
            logging.error("Feed Qeueu is empty.")
            return

        # Extract from xml
        if "title" not in schema and "description" not in schema:
            # sitemap doesn't have title or description at all
            # so we have to go through each URL to check if CORONA_KEYWORDS exists
            res_title = ""
            res_desc = ""
        else:
            # sitemap that contains either title or description
            # early detection if URL contains CORONA_KEYWORDS or not
            res_title = (
                feed_source.find(schema["title"]).text if "title" in schema else ""
            )
            res_desc = (
                feed_source.find(schema["description"]).text
                if "description" in schema
                else ""
            )

            # check if any of the CORONA_KEYWORDS occur in title or description
            if not corona_keyword_exists_in_string(
                res_title.lower()
            ) and not corona_keyword_exists_in_string(res_desc.lower()):
                continue

        rss_record = {}

        # feed_source should be BeautifulSoup object
        # if it's string, it's direct link to url (for attempt to crawl non-xml)
        rss_record["url"] = (
            feed_source
            if isinstance(feed_source, str)
            else feed_source.find(schema["url"]).text
        )

        if rss_record["url"] in CACHE:
            continue

        if not READ_ALL_SKIP_CACHE:
            add_to_cache(rss_record["url"])

        rss_record["addedOn"] = datetime.utcnow().strftime(DATE_FORMAT)

        # Process article
        article = extract_article(rss_record["url"])

        # Overwrite description if exists in meta tag
        rss_record["description"] = attempt_extract_from_meta_data(
            article.meta_data, "description", res_desc
        )
        rss_record["title"] = attempt_extract_from_meta_data(
            article.meta_data, "title", res_title
        )
        keywords = attempt_extract_from_meta_data(article.meta_data, "keywords", "")

        # If keyword doesn't exists in article, skip
        if (
            not corona_keyword_exists_in_string(rss_record["description"].lower())
            and not corona_keyword_exists_in_string(rss_record["title"].lower())
            and not corona_keyword_exists_in_string(keywords.lower())
        ):
            continue

        # Get language
        rss_record["language"] = lang  # article.meta_lang

        # Get siteName
        rss_record["siteName"] = re.sub(r"https?://(www\.)?", "", article.source_url)

        # Get the authors
        rss_record["author"] = ", ".join(article.authors)

        # Get the publish date
        rss_record["publishedAt"] = get_published_at_value(
            schema, feed_source, article, soup_page
        )

        rss_record["content"] = article.text
        # Get the top image
        rss_record["urlToImage"] = article.top_image

        if lang not in RSS_STACK:
            RSS_STACK[lang] = []
        RSS_STACK[lang].append(rss_record)


def get_published_at_value(schema, feed_source, article, soup_page):
    published_at_value = ""
    published_at_source = ""
    dt_object = None
    if "publish_date" in schema:
        # from root url, usually exists in sitemap.xml
        dt_object = convert_date_to_datetime_object(
            feed_source.find(schema["publish_date"]).text
        )
        source = "schema"
    elif attempt_extract_from_meta_data(article.meta_data, "modified_time", dt_object):
        dt_object = convert_date_to_datetime_object(
            attempt_extract_from_meta_data(
                article.meta_data, "modified_time", dt_object
            )
        )
        source = "meta_data -> modified_time"
    elif attempt_extract_from_meta_data(article.meta_data, "published_time", dt_object):
        dt_object = convert_date_to_datetime_object(
            attempt_extract_from_meta_data(
                article.meta_data, "published_time", dt_object
            )
        )
        source = "meta_data -> published_time"
    elif "pubDate" in feed_source and feed_source.pubDate:
        dt_object = convert_date_to_datetime_object(feed_source.pubDate.text)
        source = "feed_source -> pubDate"
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
                "meta_data -> modified_time",
                unix_extracted,
                unix_now,
                unix_extracted > unix_now,
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
        logging.warning("Extracted timestamp is greater than current timestamp. Resetting to current timestamp")
        dt_object = convert_date_to_datetime_object(datetime.utcnow())
    return str(dt_object.strftime(DATE_FORMAT))


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


def attempt_extract_from_meta_data(meta_data, attribute, cur_val):
    logging.debug(
        "Start attempt look for attribute: {}".format(
            attribute, cur_val if cur_val else "None"
        )
    )
    if attribute in meta_data and isinstance(meta_data[attribute], str):
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
    logging.warning(
        "Fail to find attribute: {} using default value: {}".format(attribute, cur_val)
    )
    return cur_val


def convert_date_to_datetime_object(date_string):
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
    article = Article(link)
    # Do some NLP
    article.download()  # Downloads the link's HTML content
    article.parse()  # Parse the article
    nltk.download("punkt")  # 1 time download of the sentence tokenizer
    article.nlp()  #  Keyword extraction wrapper
    return article


def print_pretty():
    for lang, rss_records in RSS_STACK.items():
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
            to_print += "\nsiteName:\t" + rss_record["siteName"]
            to_print += ""
            try:
                print(to_print.expandtabs())
            except:
                pass


def write_output():
    for lang, rss_records in RSS_STACK.items():
        with open("data/{}/output.jsonl".format(lang), "w") as fh:
            for rss_record in rss_records:
                json.dump(rss_record, fh)
                fh.write("\n")


def save_to_db():
    logging.debug("Saving to db to {} table".format(WRITE_TO_PROD_TABLE))
    db_connector.connect()
    for lang, rss_records in RSS_STACK.items():
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


def add_to_cache(url):
    with open(CACHE_FILE, "a+") as fh:
        fh.write(url + "\n")
    CACHE.add(url)


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

# place initial xml urls to queue
for lang, all_rss in NEWS_URLs.items():
    logging.debug("Lang: {}, Number of rss: {}".format(lang, len(all_rss)))
    if not os.path.isdir("./data/{}".format(lang)):
        os.mkdir("./data/{}".format(lang))
    for rss in all_rss:
        logging.debug("Adding rss to queue: {}".format(rss))
        XML_QUEUE.put((lang, rss))

# extract all xml data
for i in range(THREAD_LIMIT):
    t = threading.Thread(target=news)
    t.start()
    THREADS.append(t)

for thread in THREADS:
    thread.join()

logging.debug("Done extracting all root urls")

# process all latest feed
for i in range(len(THREADS)):
    THREADS[i] = threading.Thread(target=extract_feed_data)
    THREADS[i].start()

for thread in THREADS:
    thread.join()

logging.debug("Done extracting all feed data")

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
