from __future__ import annotations
import mysql.connector
import json
from abc import ABC, abstractmethod


class DatabaseConnector:
    _current_state = None

    def __init__(self, state: AbstractState, config_path="./"):
        self.transition(state)
        self.mysql = None
        self.config_path = config_path
        self.mydb = mysql.connector

    def connect(self):
        with open(self.config_path, "r") as handler:
            info = json.load(handler)
            self.mydb.connect(host=info["host"], user=info["user"], passwd=info["passwd"], database=info["database"])
        print("Database connected: {}".format(info))

    def transition(self, table_name):
        state_dict = {"newsapi-n": NewsArticle(),
                      "rss_record": NewsArticle(),
                      "stats_table": WorldometerStats(),
                      "overview_table": WorldometerOverview()}
        self._current_state = state_dict[table_name]
        self._current_state.databaseConnector = self

    def select(self, table_name):
        self.transition(table_name)
        self._current_state.abstract_select(table_name)

    def insert(self, data_dict, table_name):
        self.transition(table_name)
        self._current_state.abstract_insert(data_dict, table_name)


class AbstractState(ABC):
    @property
    def databaseConnector(self) -> DatabaseConnector:
        return self._databaseConnector

    @databaseConnector.setter
    def databaseConnector(self, databaseConnector: DatabaseConnector) -> None:
        self._databaseConnector = databaseConnector

    @abstractmethod
    def abstract_select(self, table_name) -> None:
        pass

    @abstractmethod
    def abstract_insert(self, data_dict, table_name) -> None:
        pass


class NewsArticle(AbstractState):

    def abstract_select(self, table_name) -> None:
        cursor = self.mydb.cursor()
        mycursor.execute("SELECT * FROM {}".format(table_name))
        return cursor.fetchall()

    # NEWS TABLE_SCHEMA
    # ['nid', 'title', 'description', 'author', 'url', 'content', 'urlToImage', 'publishedAt', 'addedOn', 'siteName', 'language', 'countryCode', 'status']
    def abstract_insert(self, data_dict, table_name) -> None:
        mycursor = self.mydb.cursor()
        sql = "INSERT INTO newsapi-n (title, description, author, url, content, urlToImage, publishedAt, addedOn, " \
              "siteName, language, countryCode, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
              "%s) ON DUPLICATE KEY UPDATE title = %s, description = %s, author = %s, content = %s, urlToImage = %s, " \
              "publishedAt = %s, addedOn = %s, siteName = %s, language = %s, countryCode = %s "
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
        print("SQL query: ", sql, val)
        try:
            mycursor.execute(sql, val)
            self.mydb.commit()
            print(mycursor.rowcount, "record inserted.")
        except Exception as ex:
            print(ex)
            print("Record not inserted")


class WorldometerStats(AbstractState):

    def abstract_select(self, table_name) -> None:
        cursor = self.mydb.cursor()
        mycursor.execute("SELECT * FROM {}".format(table_name))
        return cursor.fetchall()


    # worldometers TABLE_SCHEMA
    # country, total_cases, total_deaths, total_recovered, total_tests, new_cases, new_deaths, active_cases, serious_critical_cases, total_cases_per_million_pop, total_tests_per_million_pop, last_updated
    def abstract_insert(self, data_dict, table_name) -> None:
        mycursor = self.mydb.cursor()
        sql = "INSERT INTO stats_table (country, total_cases, total_deaths, total_recovered, total_tests, new_cases, new_deaths, active_cases, serious_critical_cases, total_cases_per_million_pop, total_deaths_per_million_pop, total_tests_per_million_pop, last_updated) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE country = %s, total_cases = %s, total_deaths = %s, total_recovered = %s, total_tests = %s, new_cases = %s, new_deaths = %s, active_cases = %s, serious_critical_cases = %s, total_cases_per_million_pop = %s, total_deaths_per_million_pop = %s, total_tests_per_million_pop = %s"
        val = (
            data_dict["country"],
            data_dict["total_cases"],
            data_dict["total_deaths"],
            data_dict["total_recovered"],
            data_dict["total_tests"],
            data_dict["new_cases"],
            data_dict["new_deaths"],
            data_dict["active_cases"],
            data_dict["serious_critical_cases"],
            data_dict["total_cases_per_million_pop"],
            data_dict["total_deaths_per_million_pop"],
            data_dict["total_tests_per_million_pop"],
            data_dict["last_updated"],
            data_dict["country"],
            data_dict["total_cases"],
            data_dict["total_deaths"],
            data_dict["total_recovered"],
            data_dict["total_tests"],
            data_dict["new_cases"],
            data_dict["new_deaths"],
            data_dict["active_cases"],
            data_dict["serious_critical_cases"],
            data_dict["total_cases_per_million_pop"],
            data_dict["total_deaths_per_million_pop"],
            data_dict["total_tests_per_million_pop"],
        )
        print("SQL query: ", sql, val)
        try:
            mycursor.execute(sql, val)
            self.mydb.commit()
            print(mycursor.rowcount, "record inserted.")
        except Exception as ex:
            print(ex)
            print("Record not inserted")


class WorldometerOverview(AbstractState):

    def abstract_select(self, table_name) -> None:
        cursor = self.mydb.cursor()
        mycursor.execute("SELECT * FROM {}".format(table_name))
        return cursor.fetchall()

    # worldometers_total_sum TABLE_SCHEMA
    # total_cases, total_deaths, total_recovered, total_tests, new_cases, new_deaths, active_cases, serious_critical_cases, total_cases_per_million_pop, total_deaths_per_million_pop, total_tests_per_million_pop, last_updated
    def abstract_insert(self, data_dict, table_name) -> None:
        mycursor = self.mydb.cursor()
        sql = "INSERT INTO overview_table (total_cases, total_deaths, total_recovered, total_tests, new_cases, " \
              "new_deaths, active_cases, serious_critical_cases, total_cases_per_million_pop, " \
              "total_deaths_per_million_pop, total_tests_per_million_pop, last_updated) VALUES (%s, %s, %s, %s, %s, " \
              "%s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE total_cases = %s, total_deaths = %s, " \
              "total_recovered = %s, total_tests = %s, new_cases = %s, new_deaths = %s, active_cases = %s, " \
              "serious_critical_cases = %s, total_cases_per_million_pop = %s, total_deaths_per_million_pop = %s, " \
              "total_tests_per_million_pop = %s "
        val = (
            data_dict["total_cases"],
            data_dict["total_deaths"],
            data_dict["total_recovered"],
            data_dict["total_tests"],
            data_dict["new_cases"],
            data_dict["new_deaths"],
            data_dict["active_cases"],
            data_dict["serious_critical_cases"],
            data_dict["total_cases_per_million_pop"],
            data_dict["total_deaths_per_million_pop"],
            data_dict["total_tests_per_million_pop"],
            data_dict["last_updated"],
            data_dict["total_cases"],
            data_dict["total_deaths"],
            data_dict["total_recovered"],
            data_dict["total_tests"],
            data_dict["new_cases"],
            data_dict["new_deaths"],
            data_dict["active_cases"],
            data_dict["serious_critical_cases"],
            data_dict["total_cases_per_million_pop"],
            data_dict["total_deaths_per_million_pop"],
            data_dict["total_tests_per_million_pop"],
        )
        print("SQL query: ", sql, val)
        try:
            mycursor.execute(sql, val)
            self.mydb.commit()
            print(mycursor.rowcount, "record inserted.")
        except Exception as ex:
            print(ex)
            print("Record not inserted")

