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


from datetime import datetime
from dateutil import parser
        

class CovidStats:
    def __init__(
        self,
        posted_date=datetime.utcnow()
    ):
        self.posted_date = posted_date

    def toMappingForm(self):
        return self.__dict__
    
class World:
    def __init__(
        self,
        confirmed = None,
        deaths = None,
        recovered = None,
        posted_date=datetime.utcnow()
    ):
        self.confirmed = confirmed
        self.deaths = deaths
        self.recovered = recovered
        self.posted_date = posted_date
    
    #function to return information for the whole world in dictionary form
    def wholeWorld_mapping(self):
        return self.toMappingForm()

class Country:
    def __init__(
        self,
        country=None,
        last_update=None,
        lat=None,
        lng=None,
        confirmed=None,
        deaths=None,
        recovered=None,
        posted_date=datetime.utcnow()
    ):
        self.confirmed = confirmed
        self.deaths = deaths
        self.recovered = recovered
        self.last_update = last_update
        self.lat = lat
        self.lng = lng
        self.country = country
        self.posted_date = posted_date

    #function to return information for the country in dictionary form
    def country_mapping(self):
        return self.toMappingForm()

class State:
    def __init__(
        self,
        state=None,
        country=None,
        last_update=None,
        lat=None,
        lng=None,
        confirmed=None,
        deaths=None,
        recovered=None,
        posted_date=datetime.utcnow()
    ):
        self.confirmed = confirmed
        self.deaths = deaths
        self.recovered = recovered
        self.last_update = last_update
        self.lat = lat
        self.lng = lng
        self.state = state
        self.country = country
        self.posted_date = posted_date
    
    #function to return information for the state in dictionary form
    def state_mapping(self):
        return self.toMappingForm()

        

if __name__ == "__main__":
    db_bingcovid.connect()
    res = get_seed_page(API_URL).json()

    # whole world
    wholeWorld = World(
        confirmed = res["totalConfirmed"],
        deaths = res["totalDeaths"],
        recovered = res["totalRecovered"],
    )
    logging.debug("Inserting whole_world data: {}".format(wholeWorld.wholeWorld_mapping()))
    db_bingcovid.insert(wholeWorld.wholeWorld_mapping(), target_table=DB_TABLE)

    # Countries
    for countryData in res["areas"]:
        currentCountry = Country(
            confirmed=countryData["totalConfirmed"],
            deaths=countryData["totalDeaths"],
            recovered=countryData["totalRecovered"],
            last_update=countryData["lastUpdated"],
            lat=countryData["lat"],
            lng=countryData["long"],
            country=countryData["country"],
        )
        logging.debug("Inserting country data: {}".format(currentCountry.country_mapping()))
        db_bingcovid.insert(currentCountry.counrty_mapping(), target_table=DB_TABLE)

        # States
        for stateData in countryData["areas"]:
            currentState = State(
                confirmed=stateData["totalConfirmed"],
                deaths=stateData["totalDeaths"],
                recovered=stateData["totalRecovered"],
                last_update=stateData["lastUpdated"],
                lat=stateData["lat"],
                lng=stateData["long"],
                state=stateData["displayName"],
                country=countryData["country"],
            )
            logging.debug("Inserting state data: {}".format(currentState.state_mapping()))
            db_bingcovid.insert(currentState.state_mapping(), target_table=DB_TABLE)
