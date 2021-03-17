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
from ScrapeBingCovid.BingCovid import BingCovid

class Nation:
    def __init__(self, country,confirmed,deaths,recovered,last_update,lat,long):
       self.country=country
       self.confirmed=confirmed
       self.deaths=deaths
       self.recovered=recovered
       self.last_update=last_update
       self.lat=lat
       self.long=long

if __name__ == "__main__":
    db_bingcovid.connect()
    res = get_seed_page(API_URL).json()

    # whole world
    wholeWorld = BingCovid(
        confirmed=res["totalConfirmed"],
        deaths=res["totalDeaths"],
        recovered=res["totalRecovered"],
    )
    logging.debug("Inserting whole_world data: {}".format(wholeWorld.__dict__))
    db_bingcovid.insert(wholeWorld.__dict__, target_table=DB_TABLE)

    # Countries
     for area in res["areas"]:
         area=Nation(country,totalConfirmed,totalDeaths,totalRecovered,lastUpdated,lat,long)
         logging.debug("Inserting country data: {}".format(area.__dict__))
         db_bingcovid.insert(area.__dict__, target_table=DB_TABLE)

        # States
        for stateData in res["areas"]:
            currentState = BingCovid(
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
