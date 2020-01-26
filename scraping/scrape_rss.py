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
            rss_record['link'] = getfeed.link.text
            
            now = datetime.now()
 
            # dd/mm/YY H:M:S
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            rss_record['access_date'] = dt_string
            rss_record['source']= soup_page.channel.title.text

            article = extract_article(rss_record['link'])

            #Get the authors
            rss_record['author'] =  article.authors
            #Get the publish date 
            if getfeed.pubDate:
                rss_record['pub_date'] = getfeed.pubDate.text
            elif article.publish_date:
                rss_record['pub_date'] = article.publish_date
            elif soup_page.lastBuildDate:
                rss_record['pub_date'] = soup_page.lastBuildDate.text
                
            #Get the article text
            #print(article.text)
            #Get a summary of the article
            rss_record['summary' ] = article.summary
            #Get the top image 
            rss_record['top_image_url'] = article.top_image
            rss_record['images'] = article.images
            rss_stack.append(rss_record)
            

def print_pretty(stack):
    for rss_record in stack:
        to_print = ""
        to_print += "\nTitle:\t" + rss_record['title']
        to_print += "\nDesc:\t" + rss_record['description']
        to_print += "\nLink:\t" + rss_record['link']
        to_print += "\nPub Date:\t" + str(rss_record['pub_date'])
        to_print += "\nAccessed:\t" + rss_record['access_date']
        to_print += "\nSource:\t" + rss_record['source']
        to_print += "\nAuthor:\t" + ', '.join(map(str, rss_record['author'])) 
        to_print += "\nSummary:\n" + rss_record['summary']
        to_print += "\nTop Image:\t" + rss_record['top_image_url']
        #to_print += "\nImages:\n" + '\n'.join(map(str, rss_record['images']))
        print(to_print.expandtabs())
        

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
