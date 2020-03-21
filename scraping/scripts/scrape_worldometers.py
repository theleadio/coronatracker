import os
import sys
import logging

# Connect to db_connector from parent directory
PARENT_DIR = ".."
CURRENT_DIR = os.path.dirname(
    os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__)))
)
sys.path.append(os.path.normpath(os.path.join(CURRENT_DIR, PARENT_DIR)))

from DatabaseConnector import db_worldometers_countries, db_worldometers_total_sum

import requests
from bs4 import BeautifulSoup
from datetime import datetime

TABLE = "test" # "prod"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
HEADER = {
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
}

db_worldometers_countries.connect()
db_worldometers_total_sum.connect()

# countries details
def get_worldometers_countries():
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
                text = text.replace('+', '').replace(',', '')
                if '.' in text:
                    country.append(float(text))
                else:
                    country.append(int(text))

        if len(country) == 9:
            if country[0] == 'Total:':
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
    countries_total_sum["last_updated"] = datetime.now().strftime(DATETIME_FORMAT)
    db_worldometers_total_sum.insert(countries_total_sum)

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
        country["last_updated"] = datetime.now().strftime(DATETIME_FORMAT)
        db_worldometers_countries.insert(country)
    print("Total countries: ", len(countries))
    print("Total Sum:", countries_total_sum)

if __name__ == "__main__":
    get_worldometers_countries()