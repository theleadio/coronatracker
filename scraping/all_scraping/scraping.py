from .ScrapeBingCovid.scrape_bing import scrape_bing
from .ScrapeRss.scrape_rss import scrape_rss
from .webscraper import webscraper
from .GlobalTimes_scraping import GlobalTimes_scraping
from .scrape_outbreak_states import scrape_outbreak_states
from .scrape_worldometers import scrape_world_meters
from .scrape_twitter import scrape_twitter


class Scraper:

    @staticmethod
    def scrape_bing():
        scrape_bing()

    @staticmethod
    def scrape_rss():
        scrape_rss()

    @staticmethod
    def web_scraper():
        webscraper()

    @staticmethod
    def global_times_scraping():
        GlobalTimes_scraping()

    @staticmethod
    def scrape_outbreak_states():
        scrape_outbreak_states()

    @staticmethod
    def scrape_world_meters():
        scrape_world_meters()

    @staticmethod
    def scrape_twitter():
        scrape_twitter()
