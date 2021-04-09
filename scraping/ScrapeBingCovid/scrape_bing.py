#!/usr/bin/env python3
#
# -*- coding: utf-8 -*-
#
# Author(s):
#   - samueljklee@gmail.com
#

import sys
import os
import logging

# Connect to db_connector from parent directory
PARENT_DIR = ".."
CURRENT_DIR = os.path.dirname(
    os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__)))
)
sys.path.append(os.path.normpath(os.path.join(CURRENT_DIR, PARENT_DIR)))

from DatabaseConnector import db_bingcovid

DB_TABLE = "test"  # "prod"
API_URL = "https://bing.com/covid/data"

# ScrapeRss helper function
from ScrapeRss.helpers import get_seed_page

# BingCovid
import BingCovidBuilder

if __name__ == "__main__":
    db_bingcovid.connect()
    res = get_seed_page(API_URL).json()

    # whole world
    wholeWorld = BingCovidBuilder()\
            .add_confirmed(res["totalConfirmed"])\
            .add_deaths(res["totalDeaths"])\
            .add_recovered(res["totalRecovered"])\
            .build()
    logging.debug("Inserting whole_world data: {}".format(wholeWorld.__dict__))
    db_bingcovid.insert(wholeWorld.__dict__, target_table=DB_TABLE)

    # Countries
    for countryData in res["areas"]:
        currentCountry = BingCovidBuilder \
            .add_confirmed(confirmed=countryData["totalConfirmed"])\
            .add_deaths(countryData["totalDeaths"])\
            .add_recovered(countryData["totalRecovered"])\
            .add_last_update(countryData["lastUpdated"])\
            .add_lat(countryData["lat"])\
            .add_lng(countryData["long"])\
            .add_country(countryData["country"])\
            .build()
        logging.debug("Inserting country data: {}".format(currentCountry.__dict__))
        db_bingcovid.insert(currentCountry.__dict__, target_table=DB_TABLE)

        # States
        for stateData in countryData["areas"]:
            currentState = BingCovidBuilder()\
                .add_confirmed(stateData["totalConfirmed"])\
                .add_deaths(stateData["totalDeaths"])\
                .add_recovered(stateData["totalRecovered"])\
                .add_last_update(stateData["lastUpdated"])\
                .add_lat(stateData["lat"])\
                .add_lng(stateData["long"])\
                .add_state(stateData["displayName"])\
                .add_country(stateData["country"])\
                .build()
            logging.debug("Inserting state data: {}".format(currentState.__dict__))
            db_bingcovid.insert(currentState.__dict__, target_table=DB_TABLE)
