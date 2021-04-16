import mysql.connector
import json
from abc import ABC, abstractmethod

#abstract class that bridges all of the databases
class DatabaseConnector(ABC):
     @abstractmethod
    def __init__(self, config_path="./"):
        self.mysql = None
        self.config_path = config_path

    def connect(self):
        with open(self.config_path, "r") as handler:
            info = json.load(handler)
            self.mydb = mysql.connector.connect(
                host=info["host"],
                user=info["user"],
                passwd=info["passwd"],
                database=info["database"],
            )
        print("Database connected: {}".format(info))

    def select(self):
        cursor = self.mydb.cursor()
        mycursor.execute("SELECT * FROM {}".format(TABLE_NAME))
        return cursor.fetchall()

#class for the connection of news data
class NewsDatabase(DatabaseConnector):

    def __init__ (self, data_dict, table_name)
        self.data_dict = data_dict
        self.table_name = table_name

    # NEWS TABLE_SCHEMA
    # ['nid', 'title', 'description', 'author', 'url', 'content', 'urlToImage', 'publishedAt', 'addedOn', 'siteName', 'language', 'countryCode', 'status']
    def insert_news_article(self):
        if not table_name:
            raise ValueError("db_connector insert_news_article missing table_name")
        self.table_name = table_name
        mycursor = self.mydb.cursor()
        sql = "INSERT INTO {} (title, description, author, url, content, urlToImage, publishedAt, addedOn, siteName, language, countryCode, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE title = %s, description = %s, author = %s, content = %s, urlToImage = %s, publishedAt = %s, addedOn = %s, siteName = %s, language = %s, countryCode = %s".format(
            table_name
        )
        val = (
            self.data_dict["title"],
            self.data_dict["description"],
            self.data_dict["author"],
            self.data_dict["url"],
            self.data_dict["content"],
            self.data_dict["urlToImage"],
            self.data_dict["publishedAt"],
            self.data_dict["addedOn"],
            self.data_dict["siteName"],
            self.data_dict["language"],
            self.data_dict["countryCode"],
            1,  # Status
            self.data_dict["title"],
            self.data_dict["description"],
            self.data_dict["author"],
            self.data_dict["content"],
            self.data_dict["urlToImage"],
            self.data_dict["publishedAt"],
            self.data_dict["addedOn"],
            self.data_dict["siteName"],
            self.data_dict["language"],
            self.data_dict["countryCode"],
        )
        print("SQL query: ", sql, val)
        try:
            mycursor.execute(sql, val)
            self.mydb.commit()
            print(mycursor.rowcount, "record inserted.")
        except Exception as ex:
            print(ex)
            print("Record not inserted")

#class for the connection of Worldometer data
class WorldometerStatsDatabase(DatabaseConnector):

    def __init__ (self, data_dict, table_name)
        self.data_dict = data_dict
        self.table_name = table_name

    # worldometers TABLE_SCHEMA
    # country, total_cases, total_deaths, total_recovered, total_tests, new_cases, new_deaths, active_cases, serious_critical_cases, total_cases_per_million_pop, total_tests_per_million_pop, last_updated
    def insert_worldometer_stats(self):
        if not table_name:
            raise ValueError("db_connector insert_worldometer missing table_name")
        self.table_name = table_name
        mycursor = self.mydb.cursor()
        sql = "INSERT INTO {} (country, total_cases, total_deaths, total_recovered, total_tests, new_cases, new_deaths, active_cases, serious_critical_cases, total_cases_per_million_pop, total_deaths_per_million_pop, total_tests_per_million_pop, last_updated) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE country = %s, total_cases = %s, total_deaths = %s, total_recovered = %s, total_tests = %s, new_cases = %s, new_deaths = %s, active_cases = %s, serious_critical_cases = %s, total_cases_per_million_pop = %s, total_deaths_per_million_pop = %s, total_tests_per_million_pop = %s".format(
            table_name
        )
        val = (
            self.data_dict["country"],
            self.data_dict["total_cases"],
            self.data_dict["total_deaths"],
            self.data_dict["total_recovered"],
            self.data_dict["total_tests"],
            self.data_dict["new_cases"],
            self.data_dict["new_deaths"],
            self.data_dict["active_cases"],
            self.data_dict["serious_critical_cases"],
            self.data_dict["total_cases_per_million_pop"],
            self.data_dict["total_deaths_per_million_pop"],
            self.data_dict["total_tests_per_million_pop"],
            self.data_dict["last_updated"],
            self.data_dict["country"],
            self.data_dict["total_cases"],
            self.data_dict["total_deaths"],
            self.data_dict["total_recovered"],
            self.data_dict["total_tests"],
            self.data_dict["new_cases"],
            self.data_dict["new_deaths"],
            self.data_dict["active_cases"],
            self.data_dict["serious_critical_cases"],
            self.data_dict["total_cases_per_million_pop"],
            self.data_dict["total_deaths_per_million_pop"],
            self.data_dict["total_tests_per_million_pop"],
        )
        print("SQL query: ", sql, val)
        try:
            mycursor.execute(sql, val)
            self.mydb.commit()
            print(mycursor.rowcount, "record inserted.")
        except Exception as ex:
            print(ex)
            print("Record not inserted")

#class for the connection of Worldometer SUM data
class WorldometerStatsSUMDatabase(DatabaseConnector):

    def __init__ (self, data_dict, table_name)
        self.data_dict = data_dict
        self.table_name = table_name            

    # worldometers_total_sum TABLE_SCHEMA
    # total_cases, total_deaths, total_recovered, total_tests, new_cases, new_deaths, active_cases, serious_critical_cases, total_cases_per_million_pop, total_deaths_per_million_pop, total_tests_per_million_pop, last_updated
    def insert_worldometers_total_sum(self):
        if not table_name:
            raise ValueError(
                "db_connector insert_worldometers_total_sum missing table_name"
            )
        self.table_name = table_name
        mycursor = self.mydb.cursor()
        sql = "INSERT INTO {} (total_cases, total_deaths, total_recovered, total_tests, new_cases, new_deaths, active_cases, serious_critical_cases, total_cases_per_million_pop, total_deaths_per_million_pop, total_tests_per_million_pop, last_updated) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE total_cases = %s, total_deaths = %s, total_recovered = %s, total_tests = %s, new_cases = %s, new_deaths = %s, active_cases = %s, serious_critical_cases = %s, total_cases_per_million_pop = %s, total_deaths_per_million_pop = %s, total_tests_per_million_pop = %s".format(
            table_name
        )
        val = (
            self.data_dict["total_cases"],
            self.data_dict["total_deaths"],
            self.data_dict["total_recovered"],
            self.data_dict["total_tests"],
            self.data_dict["new_cases"],
            self.data_dict["new_deaths"],
            self.data_dict["active_cases"],
            self.data_dict["serious_critical_cases"],
            self.data_dict["total_cases_per_million_pop"],
            self.data_dict["total_deaths_per_million_pop"],
            self.data_dict["total_tests_per_million_pop"],
            self.data_dict["last_updated"],
            self.data_dict["total_cases"],
            self.data_dict["total_deaths"],
            self.data_dict["total_recovered"],
            self.data_dict["total_tests"],
            self.data_dict["new_cases"],
            self.data_dict["new_deaths"],
            self.data_dict["active_cases"],
            self.data_dict["serious_critical_cases"],
            self.data_dict["total_cases_per_million_pop"],
            self.data_dict["total_deaths_per_million_pop"],
            self.data_dict["total_tests_per_million_pop"],
        )
        print("SQL query: ", sql, val)
        try:
            mycursor.execute(sql, val)
            self.mydb.commit()
            print(mycursor.rowcount, "record inserted.")
        except Exception as ex:
            print(ex)
            print("Record not inserted")


#class for the connection of BingCovid data
class BingCovidDatabase(DatabaseConnector):

    def __init__ (self, data_dict, table_name)
        self.data_dict = data_dict
        self.table_name = table_name   

# BING_COVID TABLE_SCHEMA
# ['nid', 'state', 'country', 'last_update', 'lat', 'lng', 'confirmed', 'deaths', 'recovered', 'posted_date']
    def insert_bing_covid(data_dict, target_table="test"):
        if not table_name:
            raise ValueError(
                "db_connector insert_worldometers_total_sum missing table_name"
            )
        self.table_name = table_name
        mycursor = self.mydb.cursor()
        sql = "INSERT INTO {} (state, country, last_update, lat, lng, confirmed, deaths, recovered, posted_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE state = %s, country = %s, confirmed = %s, deaths = %s, recovered = %s".format(
            table_name
    )
    val = (
        self.data_dict["state"],
        self.data_dict["country"],
        self.data_dict["last_update"],
        self.data_dict["lat"],
        self.data_dict["lng"],
        self.data_dict["confirmed"],
        self.data_dict["deaths"],
        self.data_dict["recovered"],
        self.data_dict["posted_date"],
        self.data_dict["state"],
        self.data_dict["country"],
        self.data_dict["confirmed"],
        self.data_dict["deaths"],
        self.data_dict["recovered"],
    )
    print("SQL query: ", sql, val)
    try:
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")
    except Exception as ex:
        print(ex)
        print("Record not inserted")
     
#class for the connection of Malaysia patient data
class MalaysiaPatientDatabase(DatabaseConnector):

    def __init__ (self, data_dict, table_name)
        self.data_dict = data_dict
        self.table_name = table_name   

# malaysia_patient_case TABLE_SCHEMA 
# case, status, status_date, confirmed_date, nationality, age, gender, hospital, description    
    def insert_malaysia_patient(data_dict, target_table="test"):
     if not table_name:
            raise ValueError(
                "db_connector insert_worldometers_total_sum missing table_name"
            )
        self.table_name = table_name
        mycursor = self.mydb.cursor()
        sql = "INSERT INTO {} (caseId, status, statusDate, confirmedDate, nationality, age, gender, hospital, description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE caseId = %s, status = %s, statusDate = %s, confirmedDate = %s, nationality = %s, age = %s, gender = %s, hospital = %s, description = %s".format(
            table_name
    )
    val = (
        self.data_dict["case"],
        self.data_dict["status"],
        self.data_dict["status_date"],
        self.data_dict["confirmed_date"],
        self.data_dict["nationality"],
        self.data_dict["age"],
        self.data_dict["gender"],
        self.data_dict["hospital"],
        self.data_dict["description"],
        self.data_dict["case"],
        self.data_dict["status"],
        self.data_dict["status_date"],
        self.data_dict["confirmed_date"],
        self.data_dict["nationality"],
        self.data_dict["age"],
        self.data_dict["gender"],
        self.data_dict["hospital"],
        self.data_dict["description"],
    )
    print("SQL query: ", sql, val)
    try:
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")
    except Exception as ex:
        print(ex)
        print("Record not inserted")

#class for the connection of Malaysia state data
class MalaysiaStatesDatabase(DatabaseConnector):

    def __init__ (self, data_dict, table_name)
        self.data_dict = data_dict
        self.table_name = table_name   

# malaysia_patient_case TABLE_SCHEMA
# case, status, status_date, confirmed_date, nationality, age, gender, hospital, description        
    def insert_malaysia_state(data_dict, target_table="test"):
    if not table_name:
            raise ValueError(
                "db_connector insert_worldometers_total_sum missing table_name"
            )
        self.table_name = table_name
        mycursor = self.mydb.cursor()
        sql = "INSERT INTO {} (state, increment_count, total_count, hospital_count, recovered_count, death_count, last_updated) VALUES (%s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE state = %s, increment_count = %s, total_count = %s, hospital_count = %s, recovered_count = %s, death_count = %s".format(
            table_name
    )
    val = (
        self.data_dict["state"],
        self.data_dict["increment_count"],
        self.data_dict["total_count"],
        self.data_dict["hospital_count"],
        self.data_dict["recovered_count"],
        self.data_dict["death_count"],
        self.data_dict["last_updated"],
        self.data_dict["state"],
        self.data_dict["increment_count"],
        self.data_dict["total_count"],
        self.data_dict["hospital_count"],
        self.data_dict["recovered_count"],
        self.data_dict["death_count"],
    )
    print("SQL query: ", sql, val)
    try:
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")
    except Exception as ex:
        print(ex)
        print("Record not inserted")
