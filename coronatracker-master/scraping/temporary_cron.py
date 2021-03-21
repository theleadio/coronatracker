#!/usr/bin/ python3

from sqlalchemy import create_engine
from sqlalchemy.sql import text
import pymysql

import json

path_to_json = 'db.json'

with open(path_to_json, "r") as handler:
    info = json.load(handler)


engine = create_engine("mysql+pymysql://{user}:{pw}@{host}:3306/{db}"
                       .format(user=info['user'],
                               pw=info['passwd'],
                               host=info['host'],
                               db=info['database']))


def sql_query(query_string):
    with engine.connect() as con:
        con.execute(query_string)


query_list = ['SET SQL_SAFE_UPDATES=0',
              "UPDATE newsapi_n SET publishedAt = DATE_SUB(publishedAt, INTERVAL 8 hour) WHERE publishedAt > CURRENT_TIMESTAMP() and siteName = 'news.cts.com.tw'",
              "UPDATE newsapi_n SET publishedAt = DATE_SUB(publishedAt, INTERVAL 8 hour) WHERE publishedAt > CURRENT_TIMESTAMP() and siteName = 'scmp.com'"]

for query_line in query_list:
    sql_query(query_line)
