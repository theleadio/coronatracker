import scraping.ScrapeBingCovid as Bing
import scraping.scripts as Scripts
from scraping.temporary_cron import TemporaryCorn
from scraping.JHU_Gsheet_DataExtraction import JHUGsheetDataExtraction
from scraping.ScrapeRss.NewsParser import NewsParser
from scraping.ScrapeRss.scrape_rss import ScrapeRss
from scraping.scrape_media import ScraperMedia
import requests
import pandas
import os
import logging
import threading

class Facade():
    
    def __init__(self):
        self.bing = Bing.ScrapeBing()
        self.outbreak = Scripts.OutBreakStates()
        self.worldmeter = Scripts.WorldMeter()
        self.temporarycron = TemporaryCorn()
        self.jhugsheetdataextraction = JHUGsheetDataExtraction()
        self.scrapemedia = ScraperMedia()
        self.newsparser = NewsParser()
        self.scraperss = ScrapeRss()


    def scrapeBing(self):
        bing.wholeWorld()
        bing.countryData()
        bing.stateData()

    def scrapeOutBreak(self):
        outbreak.get_state_details()
        outbreak.get_case_details()

    def scrapeWorldMeter(self):
        args = worldmeter.parser()
        url = "https://www.worldometers.info/coronavirus/"
        res = requests.get(url, headers=worldmeter.HEADER)
        df = pandas.read_html(res.content)
        df[0].fillna(0, inplace=True)
        df[0].apply(
            lambda dataframe: worldmeter.convertKeyAndWriteToDB(
                dataframe, args.stats_table, args.overview_table
            ),
            axis=1,
        )

    def temporaryCron(self):
        temporarycron.run_queries()
    
    def jhuGsheetDataExtraction(self):
        jhugsheetdataextraction.download()

    def scrapeMedia(self):
        scrapemedia

    def newsParser(self):
        newsparser
    
    def scrapeRss(self):
        args = scraperss.parser()

        READ_ALL_SKIP_CACHE = args.all
        debug_mode = args.debug
        database_table_name = args.table

        # create required folders
        if not os.path.isdir("data"):
            logging.debug("Creating ./data directory")
            os.mkdir("./data")

        # reset cache
        if args.clear:
            logging.debug("Clearing cache file {}".format(self.scrapeRss.CACHE_FILE))
            os.system("rm {}".format(scraperss.CACHE_FILE))

        # check cache file exists
        if not os.path.isfile(scraperss.CACHE_FILE):
            logging.debug("Creating cache file {}".format(scraperss.CACHE_FILE))
            os.system("touch {}".format(scraperss.CACHE_FILE))

        # if set READ_ALL_SKIP_CACHE, skip reading cache
        if not READ_ALL_SKIP_CACHE:
            logging.debug("Reading cache file...")
            scraperss.read_cache()

        # initialize threads
        THREADS = []

        # extract all xml data
        for i in range(scraperss.THREAD_LIMIT):
            t = threading.Thread(target=scraperss.seed_worker)
            t.start()
            THREADS.append(t)

        # place initial seed urls to seed queue to process
        for locale, list_url_schema in scraperss.NEWS_SOURCES.items():
            logging.debug(
                "locale: {}, Number of websites: {}".format(locale, len(list_url_schema))
            )
            if not os.path.isdir("./data/{}".format(locale)):
                os.mkdir("./data/{}".format(locale))
            for url_schema in list_url_schema:
                url, schema = url_schema
                logging.debug(
                    "Adding seed url to queue: {}. Schema: {}".format(url, schema)
                )
                seed_object = NewsParser(locale=locale, root_url=url, schema=schema)
                scraperss.SEED_QUEUE.put(seed_object)

        # end seed workers
        scraperss.SEED_QUEUE.join()
        for i in range(len(THREADS)):
            scraperss.SEED_QUEUE.put(None)

        logging.debug(
            "Done extracting all root urls. Approximately {} work to crunch.".format(
                scraperss.EXTRACT_QUEUE.qsize()
            )
        )

        # process extracted urls
        for i in range(len(THREADS)):
            THREADS[i] = threading.Thread(target=scraperss.extract_worker)
            THREADS[i].start()

        # end extract workers
        scraperss.EXTRACT_QUEUE.join()
        for i in range(len(THREADS)):
            scraperss.EXTRACT_QUEUE.put(None)

        logging.debug("Done extracting all feed data")

        if not scraperss.RSS_STACK:
            logging.debug("RSS Stack is empty. Exiting...")
            exit()

        if debug_mode:
            # print output and write to jsonl file
            scraperss.print_pretty()
            scraperss.write_output()
        else:
            # Store to DB
            scraperss.save_to_db(database_table_name)

        count = 0
        for lang, rss_records in scraperss.RSS_STACK.items():
            count += len(rss_records)
        logging.debug("Total feeds: {}".format(count))
        logging.debug("Done scraping.")