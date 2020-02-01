# TO-DO:
# Set keyword to detect ’武漢肺炎‘(wuhan pneumonia),‘國家衛健委’(NHC),‘新型冠狀病毒’(coronavirus) at main page
# Debug Non-Type Error
# Connect to db


from bs4 import BeautifulSoup
import requests

# url from main page
url = 'https://www.cna.com.tw/news/ahel/202001215004.aspx'
response = requests.get(url, timeout=5)
content = BeautifulSoup(response.content, "html.parser")


# url for news content specific page (for testing)
#a = 'https://www.cna.com.tw/news/ahel/202001315007.aspx'
#news_url = requests.get(a,timeout=5)
#news_content = BeautifulSoup(news_url.content, "html.parser")



for title in content.find_all('a', {"class":"menuUrl"}):
    # scrape from individual links
    news_url = title.get('href')
    news_response = requests.get(news_url, timeout=5)
    news_content = BeautifulSoup(news_response.content, "html.parser")

    # combining paragraphs of news article
    article_lines = []
    news_paragraphs = news_content.find_all('p')
    for line in news_paragraphs:
        text = line.string
        article_lines.append(text)

    # gather information, make dict for json output -> db
    newsObject = {
        'title': title.string,
        'description': news_content.find('meta',{"name":"description"}).get('content'),
        'content':"".join(article_lines),
        'author':news_content.find('meta',{"itemprop":'author'}).get('content'),
        'url': news_url,
        'urlToImage':news_content.find('link',{"rel":'image_src'}).get('href'),
        'publishedAt':news_content.find('meta',{"itemprop":'datePublished'}).get('content'), 
        'siteName':"cna.com.tw",
        'language':"ch_trad"
       

    }

    print(newsObject)
