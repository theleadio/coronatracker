#!/usr/bin/ python3

#from sqlalchemy import create_engine
#from sqlalchemy.sql import text
#import pymysql

from scraping.DatabaseConnector.mysql_connector import MySQL_Connector
from scraping.DatabaseConnector.table_queries import db_queries
import json

class TemporaryCorn():
    PATH_TO_JSON = 'db.json'

    query_list = ['SET SQL_SAFE_UPDATES=0',
                "UPDATE newsapi_n SET publishedAt = DATE_SUB(publishedAt, INTERVAL 8 hour) WHERE publishedAt > CURRENT_TIMESTAMP() and siteName = 'news.cts.com.tw'",
                "UPDATE newsapi_n SET publishedAt = DATE_SUB(publishedAt, INTERVAL 8 hour) WHERE publishedAt > CURRENT_TIMESTAMP() and siteName = 'scmp.com'"]

    def __init__(self):
        self.engine = MySQL_Connector(config_path=PATH_TO_JSON)

    def sql_query(self, query_string):
        self.engine.execute(query_string)



    def run_queries(self):
        for query_line in query_list:
            sql_query(query_line)
