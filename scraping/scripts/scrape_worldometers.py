"""
To run:
- python scripts/scrape_worldometers.py --stats_table [ STATS TABLE NAME ] --overview_table [ OVERVIEW TABLE NAME ]
"""

import os
import sys
import logging
import argparse

# Connect to db_connector from parent directory
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
from bs4 import BeautifulSoup
from datetime import datetime

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
HEADER = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
}

# countries details
def get_worldometers_countries(stats_table, overview_table):
    url = "https://www.worldometers.info/coronavirus/"
    print("Scraping", url)
    res = requests.get(url, headers=HEADER)
    page = BeautifulSoup(res.content, "html.parser")
    tables = page.find("table", {"id": "main_table_countries_today"})
    tbody = tables.find("tbody")
    row = tbody.find("tr")
    col = row.find(["td"])

    countries = []
    country = []
    countries_total_sum_raw = []
    while col:
        text = col.get_text().strip()

        if not text:
            country.append(0)
        else:
            if not country:
                country.append(text)
            else:
                text = text.replace("+", "").replace(",", "")
                if "." in text:
                    country.append(float(text))
                elif len(country) == 10:
                    country.append(text)
                else:
                    country.append(int(text))

        if len(country) == 11:
            if country[0] == "Total:":
                countries_total_sum_raw = country[:]
                break
            else:
                countries.append(country)
                country = []
        col = col.findNext(["td"])

    # Inserting
    countries_total_sum = {}
    countries_total_sum["total_cases"] = countries_total_sum_raw[1]
    countries_total_sum["total_deaths"] = countries_total_sum_raw[3]
    countries_total_sum["total_recovered"] = countries_total_sum_raw[5]
    countries_total_sum["new_cases"] = countries_total_sum_raw[2]
    countries_total_sum["new_deaths"] = countries_total_sum_raw[4]
    countries_total_sum["active_cases"] = countries_total_sum_raw[6]
    countries_total_sum["serious_critical_cases"] = countries_total_sum_raw[7]
    countries_total_sum["total_cases_per_million_pop"] = countries_total_sum_raw[8]
    countries_total_sum["total_deaths_per_million_pop"] = countries_total_sum_raw[9]
    countries_total_sum["last_updated"] = datetime.utcnow().strftime(DATETIME_FORMAT)
    db_connector.insert_worldometers_total_sum(countries_total_sum, overview_table)
    db_connector_prodv2.insert_worldometers_total_sum(
        countries_total_sum, overview_table
    )

    for country_raw in countries:
        country = {}
        country["country"] = country_raw[0]
        country["total_cases"] = country_raw[1]
        country["total_deaths"] = country_raw[3]
        country["total_recovered"] = country_raw[5]
        country["new_cases"] = country_raw[2]
        country["new_deaths"] = country_raw[4]
        country["active_cases"] = country_raw[6]
        country["serious_critical_cases"] = country_raw[7]
        country["total_cases_per_million_pop"] = country_raw[8]
        country["total_deaths_per_million_pop"] = country_raw[9]
        country["last_updated"] = datetime.utcnow().strftime(DATETIME_FORMAT)
        db_connector.insert_worldometer_stats(country, stats_table)
        db_connector_prodv2.insert_worldometer_stats(country, stats_table)
    print("Total countries: ", len(countries))
    print("Total Sum:", countries_total_sum)


def parser():
    parser = argparse.ArgumentParser(description="Scrape XML sources")
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


if __name__ == "__main__":
    args = parser()

    get_worldometers_countries(args.stats_table, args.overview_table)
