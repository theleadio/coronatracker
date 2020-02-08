#!/usr/bin/ python3
# TO-DO:

# (Priority: High) Change INSERT IGNORE query to ON DUPLICATE KEY UPDATE
# (Priority: Low) Probably should write a user defined function for data parsing


# REFERENCES:
# Intro to web scraping: https://hackernoon.com/building-a-web-scraper-from-start-to-finish-bb6b95388184
# Intro to ingest data -> db: https://www.dataquest.io/blog/sql-insert-tutorial/
# Intro to setting up cron job: https://ole.michelsen.dk/blog/schedule-jobs-with-crontab-on-mac-osx.html
# About SQL INSERT IGNORE: https://chartio.com/resources/tutorials/how-to-insert-if-row-does-not-exist-upsert-in-mysql/
# About executing raw SQL with sqlalchemy: https://chartio.com/resources/tutorials/how-to-execute-raw-sql-in-sqlalchemy/
# Setting time to utc: https://stackabuse.com/converting-strings-to-datetime-in-python/
#                    : https://stackoverflow.com/questions/79797/how-to-convert-local-time-string-to-utc

########################################################################################


from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime, timezone
import pytz
from dateutil.parser import parse

from sqlalchemy import create_engine
from sqlalchemy.sql import text
import pymysql

import json
import os.path


DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

#########################
# Scrape job            #
#########################

# Url from main page
url = 'https://www.cna.com.tw/topic/newstopic/2012.aspx'
response = requests.get(url, timeout=5)
content = BeautifulSoup(response.content, "html.parser")


# Gather url of articles, separate links that point to article and cnavideo pages.
# If point to cnavideo page, need to redirect to sub-article page.
article_url = []
cnavideo_url = []
for title in content.find_all('a', {"class": "menuUrl"}):
    link = title.get('href')
    if 'cnavideo.cna.com.tw' in link:
        cnavideo_url.append(link)
    else:
        article_url.append(link)

for cnavideolink in cnavideo_url:
    vid_response = requests.get(cnavideolink, timeout=5)
    vid_content = BeautifulSoup(vid_response.content, "html.parser")
    # get link to sub-article page
    news_pointer = vid_content.find('div', {'class': 'comment more'}).find('a')

    if news_pointer is not None:
        article_url.append(news_pointer.get('href'))

unique_article_url = []
for x in article_url:
    if x not in unique_article_url:
        unique_article_url.append(x)

# empty list to collect newsObject for each url
newsObject_stack = []

# Filtering related news and extract information
for news in unique_article_url:
    news_response = requests.get(news, timeout=5)
    news_content = BeautifulSoup(news_response.content, "html.parser")

    keyword = ['武漢肺炎', '國家衛健委', '新型冠狀病毒', '口罩']
    # keyword translation: wuhan pneumonia, NHC, coronavirus, face mask

    article_keyword = news_content.find(
        'meta', {'name': 'keywords'}).get('content')
    # detect keyword, if present then extract information to dict
    if any(words in article_keyword for words in keyword):
       # language = news_content.find('html').get('lang')
        language = "zh_TW"

        # combining paragraphs of news article
        article_lines = []
        news_paragraphs = news_content.find(
            'div', {'class': 'paragraph'}).find_all('p')
        for line in news_paragraphs:
            article_lines.append(line.text)

        # reformat time to utc
        date_test = news_content.find(
            'meta', {"itemprop": 'datePublished'}).get('content')
        date_time_naive = parse(date_test)
        timezone = pytz.timezone('Asia/Taipei')
        tw_local_dt = timezone.localize(date_time_naive, is_dst=None)
        tw_utc_str = tw_local_dt.astimezone(pytz.utc).strftime(DATE_FORMAT)

        newsObject = {
            'title': news_content.find('article', {"class": "article"}).get('data-title'),
            'description': news_content.find('meta', {"name": "description"}).get('content'),
            'content': "".join(article_lines),
            'author': news_content.find('meta', {"itemprop": 'author'}).get('content'),
            'url': news,
            'urlToImage': news_content.find('link', {"rel": 'image_src'}).get('href'),
            'addedOn': datetime.utcnow().strftime(DATE_FORMAT),
            'publishedAt': tw_utc_str,
            'siteName': "cna.com.tw",
            'language': language,
            'countryCode': "TW"
            'status': '1'
        }

        newsObject_stack.append(newsObject)


df = pd.DataFrame(newsObject_stack)
# print(df.head())
# df.to_csv('tw_cna.csv')


#########################
# Send data to db       #
#########################

# Create sqlalchemy engine
# Obtain absolute path url to facilitate cron job
# fdir = os.path.abspath(os.path.dirname(__file__))
# path_to_json = os.path.join(fdir, 'db.json')
path_to_json = 'db.json'

with open(path_to_json, "r") as handler:
    info = json.load(handler)


engine = create_engine("mysql+pymysql://{user}:{pw}@{host}:3306/{db}"
                       .format(user=info['user'],
                               pw=info['passwd'],
                               host=info['host'],
                               db=info['database']))


# Insert whole DataFrame into MySQL, populate "tw_cna_news_temp" table
df.to_sql('tw_news_temp', con=engine, if_exists='append',
          chunksize=1000, index=False)
# df.to_sql('tw_cna_news_temp', con=engine, if_exists='replace',
#           chunksize=1000, index=False)


# Update "tw_cna_news" and "newsapi_n", clear "tw_cna_news_temp"
def sql_query(query_string):
    with engine.connect() as con:
        con.execute(query_string)


query_list = ['INSERT IGNORE INTO tw_news(title, description, author, url, content, urlToImage, publishedAt, addedOn, siteName, language, status) SELECT title, description, author, url, content, urlToImage, publishedAt, addedOn, siteName, language, status FROM tw_news_temp',
              'INSERT IGNORE INTO newsapi_n(title, description, author, url, content, urlToImage, publishedAt, addedOn, siteName, language, status) SELECT title, description, author, url, content, urlToImage, publishedAt, addedOn, siteName, language, status FROM tw_news',
              'SET SQL_SAFE_UPDATES=0',
              'DELETE FROM tw_news_temp']

for query_line in query_list:
    sql_query(query_line)
