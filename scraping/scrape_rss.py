#!/usr/bin/env python3
#
# dipto.pratyaksa@carltondigital.com.au
# 26/1/2020
#
# REF:
# https://santhoshveer.com/rss-feed-reader-using-python/
# https://medium.com/@ankurjain_79625/how-did-i-scrape-news-article-using-python-6eff936b3c8c
# https://medium.com/@randerson112358/scrape-summarize-news-articles-using-python-51a48af1b4e2
#
# TO DO:
# Store the relevant RSS feed into shared repo, like Google sheet
# Algo to extract the casualty stats from linked news article

from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil.parser import parse
import re

import db_connector


import nltk
from newspaper import Article
import pprint

rss_stack = []

def news(xml_news_url, words_list):
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(xml_news_url,headers=hdr)
    parse_xml_url = urlopen(req)
    xml_page = parse_xml_url.read()
    parse_xml_url.close()

    soup_page = BeautifulSoup(xml_page, "xml")
    news_list = soup_page.findAll("item")

    #print(soup_page.channel.title.text)


    for getfeed in news_list:
       
        res_title = [ele.lower() for ele in keywords if(ele in getfeed.title.text.lower())]
        res_desc = [ele.lower() for ele in keywords if(ele in getfeed.description.text.lower())]

        rss_record = {}
        if bool(res_title or res_desc): #check if any of the keywords occur in title or description
            rss_record['title'] = getfeed.title.text
            rss_record['description'] = getfeed.description.text            
            rss_record['url'] = getfeed.link.text
            
            now = datetime.now()
 
            # dd/mm/YY H:M:S
            dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
            rss_record['accessDateTime'] = dt_string
            rss_record['source']= soup_page.channel.title.text

            article = extract_article(rss_record['url'])

            #Get the authors
            rss_record['author'] =  ', '.join(map(str, article.authors)) 

            
            #Get the publish date 
            if getfeed.pubDate:
                rss_record['publishDateTime'] = date_convert(getfeed.pubDate.text)
            elif article.publish_date:
                rss_record['publishDateTime'] = article.publish_date
                
            elif soup_page.lastBuildDate:
                rss_record['publishDateTime'] = date_convert(soup_page.lastBuildDate.text)
                
            #Get the article text
            #print(article.text)
            #Get a summary of the article
            rss_record['summary' ] = article.summary
            rss_record['content' ] = article.text
            #Get the top image 
            rss_record['urlToImage'] = article.top_image
            rss_record['images'] = article.images
            rss_stack.append(rss_record)
            

def print_pretty(stack):
    for rss_record in stack:
        to_print = ""
        to_print += "\nTitle:\t" + rss_record['title']
        to_print += "\nDesc:\t" + rss_record['description']
        to_print += "\nLink:\t" + rss_record['url']
        to_print += "\nPub Date:\t" + str(rss_record['publishDateTime'])
        to_print += "\nAccessed:\t" + rss_record['accessDateTime']
        to_print += "\nSource:\t" + rss_record['source']
        to_print += "\nAuthor:\t" +  rss_record['author']
        to_print += "\nSummary:\n" + rss_record['summary']
        to_print += "\nContent:\n" + rss_record['content']
        to_print += "\nTop Image:\t" + rss_record['urlToImage']
        #to_print += "\nImages:\n" + '\n'.join(map(str, rss_record['images']))
        try:
            #to_print  = str(to_print , encoding='utf-8', errors = 'ignore')
            print(to_print.expandtabs())
        except:
            pass
        
def save_to_db(stack):

    db_connector.connect()
    for rss_record in stack:
        db_connector.insert(rss_record)

def date_convert(date_string):
    print("input date" + date_string)
    all = re.findall(r"[\d]{1,2} [ADFJMNOS]\w* [\d]{4} \b(?:[01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]\b", date_string)
    if len(all)>0:
        datetime_str = all[0] # '09/19/18 13:55:26'
        datetime_object = datetime.strptime(datetime_str, '%d %b %Y %H:%M:%S')

        print(type(datetime_object))
        print(datetime_object)  # printed in default format
    else:
        datetime_object = date_string
    return datetime_object

def extract_article(link):
    print("Extracting from: ", link)
    article = Article(link)
    # Do some NLP
    article.download() #Downloads the link’s HTML content
    article.parse() #Parse the article
    nltk.download('punkt')#1 time download of the sentence tokenizer
    article.nlp()#  Keyword extraction wrapper

    return article


    
    
NEWS_URLs = ["https://www.theage.com.au/rss/feed.xml",
             "https://www.theage.com.au/rss/world.xml",
             "http://www.heraldsun.com.au/news/breaking-news/rss",
             "http://www.heraldsun.com.au/rss",
             "https://www.news.com.au/content-feeds/latest-news-world/",
             "https://www.news.com.au/content-feeds/latest-news-national/",
             "http://www.dailytelegraph.com.au/news/breaking-news/rss",
             "http://www.dailytelegraph.com.au/news/national/rss",
             "http://www.dailytelegraph.com.au/newslocal/rss",
             "http://www.dailytelegraph.com.au/news/world/rss",
             "https://www.sbs.com.au/news/topic/latest/feed"
             ]         
keywords = ["corona", "coronavirus"]

for rss in NEWS_URLs:
    news(rss, keywords)

print_pretty(rss_stack)
save_to_db(rss_stack)
