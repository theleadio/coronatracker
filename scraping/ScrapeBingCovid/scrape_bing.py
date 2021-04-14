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



"Creational (Builder) Design Pattern Code"
from abc import ABCMETA, abstractmethod

class ICovidBuilder(metaclass=ABCMeta):
    "The IBuilder Interface"

    @staticmethod
    @abstractmethod
    def set_number_confirmed(self, value):
    """Set the confirmed number of cases"""


    @staticmethod
    @abstractmethod
     def set_number_recovered(self, value):
         """Set the number of recovered cases"""


    @staticmethod
    @abstractmethod
    def set_number_deaths(self, value):
         """Set the number of death"""


    @staticmethod
    @abstractmethod
    def set_last_update(self, value):
        """Set the last update"""


    @staticmethod
    @abstractmethod
    def update_country(self, value):
        """update country data on Covid-19"""



    @staticmethod
    @abstractmethod
    def update_state(self, value):
        """update state data on Covid-19"""


    @staticmethod
    @abstractmethod
    def get_result(self):
        """Return the Covid cases"""


    class CovidBuilder(ICovidBuilder):
      """The Concrete Builder."""

      def __init__(self):
          self.covid = CovidUpdate()

    def set_number_confrimed(self, value):
        self.covid.confirmed = value
        return self

    def set_number_recovered(self, value):
        self.covid.recovered = value
        return self

    def set_number_deaths(self, value):
        self.covid.deaths = value
        return self

    def set_last_update(self, value):
        self.covid.last_update = value
        return self

    def update_country(self, value):
        self.covid.country = value
        return self

    def update_state(self, value):
         self.covid.state = value
         return self

    def get_result(self):
        return self.covid


    class CovidUpdate():
        """The Product"""

      def __init__(self, confirmed=0, recovered=0, deaths=0, country = " ", state = " ")

      self.confirmed = confirmed
      self.recovered = recovered
      self.deaths = deaths
      self.last_update = last_update
      self.country = country
      self.state = state

    class Director:
        """The Director, building a different representation."""

        @staticmethod
        def construct():
            return CovidBuilder()\
                .set_number_comfirmed()\
                .set_number_recovered()\
                .set_number_deaths()\
                .set_last_update()\
                .update_state()\
                .ipdate_country()\
                .get_result()


    if __name__ == "__main__":
        final = Director.construct()

        print(final)
