#!/usr/bin/env python3
#
# -*- coding: utf-8 -*-
#
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
from ScrapeBingCovid.bing_Covid import bing_Covid

if __name__ == "__main__":
    db_bingcovid.connect()
    res = get_seed_page(API_URL).json()

    # whole world
    wholeWorld = bing_Covid(
        confirmed=res["totalConfirmed"],
        deaths=res["totalDeaths"],
        recovered=res["totalRecovered"],
    )
    logging.debug("Inserting whole_world data: {}".format(wholeWorld.__dict__))
    db_bingcovid.insert(wholeWorld.__dict__, target_table=DB_TABLE)

    # Countries
    for countryData in res["areas"]:
        currentCountry = bing_Covid(
            confirmed=countryData["totalConfirmed"],
            deaths=countryData["totalDeaths"],
            recovered=countryData["totalRecovered"],
            last_update=countryData["lastUpdated"],
            lat=countryData["lat"],
            lng=countryData["long"],
            country=countryData["country"],
        )
        logging.debug("Inserting country data: {}".format(currentCountry.__dict__))
        db_bingcovid.insert(currentCountry.__dict__, target_table=DB_TABLE)

        # States
        for stateData in countryData["areas"]:
            currentState = bing_Covid(
                confirmed=stateData["totalConfirmed"],
                deaths=stateData["totalDeaths"],
                recovered=stateData["totalRecovered"],
                last_update=stateData["lastUpdated"],
                lat=stateData["lat"],
                lng=stateData["long"],
                state=stateData["displayName"],
                country=countryData["country"],
            )
            logging.debug("Inserting state data: {}".format(currentState.__dict__))
            db_bingcovid.insert(currentState.__dict__, target_table=DB_TABLE)
