
from abc import ABCMeta, abstractmethod

import requests
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
import mysql.connector
import json

from scraping.DatabaseConnector.db_malaysia_states import PROD_TABLE_NAME, TEST_TABLE_NAME
from scraping.webscraper import schema, connect, newsObject_stack, insert, TABLE_NAME


class IA(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def get_content(url):
        """method 1"""

    def extract_article(link):
        '''method 2'''

    def localtime_to_ust(datetime):
        '''method 3'''

    def connect(self):
        '''method 4'''

    def save_to_db(self):
        '''method 5'''

    def insert(data_dict):
        '''method 6'''

class webscraper(IA):
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

    def connect(self):
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

    def save_to_db(self):
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


class IB(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def connect(self):
        '''method 1'''

    def select(self):
        '''method 2'''

    def insert(data_dict, target_table="test"):
        '''method 3'''

class db_malaysia_states(IB):
    mydb = None
    TEST_TABLE_NAME = "malaysia_states_temp"
    PROD_TABLE_NAME = "malaysia_states"

    def connect(self):
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

    def select(self):
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM {}".format(TABLE_NAME))
        myresult = mycursor.fetchall()
        for x in myresult:
            print(x)

    def insert(data_dict, target_table="test"):
        table_name = PROD_TABLE_NAME if target_table == "prod" else TEST_TABLE_NAME
        mycursor = mydb.cursor()
        sql = "INSERT INTO {} (state, increment_count, total_count, hospital_count, recovered_count, death_count, last_updated) VALUES (%s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE state = %s, increment_count = %s, total_count = %s, hospital_count = %s, recovered_count = %s, death_count = %s".format(
            table_name
        )
        val = (
            data_dict["state"],
            data_dict["increment_count"],
            data_dict["total_count"],
            data_dict["hospital_count"],
            data_dict["recovered_count"],
            data_dict["death_count"],
            data_dict["last_updated"],
            data_dict["state"],
            data_dict["increment_count"],
            data_dict["total_count"],
            data_dict["hospital_count"],
            data_dict["recovered_count"],
            data_dict["death_count"],
        )
        print("SQL query: ", sql, val)
        try:
            mycursor.execute(sql, val)
            mydb.commit()
            print(mycursor.rowcount, "record inserted.")
        except Exception as ex:
            print(ex)
            print("Record not inserted")


"""Class db_malaysia_states does not have a methods of IA, so we create an adapter"""


class ClassAdapter(IA):
    def __init__(self):
        self.class_b = db_malaysia_states()

        def get_content(url):
            "calls class db_malaysia_states method select() instead"
            self.class_b.select()

        def connect(self):
            "calls class db_malaysia_states method connect() instead"
            self.class_b.connect()

        def insert(data_dict):
            "calls class db_malaysia_states method insert() instead"
            self.class_b.insert()

# user

#ITEM = webscraper()
#ITEM = db_malaysia_states.py()  # has no methods of webscraper
ITEM = ClassAdapter()


ITEM.get_content()

ITEM.connect()

ITEM.insert()
