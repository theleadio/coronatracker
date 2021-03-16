"""
To run:
- python scripts/scrape_worldometers.py --stats_table [ STATS TABLE NAME ] --overview_table [ OVERVIEW TABLE NAME ]
"""

import argparse
import os
import sys

# Connect to # db_connector from parent directory
PARENT_DIR = ".."
CURRENT_DIR = os.path.dirname(
    os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__)))
)
sys.path.append(os.path.normpath(os.path.join(CURRENT_DIR, PARENT_DIR)))

from scraping.DatabaseConnector.db_connector import DatabaseConnector

db_connector = DatabaseConnector(config_path="./db.json")
db_connector.connect()

# temporary solution as migrating to new db prod instance
db_connector_prodv2 = DatabaseConnector(config_path="./db.prodv2.json")
db_connector_prodv2.connect()

import requests
import pandas
from datetime import datetime

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
HEADER = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
}


def parser():
    parser = argparse.ArgumentParser(description="Scrape worldometers stats")
    parser.add_argument(
        "-s",
        "--stats_table",
        help="Database table name to write to.",
        default="worldometers_temp",
    )
    parser.add_argument(
        "-o",
        "--overview_table",
        help="Database table name to write to.",
        default="worldometers_total_sum_temp",
    )
    return parser.parse_args()


def cleanString(string):
    if not isinstance(string, str):
        return string
    return string.replace(",", "").replace("+", "")


def convertKeyAndWriteToDB(df, stats_table, overview_table):
    data = {}
    if df["Country,Other"] == "World":
        return
    if df["Country,Other"] != "Total:":
        data["country"] = df["Country,Other"]

    data["total_cases"] = int(cleanString(df["TotalCases"]))
    data["total_deaths"] = int(cleanString(df["TotalDeaths"]))
    data["total_recovered"] = int(cleanString(df["TotalRecovered"]))
    data["total_tests"] = int(cleanString(df["TotalTests"]))
    data["new_cases"] = int(cleanString(df["NewCases"]))
    data["new_deaths"] = int(cleanString(df["NewDeaths"]))
    data["active_cases"] = int(cleanString(df["ActiveCases"]))
    data["serious_critical_cases"] = int(cleanString(df["Serious,Critical"]))
    data["total_cases_per_million_pop"] = float(cleanString(df["Tot\xa0Cases/1M pop"]))
    data["total_deaths_per_million_pop"] = float(cleanString(df["Deaths/1M pop"]))
    data["total_tests_per_million_pop"] = float(cleanString(df["Tests/ 1M pop"]))
    data["last_updated"] = datetime.utcnow().strftime(DATETIME_FORMAT)

    if df["Country,Other"] != "Total:":
        db_connector.insert_worldometer_stats(data, stats_table)
        db_connector_prodv2.insert_worldometer_stats(data, stats_table)
    else:
        db_connector.insert_worldometers_total_sum(data, overview_table)
        db_connector_prodv2.insert_worldometers_total_sum(data, overview_table)


def scrape_world_meters(stats_table: str = "", overview_table: str = ""):
    if stats_table == "" or overview_table == "":
        args = parser()
    else:
        args = {"stats_table": stats_table, "overview_table": overview_table}

    url = "https://www.worldometers.info/coronavirus/"
    res = requests.get(url, headers=HEADER)
    df = pandas.read_html(res.content)
    df[0].fillna(0, inplace=True)
    df[0].apply(
        lambda dataframe: convertKeyAndWriteToDB(
            dataframe, args.stats_table, args.overview_table
        ),
        axis=1,
    )


if __name__ == "__main__":
    temp = parser()
    if temp:
        scrape_world_meters(temp.stats_table, temp.overview_table)
    else:
        scrape_world_meters()
