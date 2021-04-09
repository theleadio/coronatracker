import CovidBuilder
from datetime import datetime
from dateutil import parser

class BingCovidBuilder(CovidBuilder):
    """
    The concrete builder class of the CovidBuilder interface.
    Other concrete classes can implement the interface like
    a YahooCovidBuilder class which deals with Yahoo articles.
    """

    # Attributes
    state = None
    country = None
    last_update = None
    lat = None
    lng = None
    confirmed = None
    deaths = None
    recovered = None
    posted_date = None


    def __init__(self):
        self.posted_date = datetime.utcnow()

    def add_state(self, state):
        self.state = state

    def add_country(self, country):
        self.country = country

    def add_last_update(self, last_update):
        self.last_update = last_update

    def add_lat(self, lat):
        self.lat = lat

    def add_lng(self, lng):
        self.lng = lng

    def add_confirmed(self, confirmed):
        self.confirmed = confirmed

    def add_deaths(self, deaths):
        self.deaths = deaths

    def add_recovered(self, recovered):
        self.recovered = recovered

    def build(self):
        pass

