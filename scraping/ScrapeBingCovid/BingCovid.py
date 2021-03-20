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

        #This BingCovid class will act as our aggregate root, and the other two classes will be two entites.

        #Creating a way to access country data info through BingCovidCountry
        def country_data(self):
            access_to_coutrydata = BingCovidCountry(self.country,self.last_update,self.lat,self.lng,self.confirmed,self.deaths,self.recovered)
        #Creating a way to access state data info through BingCovidState
        def state_data(self):
            access_to_statedata = BingCovidState(self.last_update,self.lat,self.lng,self.confirmed,self.deaths,self.recovered,self.state,self.country)
#Changes are made from this point onwards

class BingCovidCountry:
        def __init__(
                self,
                country=None,
                last_update=None,
                lat=None,
                lng=None,
                confirmed=None,
                deaths=None,
                recovered=None,
        ):
            self.confirmed = confirmed
            self.deaths = deaths
            self.recovered = recovered
            self.last_update = parser.parse(last_update) if last_update else last_update
            self.lat = lat
            self.lng = lng
            self.country = country


class BingCovidState:
    def __init__(
            self,
            last_update=None,
            lat=None,
            lng=None,
            confirmed=None,
            deaths=None,
            recovered=None,
            state=None,
            country=None,
    ):
        self.confirmed = confirmed
        self.deaths = deaths
        self.recovered = recovered
        self.last_update = parser.parse(last_update) if last_update else last_update
        self.lat = lat
        self.lng = lng
        self.state = state
        self.country = country