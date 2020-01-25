#!/usr/bin/env python3
#
# ddipto.pratyaksa@carltondigital.com.au
# ref: https://santhoshveer.com/rss-feed-reader-using-python/

from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

def news(xml_news_url, words_list):
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(xml_news_url,headers=hdr)
    parse_xml_url = urlopen(req)
    xml_page = parse_xml_url.read()
    parse_xml_url.close()

    soup_page = BeautifulSoup(xml_page, "xml")
    news_list = soup_page.findAll("item")

    for getfeed in news_list:
        #if(keywords[0] in getfeed.title.text):
        #if any(ext in keywords for ext in getfeed):
        res = [ele.lower() for ele in keywords if(ele in getfeed.title.text.lower())]
        if bool(res):
            print("\n")
            print('\033[1;33m %s \033[1;m' %getfeed.title.text)
            print('\033[1;32m %s \033[1;m' %getfeed.link.text)
            if getfeed.pubDate:
                print('\033[1;35m %s \033[1;m' %getfeed.pubDate.text)
            print("\n")

#NEWS_URL = "https://news.ycombinator.com/rss"
NEWS_URLs = ["https://www.theage.com.au/rss/feed.xml",
             "http://www.heraldsun.com.au/news/breaking-news/rss",
             "https://www.news.com.au/content-feeds/latest-news-world/",
             "https://www.news.com.au/content-feeds/latest-news-national/"]         
keywords = ["corona", "coronavirus", "epidemic", "epidemy", "disease"]

for rss in NEWS_URLs:
    news(rss, keywords)
