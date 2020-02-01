# TO-DO:
# [DONE] Set keyword to detect ’武漢肺炎‘(wuhan pneumonia),‘國家衛健委’(NHC),‘新型冠狀病毒’(coronavirus) at news article page
# [DONE] Debug Non-Type Error
# Connect to db


from bs4 import BeautifulSoup
import requests

# url from main page
url = 'https://www.cna.com.tw/news/ahel/202001215004.aspx'
response = requests.get(url, timeout=5)
content = BeautifulSoup(response.content, "html.parser")


# gather url of articles
article_url = []
for title in content.find_all('a', {"class": "menuUrl"}):
    link = title.get('href')
    article_url.append(link)


# empty list to collect newsObject for each url
newsObject_stack = []

# filtering related news and extract information
for news in article_url:
    news_response = requests.get(news, timeout=5)
    news_content = BeautifulSoup(news_response.content, "html.parser")

    keyword = ['武漢肺炎', '國家衛健委', '新型冠狀病毒', '口罩']
    # keyword translation: wuhan pneumonia, NHC, coronavirus, face mask

    article_keyword = news_content.find(
        'meta', {'name': 'keywords'}).get('content')
    # detect keyword, if present then extract information to dict
    if any(words in article_keyword for words in keyword):

        # combining paragraphs of news article
        article_lines = []
        news_paragraphs = news_content.find(
            'div', {'class': 'paragraph'}).find_all('p')
        for line in news_paragraphs:
            article_lines.append(line.text)

        newsObject = {
            'title': news_content.find('article', {"class": "article"}).get('data-title'),
            'description': news_content.find('meta', {"name": "description"}).get('content'),
            'content': "".join(article_lines),
            'author': news_content.find('meta', {"itemprop": 'author'}).get('content'),
            'url': news,
            'urlToImage': news_content.find('link', {"rel": 'image_src'}).get('href'),
            'publishedAt': news_content.find('meta', {"itemprop": 'datePublished'}).get('content'),
            'siteName': "cna.com.tw",
            'language': "ch_trad"
        }

        newsObject_stack.append(newsObject)
        # print(newsObject)
