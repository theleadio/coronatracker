#!/usr/bin/env python3
#
# dipto.pratyaksa@carltondigital.com.au
# 26/1/2020
#
# REF:
# https://santhoshveer.com/rss-feed-reader-using-python/
# https://medium.com/@ankurjain_79625/how-did-i-scrape-news-article-using-python-6eff936b3c8c
# https://medium.com/@randerson112358/scrape-summarize-news-articles-using-python-51a48af1b4e2
#
# TO DO:
# Store the relevant RSS feed into shared repo, like Google sheet
# Algo to extract the casualty stats from linked news article

from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from datetime import datetime
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

"""
https://www.theage.com.au/rss/feed.xml
https://www.theage.com.au/rss/world.xml
http://www.heraldsun.com.au/news/breaking-news/rss
http://www.heraldsun.com.au/rss
https://www.news.com.au/content-feeds/latest-news-world/
https://www.news.com.au/content-feeds/latest-news-national/
http://www.dailytelegraph.com.au/news/breaking-news/rss
http://www.dailytelegraph.com.au/news/national/rss
http://www.dailytelegraph.com.au/newslocal/rss
http://www.dailytelegraph.com.au/news/world/rss
https://www.sbs.com.au/news/topic/latest/feed
https://www.channelnewsasia.com/googlenews/cna_news_sitemap.xml
"""

NEWS_URLs = {
    "en": [
        (
            "https://www.theage.com.au/rss/feed.xml",
            {"title": "title", "description": "description", "url": "link",},
        ),
        (
            "https://www.theage.com.au/rss/world.xml",
            {"title": "title", "description": "description", "url": "link",},
        ),
        (
            "http://www.heraldsun.com.au/news/breaking-news/rss",
            {"title": "title", "description": "description", "url": "link",},
        ),
        (
            "http://www.heraldsun.com.au/rss",
            {"title": "title", "description": "description", "url": "link",},
        ),
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
            {"title": "title", "description": "news:keywords", "url": "loc",},
        ),
    ]
}

OUTPUT_FILENAME = "output.jsonl"
DATE_REGEX_RULE = (
    r"[\d]{1,2} [ADFJMNOS]\w* [\d]{4} \b(?:[01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]\b"
)
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
CORONA_KEYWORDS = set(["corona", "coronavirus"])
THREAD_LIMIT = 10

THREADS = []
XML_QUEUE = queue.Queue()
EXTRACT_FEED_QUEUE = queue.Queue()
RSS_STACK = {}


def news():
    while not XML_QUEUE.empty():
        try:
            lang, root_url_schema = XML_QUEUE.get()
            root_url, schema = root_url_schema
            hdr = {"User-Agent": "Mozilla/5.0"}
            req = Request(root_url, headers=hdr)
            parse_xml_url = urlopen(req)
            xml_page = parse_xml_url.read()
            parse_xml_url.close()

            soup_page = BeautifulSoup(xml_page, "xml")
            news_list = soup_page.findAll("item")

            if not news_list:
                news_list = soup_page.findAll("url")

            for getfeed in news_list:
                EXTRACT_FEED_QUEUE.put((lang, root_url, soup_page, getfeed, schema))
        except queue.Empty:
            break


def extract_feed_data():
    while not EXTRACT_FEED_QUEUE.empty():
        try:
            lang, root_url, soup_page, feed_source, schema = EXTRACT_FEED_QUEUE.get()

            res_title = feed_source.find(schema["title"]).text
            res_desc = feed_source.find(schema["description"]).text

            # check if any of the CORONA_KEYWORDS occur in title or description
            if (
                len(
                    set(re.findall(r"\w+", res_title.lower())).intersection(
                        CORONA_KEYWORDS
                    )
                )
                == 0
                and len(
                    set(re.findall(r"\w+", res_desc.lower())).intersection(
                        CORONA_KEYWORDS
                    )
                )
                == 0
            ):
                continue

            rss_record = {}
            rss_record["title"] = res_title
            rss_record["description"] = res_desc
            rss_record["url"] = feed_source.find(schema["url"]).text

            # dd/mm/YY H:M:S
            dt_string = datetime.now().strftime(DATE_FORMAT)
            rss_record["addedOn"] = dt_string
            # rss_record["source"] = soup_page.channel.title.text

            article = extract_article(rss_record["url"])

            # Get language
            rss_record["language"] = article.meta_lang

            # Get siteName
            rss_record["siteName"] = re.sub(r"https?://(www\.)?","", article.source_url)

            # Get the authors
            rss_record["author"] = ", ".join(article.authors)

            # Get the publish date
            if feed_source.pubDate:
                rss_record["publishedAt"] = date_convert(feed_source.pubDate.text)
            elif article.publish_date:
                rss_record["publishedAt"] = article.publish_date.strftime(DATE_FORMAT)
            elif soup_page.lastBuildDate:
                rss_record["publishedAt"] = date_convert(soup_page.lastBuildDate.text)
            else:
                rss_record["publishedAt"] = ""

            rss_record["content"] = article.text
            # Get the top image
            rss_record["urlToImage"] = article.top_image

            if lang not in RSS_STACK:
                RSS_STACK[lang] = []
            RSS_STACK[lang].append(rss_record)
        except queue.Empty:
            break


def print_pretty():
    for lang, rss in RSS_STACK.items():
        for rss_record in rss:
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
                # to_print  = str(to_print , encoding='utf-8', errors = 'ignore')
                if verbose:
                    print(to_print.expandtabs())
            except:
                pass


def write_output():
    for lang, rss in RSS_STACK.items():
        with open("data/{}/output.jsonl".format(lang), "w") as fh:
            for rss_record in rss:
                json.dump(rss_record, fh)
                fh.write("\n")


def save_to_db():
    db_connector.connect()
    for lang, rss_record in RSS_STACK.items():
        db_connector.insert(rss_record)


def date_convert(date_string):
    if verbose:
        print("input date: " + date_string)
    all = re.findall(DATE_REGEX_RULE, date_string,)
    if len(all) > 0:
        datetime_str = all[0]
        datetime_object = datetime.strptime(datetime_str, "%d %b %Y %H:%M:%S").strftime(DATE_FORMAT)
    else:
        datetime_object = date_string
    if verbose:
        print(datetime_object, datetime_str, date_string)
    return str(datetime_object)


def extract_article(link):
    if verbose:
        print("Extracting from: ", link)
    article = Article(link)
    # Do some NLP
    article.download()  # Downloads the link’s HTML content
    article.parse()  # Parse the article
    nltk.download("punkt")  # 1 time download of the sentence tokenizer
    article.nlp()  #  Keyword extraction wrapper
    return article


def parser():
    parser = argparse.ArgumentParser(description="Scrape XML sources")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose")
    return parser.parse_args()


# arguments
args = parser()
verbose = args.verbose

# create required folders
if not os.path.isdir("data"):
    os.mkdir("./data")

# place initial xml urls to queue
for lang, all_rss in NEWS_URLs.items():
    if not os.path.isdir("./data/{}".format(lang)):
        os.mkdir("./data/{}".format(lang))
    for rss in all_rss:
        XML_QUEUE.put((lang, rss))

# extract all xml data
for i in range(THREAD_LIMIT):
    t = threading.Thread(target=news)
    t.start()
    THREADS.append(t)

for thread in THREADS:
    thread.join()

# process all latest feed
for i in range(len(THREADS)):
    THREADS[i] = threading.Thread(target=extract_feed_data)
    THREADS[i].start()

for thread in THREADS:
    thread.join()

# Store to DB
save_to_db()

# Write to json file
write_output()

if verbose:
    print_pretty()
if verbose:
    count = 0
    for lang, RSS in RSS_STACK.items():
        count += len(RSS)
    print("Total feeds: {}".format(count))
