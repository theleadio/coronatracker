#!/usr/bin/ python3
# TO-DO:

# REFERENCES:
# Intro to web scraping: https://hackernoon.com/building-a-web-scraper-from-start-to-finish-bb6b95388184
# Intro to ingest data -> db: https://www.dataquest.io/blog/sql-insert-tutorial/
# Intro to setting up cron job: https://ole.michelsen.dk/blog/schedule-jobs-with-crontab-on-mac-osx.html
# About SQL INSERT IGNORE: https://chartio.com/resources/tutorials/how-to-insert-if-row-does-not-exist-upsert-in-mysql/
# About executing raw SQL with sqlalchemy: https://chartio.com/resources/tutorials/how-to-execute-raw-sql-in-sqlalchemy/
# Setting time to utc: https://stackabuse.com/converting-strings-to-datetime-in-python/
#                    : https://stackoverflow.com/questions/79797/how-to-convert-local-time-string-to-utc
# How to find sitemap to get .xml: https://stackoverflow.com/questions/10232774/how-to-find-sitemap-xml-path-on-websites
# About exceptions: https://stackoverflow.com/questions/16511337/correct-way-to-try-except-using-python-requests-module/16511493
# Accessing into server: https://medium.com/@GalarnykMichael/aws-ec2-part-2-ssh-into-ec2-instance-c7879d47b6b2

########################################################################################


from bs4 import BeautifulSoup
from newspaper import Article
import requests
import pandas as pd
from datetime import datetime, timezone
import pytz
from dateutil.parser import parse
import re

import mysql.connector

import json
import os.path
import logging


mydb = None
TABLE_NAME = "newsapi_n"


def get_content(url):
    url = url
    try:
        response = requests.get(url, timeout=5)
        content = BeautifulSoup(response.content, "xml")
        # content = BeautifulSoup(response.content, "html.parser")
    except Exception:
        return None

    return content


def extract_article(link):
    logging.debug("Extracting from: {}".format(link))
    try:
        article = Article(link)
        # Do some NLP
        article.download()  # Downloads the link's HTML content
        article.parse()  # Parse the article
        article.nlp()  # Keyword extraction wrapper
    except Exception as e:
        logging.error("Fail to extract Article. Error: {}".format(e))
        return None, False

    return article, True


def localtime_to_ust(datetime):

    date_time_naive = parse(datetime)
    timezone = pytz.timezone(schema['timezone'])
    local_dt = timezone.localize(date_time_naive, is_dst=None)

    return local_dt


def connect():
    global mydb

    # populate this from env file
    path_to_json = "./db.json"

    with open(path_to_json, "r") as handler:
        info = json.load(handler)
        print(info)

        mydb = mysql.connector.connect(
            host=info["host"],
            user=info["user"],
            passwd=info["passwd"],
            database=info["database"],
        )

    print(mydb)


def save_to_db():
    connect()
    for newsObject in newsObject_stack:
        insert(newsObject)


def insert(data_dict):
    table_name = TABLE_NAME
    mycursor = mydb.cursor()
    sql = "INSERT INTO {} (title, description, author, url, content, urlToImage, publishedAt, addedOn, siteName, language, countryCode, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE title = %s, description = %s, author = %s, content = %s, urlToImage = %s, publishedAt = %s, addedOn = %s, siteName = %s, language = %s, countryCode = %s".format(
        table_name
    )
    val = (
        data_dict["title"],
        data_dict["description"],
        data_dict["author"],
        data_dict["url"],
        data_dict["content"],
        data_dict["urlToImage"],
        data_dict["publishedAt"],
        data_dict["addedOn"],
        data_dict["siteName"],
        data_dict["language"],
        data_dict["countryCode"],
        1,  # Status
        data_dict["title"],
        data_dict["description"],
        data_dict["author"],
        data_dict["content"],
        data_dict["urlToImage"],
        data_dict["publishedAt"],
        data_dict["addedOn"],
        data_dict["siteName"],
        data_dict["language"],
        data_dict["countryCode"],
    )
    print("SQL query: ", sql)
    try:
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")
    except Exception as ex:
        print(ex)
        print("Record not inserted")


DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
SPECIAL_LANG = set(["zh_TW", "zh_CN"])


key = ["新型コロナウイルス", "新型肺炎", "新型ウィルス", "武漢肺炎", "新型冠狀病毒"]
newsObject_stack = []

NEWS_URLs = {
    "ja_JP": [
        (
            "https://www3.nhk.or.jp/rss/news/cat0.xml",
            {"siteName": "www3.nhk.or.jp",
             "timezone": "Japan"}
        ),
        (
            "http://rss.asahi.com/rss/asahi/newsheadlines.rdf",
            {"siteName": "www.asahi.com"}
        )
    ],
    "zh_TW": [
        (
            "https://www.cna.com.tw/topic/newstopic/2012.aspx",
            {"siteName": "www.cna.com.tw",
             "timezone": "Asia/Taipei"}
        )
    ]

}


# Check language
for locale, all_rss in NEWS_URLs.items():
    for rss in all_rss:
        locale, root_url_schema = (locale, rss)
        root_url, schema = root_url_schema
        if schema['siteName'] == "www.cna.com.tw":
            site_links = get_content(root_url).findAll(
                'a', {"class": "menuUrl"})

        else:
            print(root_url)
            site_links_test = get_content(root_url)
            if site_links_test is None:
                continue
            else:
                site_links = site_links_test.findAll('link')

        links_container = []

        for link in site_links:
            if schema['siteName'] == "www.cna.com.tw":
                links_container.append(link.get("href"))

            else:
                links_container.append(link.text)

        for link in links_container:

            # Check if keywords or title matches key
            link_content = get_content(link)

            if not link_content is None:
                link_keywords_test = link_content.find(
                    'meta', {"name": "keywords"})
                link_title_test = link_content.find("title")

                if not link_keywords_test is None:
                    link_keywords = link_keywords_test.get("content")

                    if any(words in link_keywords for words in key):
                        link_title = link_title_test.text

                    elif not link_title_test is None:
                        link_title = link_title_test.text

                        if any(words in link_title for words in key):
                            pass

                        else:
                            continue

                    else:
                        continue

                else:
                    continue

            else:
                continue
            # Get title
            news_title = link_title

            # Get content
            article, status = extract_article(link)
            if not status:
                continue

            # Get author and format publishedAt
            if schema["siteName"] == "www3.nhk.or.jp":
                news_author = link_content.find(
                    'meta', {"name": 'author'}).get('content')

                date_string = link_content.find('time').get("datetime")
                local_dt = localtime_to_ust(date_string)

            elif schema["siteName"] == "www.asahi.com":
                news_author = link_content.find(
                    'meta', {"property": "og:site_name"}).get("content")

                date_string_test = link_content.find(
                    'meta', {"name": "pubdate"})
                if date_string_test == None:
                    continue
                else:
                    date_string = date_string_test.get("content")
                    local_dt = parse(date_string)

            elif schema["siteName"] == "www.cna.com.tw":
                news_author_test = link_content.find(
                    "meta", {"itemprop": "author"})
                if news_author_test == None:
                    continue
                news_author = news_author_test.get("content")
                date_string_test = link_content.find(
                    "meta", {"itemprop": "datePublished"})
                if date_string_test == None:
                    continue
                date_string = date_string_test.get("content")
                local_dt = localtime_to_ust(date_string)

            utc_str = local_dt.astimezone(pytz.utc).strftime(DATE_FORMAT)

            # Get language and country
            lang_locale = locale.split("_")
            lang = lang_locale[0]
            country = lang_locale[1]

            newsObject = {

                'title': news_title,
                'description': link_content.find('meta', {"name": "description"}).get('content'),
                'content': article.text,
                'author': news_author,
                'url': link,
                'urlToImage': article.top_image,
                'addedOn': datetime.utcnow().strftime(DATE_FORMAT),
                'publishedAt': utc_str,
                'siteName': schema['siteName'],
                'language': lang if locale not in SPECIAL_LANG else locale,
                'countryCode': country,
                'status': '1'
            }
            newsObject_stack.append(newsObject)


save_to_db()
# print(newsObject_stack)
from twitterscraper import query_tweets
import json
import datetime

if __name__ == '__main__':
    search_query = "WuhanVirus OR 2019nCoV OR Coronavirus OR WuhanCoronavirus OR coronaviruses OR coronavirusoutbreak OR coronavirus OR Covid-19 OR COVID-19 OR ChineseCoronavirus OR Coronaoutbreak"
    filename = "corona_twitter.json"
    #filename = "{}.json".format(username)

    tweets = query_tweets(query=search_query, begindate=datetime.date(2019, 12, 30), enddate=datetime.date(2020, 1, 27))
    print("Found: {} tweets".format(len(tweets)))

    j = []
    for t in tweets:
        t.timestamp = t.timestamp.isoformat()
        print("{} {} {} {} {}: {}".format(t.username, t.tweet_id, t.hashtags, t.links, t.timestamp, t.text))
        j.append(t.__dict__)

    with open(filename, "w") as f:
        f.write(json.dumps(j))

import sys
import os
import logging

# Connect to db_connector from parent directory
PARENT_DIR = ".."
CURRENT_DIR = os.path.dirname(
    os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__)))
)
sys.path.append(os.path.normpath(os.path.join(CURRENT_DIR, PARENT_DIR)))

from DatabaseConnector import db_bingcovid

DB_TABLE = "test"  # "prod"
API_URL = "https://bing.com/covid/data"

# ScrapeRss helper function
from ScrapeRss.helpers import get_seed_page

# BingCovid
from ScrapeBingCovid.BingCovid import BingCovid

if __name__ == "__main__":
    db_bingcovid.connect()
    res = get_seed_page(API_URL).json()

    # whole world
    wholeWorld = BingCovid(
        confirmed=res["totalConfirmed"],
        deaths=res["totalDeaths"],
        recovered=res["totalRecovered"],
    )
    logging.debug("Inserting whole_world data: {}".format(wholeWorld.__dict__))
    db_bingcovid.insert(wholeWorld.__dict__, target_table=DB_TABLE)

    # Countries
    for countryData in res["areas"]:
        currentCountry = BingCovid(
            confirmed=countryData["totalConfirmed"],
            deaths=countryData["totalDeaths"],
            recovered=countryData["totalRecovered"],
            last_update=countryData["lastUpdated"],
            lat=countryData["lat"],
            lng=countryData["long"],
            country=countryData["country"],
        )
        logging.debug("Inserting country data: {}".format(currentCountry.__dict__))
        db_bingcovid.insert(currentCountry.__dict__, target_table=DB_TABLE)

        # States
        for stateData in countryData["areas"]:
            currentState = BingCovid(
                confirmed=stateData["totalConfirmed"],
                deaths=stateData["totalDeaths"],
                recovered=stateData["totalRecovered"],
                last_update=stateData["lastUpdated"],
                lat=stateData["lat"],
                lng=stateData["long"],
                state=stateData["displayName"],
                country=countryData["country"],
            )
            logging.debug("Inserting state data: {}".format(currentState.__dict__))
            db_bingcovid.insert(currentState.__dict__, target_table=DB_TABLE)
