# TO-DO:
# [DONE] Set keyword to detect ’武漢肺炎‘(wuhan pneumonia),‘國家衛健委’(NHC),‘新型冠狀病毒’(coronavirus) at news article page
# [DONE] Debug Non-Type Error (1. hyperlinks within paragraphs; 2. cnavideo link to article)
# [DONE] Connect to db
# (Priority: Low) Probably should write a user defined function for data parsing
# (Priority: High) Finalise SQL table [no primary key, how to deal with duplicates?]


# REFERENCES:
# Intro to web scraping: https://hackernoon.com/building-a-web-scraper-from-start-to-finish-bb6b95388184
# Intro to ingest data -> db: https://www.dataquest.io/blog/sql-insert-tutorial/

########################################################################################

from bs4 import BeautifulSoup
import requests
import pandas as pd
from sqlalchemy import create_engine
import pymysql
import json


# url from main page
url = 'https://www.cna.com.tw/news/ahel/202001215004.aspx'
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


# empty list to collect newsObject for each url
newsObject_stack = []

# filtering related news and extract information
for news in article_url:
    news_response = requests.get(news, timeout=5)
    news_content = BeautifulSoup(news_response.content, "html.parser")

    keyword = ['武漢肺炎', '國家衛健委', '新型冠狀病毒', '口罩']
    # keyword translation: wuhan pneumonia, NHC, coronavirus, face mask

    article_keyword = news_content.find(
        'meta', {'name': 'keywords'}).get('content')
    # detect keyword, if present then extract information to dict
    if any(words in article_keyword for words in keyword):

        # combining paragraphs of news article
        article_lines = []
        news_paragraphs = news_content.find(
            'div', {'class': 'paragraph'}).find_all('p')
        for line in news_paragraphs:
            article_lines.append(line.text)

        newsObject = {
            'title': news_content.find('article', {"class": "article"}).get('data-title'),
            'description': news_content.find('meta', {"name": "description"}).get('content'),
            'content': "".join(article_lines),
            'author': news_content.find('meta', {"itemprop": 'author'}).get('content'),
            'url': news,
            'urlToImage': news_content.find('link', {"rel": 'image_src'}).get('href'),
            'publishedAt': news_content.find('meta', {"itemprop": 'datePublished'}).get('content'),
            'siteName': "cna.com.tw",
            'language': "zh_trad"
        }

        newsObject_stack.append(newsObject)


df = pd.DataFrame(newsObject_stack)
# print(df.head())
# df.to_csv('tw_cna.csv')


# create sqlalchemy engine
path_to_json = "./db.json"

with open(path_to_json, "r") as handler:
    info = json.load(handler)


engine = create_engine("mysql+pymysql://{user}:{pw}@{host}:3306/{db}"
                       .format(user=info['user'],
                               pw=info['passwd'],
                               host=info['host'],
                               db=info['database']))


# Insert whole DataFrame into MySQL
df.to_sql('tw_cna_news', con=engine, if_exists='append',
          chunksize=1000, index=False)
