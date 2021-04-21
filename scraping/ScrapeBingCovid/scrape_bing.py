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

#Iterator Pattern
class Iterator(Iterator):
    _position:int=None
    _reverse:bool=False

    def __init__(self,collection:AreasCollection,reverse:bool=False)->None:
        self._collection=collection
        self._reverse=reverse
        self._position=-1 if reverse else 0

    def __next__(self):
        try:
            value=self._collection[self._position]
            self._position+=-1 if self._reverse else 1
        except IndexError:
            raise StopIteration()
        return value

#collection class : areas
class AreasCollection(Iterable):
    def __init__(self,collection:List[Any]=[])->None:
        self._collection=collection

    def __iter__(self)->Iterator:
        return Iterator(self._collection)

    def get_reverse_iterator(self)->Iterator:
        return Iterator(self._collection,True)

    def add_item(self,item:Any):
        self._collection.append(item)

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
    for countryData in res["areas"]:
        currentCountry = BingCovid(
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
