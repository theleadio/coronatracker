from datetime import datetime
from dateutil import parser


class BingCovid:
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
        posted_date=datetime.utcnow(),
    ):
        self.state = state
        self.country = country
        self.last_update = parser.parse(last_update) if last_update else last_update
        self.lat = lat
        self.lng = lng
        self.confirmed = confirmed
        self.deaths = deaths
        self.recovered = recovered
        self.posted_date = posted_date



#New File with changes

from datetime import datetime
from dateutil import

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


#Aggregate root


Class Covid_Cases:

 def __init__(self, country: str, state: str, recovered: list[], confirmed: list[], deaths: list[])

self.country = country
self.recovered = recovered
self.confirmed = confirmed
self.deaths = deaths


# BingCovid
from ScrapeBingCovid.BingCovid import BingCovid

if __name__ == "__main__":
    db_bingcovid.connect()
    res = get_seed_page(API_URL).json()

     # Countries data about Covid19 cases
    for countryData in res["areas"]:

    #changed BingCovid to Covid_Cases
        currentCountry = Covid_Cases(
            confirmed=countryData["totalConfirmed"],
            deaths=countryData["totalDeaths"],
            recovered=countryData["totalRecovered"],
            country=countryData["country"],

   logging.debug("Inserting country data: {}".format(currentCountry.__dict__))
        db_bingcovid.insert(currentCountry.__dict__, target_table=DB_TABLE)



        # States data about Covid19 cases
        for stateData in countryData["areas"]:

        #changed BingCovid to Covid_Cases
            currentState = Covid_Cases(
                confirmed=stateData["totalConfirmed"],
                deaths=stateData["totalDeaths"],
                recovered=stateData["totalRecovered"],
                state=stateData["displayName"],
                country=countryData["country"],

     logging.debug("Inserting state data: {}".format(currentState.__dict__))
            db_bingcovid.insert(currentState.__dict__, target_table=DB_TABLE)
