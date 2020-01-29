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

import db_connector


NEWS_URLs = [
    "https://www.theage.com.au/rss/feed.xml",
    "https://www.theage.com.au/rss/world.xml",
    "http://www.heraldsun.com.au/news/breaking-news/rss",
    "http://www.heraldsun.com.au/rss",
    "https://www.news.com.au/content-feeds/latest-news-world/",
    "https://www.news.com.au/content-feeds/latest-news-national/",
    "http://www.dailytelegraph.com.au/news/breaking-news/rss",
    "http://www.dailytelegraph.com.au/news/national/rss",
    "http://www.dailytelegraph.com.au/newslocal/rss",
    "http://www.dailytelegraph.com.au/news/world/rss",
    "https://www.sbs.com.au/news/topic/latest/feed",
]

OUTPUT_FILENAME = "output.jsonl"
DATE_REGEX_RULE = (
    r"[\d]{1,2} [ADFJMNOS]\w* [\d]{4} \b(?:[01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]\b"
)
DATE_FORMAT = "%d %b %Y %H:%M:%S"
CORONA_KEYWORDS = set(["corona", "coronavirus"])
THREAD_LIMIT = 10

THREADS = []
XML_QUEUE = queue.Queue()
EXTRACT_FEED_QUEUE = queue.Queue()
RSS_STACK = []


def news():
    while not XML_QUEUE.empty():
        try:
            xml_news_url = XML_QUEUE.get()
            hdr = {"User-Agent": "Mozilla/5.0"}
            req = Request(xml_news_url, headers=hdr)
            parse_xml_url = urlopen(req)
            xml_page = parse_xml_url.read()
            parse_xml_url.close()

            soup_page = BeautifulSoup(xml_page, "xml")
            news_list = soup_page.findAll("item")

            for getfeed in news_list:
                EXTRACT_FEED_QUEUE.put((soup_page, getfeed))
        except queue.Empty:
            break


def extract_feed_data():
    while not EXTRACT_FEED_QUEUE.empty():
        try:
            soup_page, feed_source = EXTRACT_FEED_QUEUE.get()

            res_title = feed_source.title.text
            res_desc = feed_source.description.text

            # check if any of the CORONA_KEYWORDS occur in title or description
            if (
                len(set(res_title.lower().split()).intersection(CORONA_KEYWORDS)) == 0
                and len(set(res_desc.lower().split()).intersection(CORONA_KEYWORDS))
                == 0
            ):
                continue

            rss_record = {}
            rss_record["title"] = res_title
            rss_record["description"] = res_desc
            rss_record["url"] = feed_source.link.text

            # dd/mm/YY H:M:S
            dt_string = datetime.now().strftime("%d %b %Y %H:%M:%S")
            rss_record["addedOn"] = dt_string
            # rss_record["source"] = soup_page.channel.title.text

            article = extract_article(rss_record["url"])

            # Get language
            rss_record["language"] = (
                article.meta_lang if hasattr(article, "meta_lang") else None
            )

            # Get siteName
            rss_record["siteName"] = (
                article.source_url if hasattr(article, "source_url") else None
            )

            # Get the authors
            rss_record["author"] = (
                ", ".join(map(str, article.authors))
                if hasattr(article, "authors")
                else None
            )

            # Get the publish date
            if feed_source.pubDate:
                rss_record["publishedAt"] = date_convert(feed_source.pubDate.text)
            elif article.publish_date:
                rss_record["publishedAt"] = article.publish_date.strftime(DATE_FORMAT)
            elif soup_page.lastBuildDate:
                rss_record["publishedAt"] = date_convert(soup_page.lastBuildDate.text)
            else:
                rss_record["publishedAt"] = None

            # Get the article text
            # print(article.text)
            # Get a summary of the article
            # rss_record["summary"] = article.summary if hasattr(article, 'summary') else None
            rss_record["content"] = article.text if hasattr(article, "text") else None
            # Get the top image
            rss_record["urlToImage"] = (
                article.top_image if hasattr(article, "top_image") else None
            )
            # rss_record["images"] = article.images if hasattr(article, 'images') else None

            RSS_STACK.append(rss_record)
        except queue.Empty:
            break


def print_pretty():
    for rss_record in RSS_STACK:
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
    with open("output.jsonl", "w") as fh:
        for rss in RSS_STACK:
            print(rss)
            json.dump(rss, fh)
            fh.write("\n")


def save_to_db():
    db_connector.connect()
    for rss_record in RSS_STACK:
        db_connector.insert(rss_record)


def date_convert(date_string):
    if verbose:
        print("input date: " + date_string)
    all = re.findall(DATE_REGEX_RULE, date_string,)
    if len(all) > 0:
        datetime_str = all[0]
        datetime_object = datetime.strptime(datetime_str, DATE_FORMAT)
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
    parser.add_argument("-v", "--verbose", help="Verbose", default=False)
    parser.add_argument(
        "-o",
        "--output",
        help="Output result in json line format.",
        default=OUTPUT_FILENAME,
    )
    return parser.parse_args()


args = parser()
verbose = args.verbose
output = args.output

# place initial xml urls to queue
for rss in NEWS_URLs:
    XML_QUEUE.put(rss)

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

save_to_db()

if output:
    OUTPUT_FILENAME = output
    write_output()

if verbose:
    print_pretty()
if verbose:
    print("Total feeds: {}".format(len(RSS_STACK)))
