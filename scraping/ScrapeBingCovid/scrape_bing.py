import sys
import os
import logging

from datetime import datetime
from dateutil import parser

from abc import ABC, abstractmethod

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

# BingCovid class that is now BingData and contains default values for the potential domain of the object being created
class BingData:
    def __init__(self,
       state=None,
       country=None,
       last_update=None,
       lat=None,
       lng=None,
       confirmed=None,
       deaths=None,
       recovered=None,

    );

       self.last_update = parser.parse(last_update) if last_update else last_update
       self.posted_date=datetime.utcnow()
        
# Abstract builder class to define the interface of what we can build
class DataBuilder(ABC):

    #Reset the builder
    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def build_world(self):
        pass 

    @abstractmethod
    def build_country(self):
        pass     

    @abstractmethod
    def build_state(self):
        pass 

# Implementation for building data pertaining to the world
class WorldBuilder(DataBuilder):
    def __init__(self):
        self.data = BingData()

    def reset(self): 
        self.data = BingData()

    def get_data(self):
        return self.data

    def build_world(self):
        self.data.confirmed = confirmed
        self.data.deaths = deaths
        self.data.recovered = recovered
        
# Implementation for building data pertaining to countries
class CountryBuilder(DataBuilder):
    def __init__(self):
        self.data = BingData()

    def reset(self): 
        self.data = BingData()

    def get_data(self):
        return self.data

    def build_country(self):
        self.data.confirmed = confirmed
        self.data.deaths = deaths
        self.data.recovered = recovered
        self.lat = lat
        self.lng = lng
        self.country = country

# Implementation for building data pertaining to sates
 class StateBuilder(DataBuilder):
    def __init__(self):
        self.data = BingData()

    def reset(self): 
        self.data = BingData()

    def get_data(self):
        return self.data

    def build_state(self):
        self.data.confirmed = confirmed
        self.data.deaths = deaths
        self.data.recovered = recovered
        self.lat = lat
        self.lng = lng
        self.country = country    
        self.state = state   


if __name__ == "__main__":
    db_bingcovid.connect()
    res = get_seed_page(API_URL).json()

    # whole world
    # create a world builder, then build the world  data
    builder = WorldBuilder()

        builder.build_world(
        confirmed=res["totalConfirmed"],
        deaths=res["totalDeaths"],
        recovered=res["totalRecovered"],
    )
    # Store data that was built
    wholeWorld= builder.get_data()

    logging.debug("Inserting whole_world data: {}".format(wholeWorld.__dict__))
    db_bingcovid.insert(wholeWorld.__dict__, target_table=DB_TABLE)

    # Countries

    for countryData in res["areas"]:

        # for each country create a country builder, then build the country data
        # data is reset each iteration
        builder.reset()
        builder = CountryBuilder()

            builder.build_country(
            confirmed=countryData["totalConfirmed"],
            deaths=countryData["totalDeaths"],
            recovered=countryData["totalRecovered"],
            last_update=countryData["lastUpdated"],
            lat=countryData["lat"],
            lng=countryData["long"],
            country=countryData["country"],
        )
        # Store data that was built
        currentCountry = builder.get_data()

        logging.debug("Inserting country data: {}".format(currentCountry.__dict__))
        db_bingcovid.insert(currentCountry.__dict__, target_table=DB_TABLE)

        # States
        for stateData in countryData["areas"]:

            # for each state create a state builder, then build the state data
            # data is reset each iteration
            builder.reset()
            builder = StateBuilder()

                builder.build_state(
                confirmed=stateData["totalConfirmed"],
                deaths=stateData["totalDeaths"],
                recovered=stateData["totalRecovered"],
                last_update=stateData["lastUpdated"],
                lat=stateData["lat"],
                lng=stateData["long"],
                state=stateData["displayName"],
                country=countryData["country"],
            )
            # Store data that was built
            currentState = builder.get_data()

            logging.debug("Inserting state data: {}".format(currentState.__dict__))
            db_bingcovid.insert(currentState.__dict__, target_table=DB_TABLE)
