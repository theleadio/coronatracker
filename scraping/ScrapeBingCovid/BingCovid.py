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

<<<<<<< Updated upstream
     def add_to_queue(self):
        for bings_object in self.bings_list:
            EXTRACT_QUEUE.put(bings_object)
=======
from DatabaseConnector import db_bingcovid
     DB_TABLE = "test"
     API_URL = "https://bing.com/covid/data"

     if __name__ == "__main__":
         db_bingcovid.connect()
         res = get_seed_page(API_URL).json()
>>>>>>> Stashed changes
