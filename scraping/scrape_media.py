#this is aggregate root for scrape_webscraper and scrape_twitter
from .webscraper import webscraper
from .scrape_twitter import scrape_twitter

class ScraperMedia():

    def scrape_twitter(self):
        scrape_twitter()

    def webscraper(self):
        webscraper()   


