import mysql.connector
import json
import re

TABLES = {
    "BING": {
        "INSERT_TEST": "INSERT INTO bing_covid_temp (state, country, last_update, lat, lng, confirmed, deaths, recovered, posted_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE state = %s, country = %s, confirmed = %s, deaths = %s, recovered = %s",
        "INSERT_PROD": "INSERT INTO bing_covid (state, country, last_update, lat, lng, confirmed, deaths, recovered, posted_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE state = %s, country = %s, confirmed = %s, deaths = %s, recovered = %s"
    },
    "MALAYSIA": {
        "INSERT_TEST": "INSERT INTO malaysia_patient_case_temp (caseId, status, statusDate, confirmedDate, nationality, age, gender, hospital, description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE caseId = %s, status = %s, statusDate = %s, confirmedDate = %s, nationality = %s, age = %s, gender = %s, hospital = %s, description = %s",
        "INSERT_PROD": "INSERT INTO malaysia_patient_case (caseId, status, statusDate, confirmedDate, nationality, age, gender, hospital, description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE caseId = %s, status = %s, statusDate = %s, confirmedDate = %s, nationality = %s, age = %s, gender = %s, hospital = %s, description = %s"
    },
    "MALAYSIA_STATES": {
        "INSERT_TEST": "INSERT INTO malaysia_states_temp (state, increment_count, total_count, hospital_count, recovered_count, death_count, last_updated) VALUES (%s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE state = %s, increment_count = %s, total_count = %s, hospital_count = %s, recovered_count = %s, death_count = %s",
        "INSERT_PROD": "INSERT INTO malaysia_states (state, increment_count, total_count, hospital_count, recovered_count, death_count, last_updated) VALUES (%s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE state = %s, increment_count = %s, total_count = %s, hospital_count = %s, recovered_count = %s, death_count = %s",
    },
    "WEBSCRAPER": {
        "INSERT_TEST": "INSERT INTO newsapi_en (title, description, author, url, content, urlToImage, publishedAt, addedOn, siteName, language, countryCode, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE title = %s, description = %s, author = %s, content = %s, urlToImage = %s, publishedAt = %s, addedOn = %s, siteName = %s, language = %s, countryCode = %s",
        "INSERT_PROD": "INSERT INTO newsapi_n (title, description, author, url, content, urlToImage, publishedAt, addedOn, siteName, language, countryCode, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE title = %s, description = %s, author = %s, content = %s, urlToImage = %s, publishedAt = %s, addedOn = %s, siteName = %s, language = %s, countryCode = %s"
    },
    "WORLD": {
        "INSERT_TEST": "INSERT INTO worldometers (country, total_cases, total_deaths, total_recovered, total_tests, new_cases, new_deaths, active_cases, serious_critical_cases, total_cases_per_million_pop, total_deaths_per_million_pop, total_tests_per_million_pop, last_updated) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE country = %s, total_cases = %s, total_deaths = %s, total_recovered = %s, total_tests = %s, new_cases = %s, new_deaths = %s, active_cases = %s, serious_critical_cases = %s, total_cases_per_million_pop = %s, total_deaths_per_million_pop = %s, total_tests_per_million_pop = %s",
        "INSERT_PROD": "INSERT INTO worldometers (country, total_cases, total_deaths, total_recovered, total_tests, new_cases, new_deaths, active_cases, serious_critical_cases, total_cases_per_million_pop, total_deaths_per_million_pop, total_tests_per_million_pop, last_updated) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE country = %s, total_cases = %s, total_deaths = %s, total_recovered = %s, total_tests = %s, new_cases = %s, new_deaths = %s, active_cases = %s, serious_critical_cases = %s, total_cases_per_million_pop = %s, total_deaths_per_million_pop = %s, total_tests_per_million_pop = %s"
    },
    "WORLD_SUM": {
        "INSERT_TEST": "INSERT INTO worldometers_total_sum (total_cases, total_deaths, total_recovered, total_tests, new_cases, new_deaths, active_cases, serious_critical_cases, total_cases_per_million_pop, total_deaths_per_million_pop, total_tests_per_million_pop, last_updated) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE total_cases = %s, total_deaths = %s, total_recovered = %s, total_tests = %s, new_cases = %s, new_deaths = %s, active_cases = %s, serious_critical_cases = %s, total_cases_per_million_pop = %s, total_deaths_per_million_pop = %s, total_tests_per_million_pop = %s",
        "INSERT_PROD": "INSERT INTO worldometers_total_sum (total_cases, total_deaths, total_recovered, total_tests, new_cases, new_deaths, active_cases, serious_critical_cases, total_cases_per_million_pop, total_deaths_per_million_pop, total_tests_per_million_pop, last_updated) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE total_cases = %s, total_deaths = %s, total_recovered = %s, total_tests = %s, new_cases = %s, new_deaths = %s, active_cases = %s, serious_critical_cases = %s, total_cases_per_million_pop = %s, total_deaths_per_million_pop = %s, total_tests_per_million_pop = %s"
    },
    "NEWS": {
        "INSERT_TEST": "INSERT INTO news (title, description, author, url, content, urlToImage, publishedAt, addedOn, siteName, language, countryCode, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE title = %s, description = %s, author = %s, content = %s, urlToImage = %s, publishedAt = %s, addedOn = %s, siteName = %s, language = %s, countryCode = %s",
        "INSERT_TEST": "INSERT INTO news (title, description, author, url, content, urlToImage, publishedAt, addedOn, siteName, language, countryCode, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE title = %s, description = %s, author = %s, content = %s, urlToImage = %s, publishedAt = %s, addedOn = %s, siteName = %s, language = %s, countryCode = %s"
    }
}


class DbName:
    BING = "BING"
    MALAYSIA = "MALAYSIA"
    MALAYSIA_STATES = "MALAYSIA_STATES"
    WEBSCRAPER = "WEBSCRAPER"
    WORLD = "WORLD"
    WORLD_SUM = "WORLD_SUM"
    NEWS = "NEWS"


class DbConnection:
    """
    Represents a connection to any DB
    Automatically connects to DB on instance
    """

    __config_path = None
    __is_prod = None
    __source = None
    __mydb = None
    __my_cursor = None

    def __init__(self, source: str, is_prod: bool, config_path: str = "./db.json"):
        """
        :param source: A field from DbName
        :param is_prod: Whether or not the table insertion is PROD or TEST
        :param config_path: Optional, pass path of DB creds here
        """
        self.__config_path = config_path
        self.__is_prod = is_prod
        self.__source = source
        self.__connect()

    def __connect(self):
        with open(self.__config_path, "r") as handler:
            info = json.load(handler)
            self.__mydb = mysql.connector.connect(
                host=info["host"],
                user=info["user"],
                passwd=info["passwd"],
                database=info["database"],
            )
            self.__my_cursor = self.__mydb.cursor()
        print("Database connected: {}".format(info))

    def __get_table_name(self):
        match = re.search("INSERT INTO(.*?) \(", TABLES[self.__source]["TEST"]).group(0)
        if match:
            return match[11:len(match) - 1].strip()

    def select(self):
        table_name = self.__get_table_name()
        self.__my_cursor.execute("SELECT * FROM {}".format(table_name))
        myresult = self.__my_cursor.fetchall()
        for x in myresult:
            print(x)

    def insert(self, data_dict):
        self.__my_cursor = self.__mydb.cursor()
        if self.__is_prod:
            sql = TABLES[self.__source]["INSERT_PROD"]
        else:
            sql = TABLES[self.__source]["INSERT_TEST"]
        val = tuple(data_dict[key] for key in data_dict)

        try:
            self.__my_cursor.execute(sql, val)
            self.__mydb.commit()
            print(self.__my_cursor.rowcount, "record inserted.")
        except Exception as e:
            print(e)
            print("Record not inserted")

    def update(self, sql_statement):
        self.__my_cursor.execute(sql_statement)
