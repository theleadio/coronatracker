from .ScrapeBingCovid.scrape_bing import scrape_bing
from .ScrapeRss.scrape_rss import scrape_rss


class Scraper:

    @staticmethod
    def scrape_bing():
        scrape_bing()

    @staticmethod
    def scrape_rss(self):
        scrape_rss()
