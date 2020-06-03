"""
To run:
- python scripts/scrape_worldometers.py --stats_table [ STATS TABLE NAME ] --overview_table [ OVERVIEW TABLE NAME ]
"""

import re
import os
import sys
import logging
import argparse

# Connect to # db_connector from parent directory
PARENT_DIR = ".."
CURRENT_DIR = os.path.dirname(
    os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__)))
)
sys.path.append(os.path.normpath(os.path.join(CURRENT_DIR, PARENT_DIR)))

from DatabaseConnector.db_connector import DatabaseConnector

db_connector = DatabaseConnector(config_path="./db.json")
db_connector.connect()

# temporary solution as migrating to new db prod instance
db_connector_prodv2 = DatabaseConnector(config_path="./db.prodv2.json")
db_connector_prodv2.connect()

import requests
import pandas
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from dateutil import parser

ORIG_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S+Z"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
HEADER = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
}
lastUpdatedDate = datetime.utcnow().strftime(DATETIME_FORMAT)


def arg_parser():
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
    s = string.replace(",", "").replace("+", "").strip()
    return 0 if s == "N/A" or not s else s


def convertSoupToData(row, map):
    temp = {}
    data = {}
    for idx, td in enumerate(row):
        temp[map[idx]] = td.text

    data["country"] = temp["Country,Other"]
    data["total_cases"] = int(cleanString(temp["TotalCases"]))
    data["total_deaths"] = int(cleanString(temp["TotalDeaths"]))
    data["total_recovered"] = int(cleanString(temp["TotalRecovered"]))
    data["total_tests"] = int(cleanString(temp["TotalTests"]))
    data["new_cases"] = int(cleanString(temp["NewCases"]))
    data["new_deaths"] = int(cleanString(temp["NewDeaths"]))
    data["active_cases"] = int(cleanString(temp["ActiveCases"]))
    data["serious_critical_cases"] = int(cleanString(temp["Serious,Critical"]))
    data["total_cases_per_million_pop"] = float(cleanString(temp["TotCases/1M pop"]))
    data["total_deaths_per_million_pop"] = float(cleanString(temp["Deaths/1M pop"]))
    data["total_tests_per_million_pop"] = float(cleanString(temp["Tests/1M pop"]))
    return data


if __name__ == "__main__":
    args = arg_parser()

    url = "https://www.worldometers.info/coronavirus/"
    res = requests.get(url, headers=HEADER)

    # Get last updated date
    lastUpdatedDateArray = re.findall(r"Last updated:\s+([A-Za-z0-9\s,:]+)", res.text)
    lastUpdatedDate = (
        parser.parse(lastUpdatedDateArray[0])
        .astimezone(timezone.utc)
        .strftime(DATETIME_FORMAT)
        if lastUpdatedDateArray
        else lastUpdatedDate
    )

    # Find tables
    match_tables = re.findall(
        r"(<table[^>]*>(?:.|\n)+?(?=<\/table>)<\/table>)", res.text
    )
    if not match_tables:
        raise ValueError("No match tables")

    # Convert to BS4
    soup = BeautifulSoup(match_tables[0].strip(), "html.parser")

    # Remove unnecessary rows
    for tr in soup.findAll(
        "tr", {"class": "total_row_world row_continent", "class": "total_row_world"}
    ):
        tr.decompose()

    headerMapping = {}
    for idx, tr in enumerate(soup("tr")):
        if tr is None:
            continue

        if tr("th"):
            for idx, td in enumerate(tr("th")):
                headerMapping[idx] = td.text.replace("\xa0", "").replace("\n", "")
            continue

        data = convertSoupToData(tr("td"), headerMapping)
        data["last_updated"] = lastUpdatedDate

        if data["country"] == "Total:":
            del data["country"]
            db_connector.insert_worldometers_total_sum(data, args.overview_table)
            db_connector_prodv2.insert_worldometers_total_sum(data, args.overview_table)
        else:
            db_connector.insert_worldometer_stats(data, args.stats_table)
            db_connector_prodv2.insert_worldometer_stats(data, args.stats_table)
