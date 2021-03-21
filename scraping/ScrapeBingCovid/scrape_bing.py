
import sys
import os
import logging

from datetime import datetime
from dateutil import parser

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

#This class acts as the aggregate root
#It allows entry to specific data points from sublasses within the same domain of BingCovidData
class BingCovidData: 
    def __init__(self,  posted_date=datetime.utcnow()):
    self.posted_date = posted_date
    self.worlddata = self.WorldData()    

    #This subclass contains enities specifically regarding the whole world
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

    #This subclass contains enities specifically regarding specific countries
    class Country:
        def __init__(
            self, 
            confirmed = None,
            deaths = None,
            recovered = None,
            last_update = None,
            lat = None,
            lng = None,
            country = None,
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

    #This subclass contains enities specifically regarding specific states
    class State:
          def __init__(
            self, 
            confirmed = None,
            deaths = None,
            recovered = None,
            last_update = None,
            lat = None,
            lng = None,
            country = None,
            state = None,
            posted_date=datetime.utcnow()
          ):
            self.confirmed = confirmed
            self.deaths = deaths
            self.recovered = recovered
            self.last_update = last_update
            self.lat = lat
            self.lng = lng
            self.country = country
            self.state = state
            self.posted_date = posted_date       


if __name__ == "__main__":
    db_bingcovid.connect()
    res = get_seed_page(API_URL).json()

    # Whole world
    #Instead of refrencing BingCovid, data pertaining to the whole world is refrenced through BingCovidData.World
    wholeWorld = BingCovidData.World(
        confirmed=res["totalConfirmed"],
        deaths=res["totalDeaths"],
        recovered=res["totalRecovered"],
    )
    logging.debug("Inserting whole_world data: {}".format(wholeWorld.__dict__))
    db_bingcovid.insert(wholeWorld.__dict__, target_table=DB_TABLE)

    # Countries
    for countryData in res["areas"]:
        #Instead of refrencing BingCovid, data pertaining to a specific country is refrenced through BingCovidData.Country
        currentCountry = BingCovidData.Country(
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
            #Instead of refrencing BingCovid, data pertaining to a specific country is refrenced through BingCovidData.State
            currentState = BingCovidData.State(
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
