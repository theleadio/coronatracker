#!/usr/bin/env python3
#
# dipto.pratyaksa@carltondigital.com.au
# ref: https://santhoshveer.com/rss-feed-reader-using-python/
#
# TO DO:
# Store the relevant RSS feed into shared repo, like Google sheet
# Algo to extract the casualty stats from linked news article

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

    print(soup_page.channel.title.text)

    for getfeed in news_list:
       
        res = [ele.lower() for ele in keywords if(ele in getfeed.title.text.lower())]
        if bool(res):
            print("\n")
            print('Title:\t %s' %getfeed.title.text)
            print('Desc:\t %s' %getfeed.description.text)
            print('Link:\t %s' %getfeed.link.text)
            if getfeed.pubDate:
                print('Pub Date:\t %s' %getfeed.pubDate.text)
            print("\n")

NEWS_URLs = ["https://www.theage.com.au/rss/feed.xml",
             "https://www.theage.com.au/rss/world.xml",
             "http://www.heraldsun.com.au/news/breaking-news/rss",
             "http://www.heraldsun.com.au/rss",
             "https://www.news.com.au/content-feeds/latest-news-world/",
             "https://www.news.com.au/content-feeds/latest-news-national/"]         
keywords = ["corona", "coronavirus", "epidemic", "epidemy", "disease"]

for rss in NEWS_URLs:
    news(rss, keywords)
