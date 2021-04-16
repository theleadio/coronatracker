"""
Crawling:
http://www.dailytelegraph.com.au/news/breaking-news/rss
http://www.dailytelegraph.com.au/newslocal/rss
http://www.news24.jp/sitemap_economy.xml
http://www.news24.jp/sitemap_international.xml
http://www.news24.jp/sitemap_society.xml
http://www.taipeitimes.com/sitemap.xml
https://baomoi.com/sitemaps/sitemap-news.xml
https://news.kompas.com/web/sitemap.xml
https://toyokeizai.net/sitemap.xml
https://vietnamnews.vn/sitemap.xml
https://vnexpress.net/google-news-sitemap.xml
https://www.channelnewsasia.com/googlenews/cna_news_sitemap.xml
https://www.ettoday.net/news-sitemap.xml
https://www.liputan6.com/sitemap_post.xml
https://www.news.com.au/content-feeds/latest-news-national/
https://www.news.com.au/content-feeds/latest-news-world/
https://www.sbs.com.au/news/topic/latest/feed
https://www.scmp.com/rss/318208/feed
https://www.shine.cn/sitemap-news.xml
https://www.taiwannews.com.tw/ch/sitemap.xml
https://www.taiwannews.com.tw/en/sitemap.xml
https://www.theage.com.au/rss/feed.xml
https://www.tienphong.vn/event/virus-covid19-2302.tpo
http://www.hani.co.kr/arti/RSS/sitemap_www.xml
http://www.koreatimes.co.kr/www/rss/world.xml
http://www.koreatimes.co.kr/www/rss/nation.xml
http://koreajoongangdaily.joins.com/sitemap_google_news.xml
https://news.joins.com/sitemap/latest-articles
http://www.donga.com/sitemap/donga-newsmap.xml
https://news.chosun.com/google/rss.html
https://news.chosun.com/site/data/rss/rss.xml
http://english.chosun.com/site/data/rss/rss.xml
https://thestandard.co/coronavirus-coverage/
https://www.thairath.co.th/sitemap-daily.xml
https://rss.komchadluek.net/latest_news_google_news.xml
https://www.ilmessaggero.it/?sez=XML&p=MapNews
https://www.leggo.it/?sez=XML&p=MapNews
https://www.lastampa.it/sitemap.xml
https://www.malaymail.com/sitemap.xml
https://www.projekmm.com/sitemap.xml
https://www.orientaldaily.com.my/sitemap.xml
https://www.welt.de/sitemaps/newssitemap/newssitemap.xml
https://www.welt.de/sitemaps/sitemap/today.xml
https://www.focus.de/
https://www.faz.net/aktuell/
http://www.gov.cn/google.xml
https://www.nu.nl/sitemap_news.xml
https://www.rivm.nl/sitemap.xml
https://www.nrc.nl/sitemap/index.xml
https://www.thehindu.com/sitemap/googlenews.xml
https://www.dailythanthi.com/Sitemap/googlesitemap.xml
https://www.maalaimalar.com/Sitemap/googlesitemap.xml
https://www.hindutamil.in/feed/news-corona-virus-518.xml
https://www.livehindustan.com/news-sitemap.xml
https://www.bhaskar.com/sitemapgoogle/topnews_1.xml
https://www.jagran.com/news-sitemap.xml
https://www.timestamilnews.com/

Don't crawl:
http://www.heraldsun.com.au/news/breaking-news/rss
http://www.heraldsun.com.au/rss
https://www.theage.com.au/rss/world.xml
http://www.dailytelegraph.com.au/news/national/rss
http://www.dailytelegraph.com.au/news/world/rss

"""

from ScrapeRss.globals import (
    ISO_8601_DATE_FORMAT,
    ISO_8601_DATE_WITHOUT_SEC_FORMAT,
    YEAR_MONTH_DAY_FORMAT,
)

from abc import ABCMeta, abstractmethod

class INewsSourceBuilder(metaclass = ABCMeta):
    "The Builder Interface"

@staticmethod
@abstractmethod
def build_url():
    pass

@staticmethod
@abstractmethod
def build_title():
    pass

@staticmethod
@abstractmethod
def build_description():
    pass

@staticmethod
@abstractmethod
def build_data_xml():
    pass

@staticmethod
@abstractmethod
def get_news():
    pass
    
class NewsSource(INewsSourceBuilder):
    "concrete builder"

    def __init__(self): 
        self.Product = Product()
    
    def build_url(self, url):
        self.url = url
        return self
    
    def build_title(self, title):
        self.title = title
        return self
    
    def build_description(self, description):
        self.description = description
        return self
    
    def build_data_xml(self, data_xml):
        self.data_xml = data_xml
        return self

    def get_News(self):
        return self.product

class Product():
    "the products"

    def __init__(self):
        self.news = []

class Director:
    "the director, building a complex representation"

    @staticmethod
    def construct():
        "constructs and return final products"
        return Builder()\
            .build_url()\
            .build_title()\
            .build_description()\
            .build_data_xml()\
            .get_news()

NEWS_SOURCES = {
    "de_DE": [
        (
            "https://www.welt.de/sitemaps/newssitemap/newssitemap.xml",
            {
                "url": "loc",
                "title": "news:title",
                "keywords": "news:keywords",
                "date_xml": ("news:publication_date", ISO_8601_DATE_FORMAT),
            },
        ),
        (
            "https://www.welt.de/sitemaps/sitemap/today.xml",
            {
                "url": "loc",
                "title": "image:title",
                "date_xml": ("lastmod", ISO_8601_DATE_FORMAT),
            },
        ),
        ("https://www.focus.de/", {"not_xml": True,},),
        ("https://www.faz.net/aktuell/", {"not_xml": True,},),
    ],
    "en_AU": [
        (
            "https://www.theage.com.au/rss/feed.xml",
            {
                "title": "title",
                "description": "description",
                "url": "link",
                "date_xml": ("pubDate", None),
            },
        ),
        # Doesn't work anymore, couldn't access rss feed
        # (
        #     "https://www.theage.com.au/rss/world.xml",
        #     {"title": "title", "description": "description", "url": "link",},
        # ),
        # Remove heraldsun rss to prevent scraping the same content as other rss
        # > as it's a smaller newspaper that is likely syndicating news from bigger news
        #         (
        #             "http://www.heraldsun.com.au/news/breaking-news/rss",
        #             {"title": "title", "description": "description", "url": "link",},
        #         ),
        #         (
        #             "http://www.heraldsun.com.au/rss",
        #             {"title": "title", "description": "description", "url": "link",},
        #         ),
        (
            "https://www.news.com.au/content-feeds/latest-news-world/",
            {
                "title": "title",
                "description": "description",
                "url": "link",
                "date_xml": ("pubDate", None),
            },
        ),
        (
            "https://www.news.com.au/content-feeds/latest-news-national/",
            {
                "title": "title",
                "description": "description",
                "url": "link",
                "date_xml": ("pubDate", None),
            },
        ),
        (
            "http://www.dailytelegraph.com.au/news/breaking-news/rss",
            {"title": "title", "description": "description", "url": "link",},
        ),
        # (
        #     "http://www.dailytelegraph.com.au/news/national/rss",
        #     {"title": "title", "description": "description", "url": "link",},
        # ),
        (
            "http://www.dailytelegraph.com.au/newslocal/rss",
            {"title": "title", "description": "description", "url": "link",},
        ),
        # (
        #     "http://www.dailytelegraph.com.au/news/world/rss",
        #     {"title": "title", "description": "description", "url": "link",},
        # ),
        (
            "https://www.sbs.com.au/news/topic/latest/feed",
            {
                "title": "title",
                "description": "description",
                "url": "link",
                "date_xml": ("pubDate", None),
            },
        ),
    ],
    "en_CN": [
        (
            "https://www.shine.cn/sitemap-news.xml",
            {
                "title": "news:title",
                "url": "loc",
                "date_xml": ("news:publication_date", ISO_8601_DATE_FORMAT),
            },
        ),
    ],
    "en_IN": [
        (
            "https://www.thehindu.com/sitemap/googlenews.xml",
            {
                "title": "news:title",
                "url": "loc",
                "keywords": "news:keywords",
                "date_xml": ("lastmod", ISO_8601_DATE_FORMAT),
            },
        ),
    ],
    "en_TW": [
        (
            "http://www.taipeitimes.com/sitemap.xml",
            {"url": "loc", "date_xml": ("lastmod", ISO_8601_DATE_FORMAT),},
        ),
        (
            "https://www.taiwannews.com.tw/en/sitemap.xml",
            {
                "title": "news:title",
                "url": "loc",
                "date_xml": ("news:publication_date", YEAR_MONTH_DAY_FORMAT),
            },
        ),
    ],
    "en_SG": [
        (
            "https://www.channelnewsasia.com/googlenews/cna_news_sitemap.xml",
            {
                "title": "title",
                "description": "news:keywords",
                "url": "loc",
                "date_xml": ("news:publication_date", ISO_8601_DATE_FORMAT),
            },
        ),
    ],
    "en_HK": [
        (
            "https://www.scmp.com/rss/318208/feed",
            {
                "title": "title",
                "description": "description",
                "url": "link",
                "date_xml": ("pubDate", None),
            },
        ),
    ],
    "en_KR": [
        (
            "http://english.chosun.com/site/data/rss/rss.xml",
            {
                "title": "title",
                "description": "description",
                "url": "link",
                "date_xml": ("dc:date", ISO_8601_DATE_FORMAT),
            },
        ),
        (
            "http://www.koreatimes.co.kr/www/rss/world.xml",
            {
                "title": "title",
                "description": "description",
                "url": "link",
                "author": "author",
            },
        ),
        (
            "http://www.koreatimes.co.kr/www/rss/nation.xml",
            {
                "title": "title",
                "description": "description",
                "url": "link",
                "author": "author",
            },
        ),
        (
            "http://koreajoongangdaily.joins.com/sitemap_google_news.xml",
            {
                "title": "news:title",
                "url": "loc",
                "date_xml": ("news:publication_date", YEAR_MONTH_DAY_FORMAT),
            },
        ),
    ],
    "hi_IN": [
        (
            "https://www.livehindustan.com/news-sitemap.xml",
            {
                "title": "news:title",
                "url": "loc",
                "keywords": "news:keywords",
                "date_xml": ("lastmod", ISO_8601_DATE_FORMAT),
            },
        ),
        (
            "https://www.bhaskar.com/sitemapgoogle/topnews_1.xml",
            {
                "title": "news:title",
                "url": "loc",
                "keywords": "news:keywords",
                "date_xml": ("news:publication_date", ISO_8601_DATE_FORMAT),
            },
        ),
        (
            "https://www.jagran.com/news-sitemap.xml",
            {
                "title": "news:title",
                "url": "loc",
                "keywords": "news:keywords",
                "date_xml": ("news:publication_date", ISO_8601_DATE_FORMAT),
            },
        ),
    ],
    "ko_KR": [
        (
            "https://news.chosun.com/google/rss.html",
            {
                "title": "title",
                "description": "description",
                "url": "link",
                "date_xml": ("pubDate", None),
            },
        ),
        (
            "https://news.chosun.com/site/data/rss/rss.xml",
            {
                "title": "title",
                "description": "description",
                "url": "link",
                "author": "author",
                "date_xml": ("dc:date", ISO_8601_DATE_FORMAT),
            },
        ),
        (
            "https://news.joins.com/sitemap/latest-articles",
            {
                "title": "news:title",
                "url": "loc",
                "keywords": "news:keywords",
                "date_xml": ("news:publication_date", ISO_8601_DATE_FORMAT),
            },
        ),
        (
            "http://www.donga.com/sitemap/donga-newsmap.xml",
            {
                "title": "news:title",
                "url": "loc",
                "date_xml": ("news:publication_date", ISO_8601_DATE_FORMAT),
            },
        ),
        (
            "http://www.hani.co.kr/arti/RSS/sitemap_www.xml",
            {
                "title": "news:title",
                "url": "loc",
                "date_xml": ("news:publication_date", ISO_8601_DATE_WITHOUT_SEC_FORMAT),
            },
        ),
    ],
    "en_QA": [
        (
            "https://www.aljazeera.com/xml/sslsitemaps/sitemap2020_1.xml",
            {"url": "loc", "date_xml": ("lastmod", YEAR_MONTH_DAY_FORMAT),},
        ),
    ],
    "id_ID": [("https://news.kompas.com/web/sitemap.xml", {"url": "loc",},),],
    "it_IT": [
        (
            "https://www.ilmessaggero.it/?sez=XML&p=MapNews",
            {
                "title": "news:title",
                "url": "loc",
                "keywords": "news:keywords",
                "date_xml": ("news:publication_date", ISO_8601_DATE_FORMAT),
            },
        ),
        (
            "https://www.leggo.it/?sez=XML&p=MapNews",
            {
                "title": "news:title",
                "url": "loc",
                "keywords": "news:keywords",
                "date_xml": ("news:publication_date", ISO_8601_DATE_FORMAT),
            },
        ),
        (
            "https://www.lastampa.it/sitemap.xml",
            {"url": "loc", "date_xml": ("lastmod", ISO_8601_DATE_FORMAT),},
        ),
    ],
    "ja_JP": [
        (
            "https://toyokeizai.net/sitemap.xml",
            {"url": "loc", "date_xml": ("lastmod", ISO_8601_DATE_FORMAT),},
        ),
        (
            "http://www.news24.jp/sitemap_society.xml",
            {
                "url": "loc",
                # don't include title even though xml has it
                # title doesn't have enough info, crawl each instead
                # "title": "news:title",
                "date_xml": ("news:publication_date", ISO_8601_DATE_WITHOUT_SEC_FORMAT),
            },
        ),
        (
            "http://www.news24.jp/sitemap_economy.xml",
            {
                "url": "loc",
                # don't include title even though xml has it
                # title doesn't have enough info, crawl each instead
                # "title": "news:title",
                "date_xml": ("news:publication_date", ISO_8601_DATE_WITHOUT_SEC_FORMAT),
            },
        ),
        (
            "http://www.news24.jp/sitemap_international.xml",
            {
                "url": "loc",
                # don't include title even though xml has it
                # title doesn't have enough info, crawl each instead
                # "title": "news:title",
                "date_xml": ("news:publication_date", ISO_8601_DATE_WITHOUT_SEC_FORMAT),
            },
        ),
    ],
    "ta_IN": [
        (
            "https://www.dailythanthi.com/Sitemap/googlesitemap.xml",
            {
                "title": "news:title",
                "url": "loc",
                "keywords": "news:keywords",
                "date_xml": ("lastmod", ISO_8601_DATE_FORMAT),
            },
        ),
        (
            "https://www.maalaimalar.com/Sitemap/googlesitemap.xml",
            {
                "title": "news:title",
                "url": "loc",
                "keywords": "news:keywords",
                "date_xml": ("lastmod", ISO_8601_DATE_FORMAT),
            },
        ),
        (
            "https://www.hindutamil.in/feed/news-corona-virus-518.xml",
            {
                "title": "news:title",
                "url": "loc",
                "keywords": "news:keywords",
                "date_xml": ("lastmod", ISO_8601_DATE_FORMAT),
            },
        ),
        ("https://www.timestamilnews.com/", {"not_xml": True,},),
    ],
    "th_TH": [
        ("https://thestandard.co/coronavirus-coverage/", {"not_xml": True,},),
        (
            "https://www.thairath.co.th/sitemap-daily.xml",
            {"url": "loc", "title": "image:title",},
        ),
        (
            "https://rss.komchadluek.net/latest_news_google_news.xml",
            {
                "url": "loc",
                "title": "news:title",
                "keywords": "news:keywords",
                "date_xml": ("news:publication_date", ISO_8601_DATE_FORMAT),
            },
        ),
        (
            "https://rss.komchadluek.net/latest_news_google_news.xml",
            {
                "url": "loc",
                "title": "news:title",
                "keywords": "news:keywords",
                "date_xml": ("news:publication_date", ISO_8601_DATE_FORMAT),
            },
        ),
    ],
    "en_MY": [
        (
            "https://www.malaymail.com/sitemap.xml",
            {
                "url": "loc",
                "title": "news:title",
                "keywords": "news:keywords",
                "date_xml": ("news:publication_date", ISO_8601_DATE_FORMAT),
            },
        ),
    ],
    "ms_MY": [
        (
            "https://www.projekmm.com/sitemap.xml",
            {
                "url": "loc",
                "title": "news:title",
                "keywords": "news:keywords",
                "date_xml": ("news:publication_date", ISO_8601_DATE_FORMAT),
            },
        ),
    ],
    "nl_NL": [
        (
            "https://www.nu.nl/sitemap_news.xml",
            {
                "url": "loc",
                "title": "news:title",
                "keywords": "news:keywords",
                "date_xml": ("news:publication_date", ISO_8601_DATE_FORMAT),
            },
        ),
        (
            "https://www.rivm.nl/sitemap.xml",
            {
                "url": "loc",
                "date_xml": ("lastmod", ISO_8601_DATE_FORMAT),
                "custom_blacklist": ["/en/"],
            },
        ),
        (
            "https://www.nrc.nl/sitemap/index.xml",
            {"url": "loc", "date_xml": ("lastmod", ISO_8601_DATE_FORMAT),},
        ),
    ],
    "zh_MY": [
        (
            "https://www.orientaldaily.com.my/sitemap.xml",
            {
                "url": "loc",
                "title": "news:title",
                "date_xml": ("news:publication_date", ISO_8601_DATE_FORMAT),
            },
        ),
    ],
    "vi_VN": [
        ("https://www.tienphong.vn/event/virus-covid19-2302.tpo", {"not_xml": True}),
        (
            "https://baomoi.com/sitemaps/sitemap-news.xml",
            {
                "url": "loc",
                "title": "news:title",
                "keywords": "news:keywords",
                "date_xml": ("news:publication_date", ISO_8601_DATE_WITHOUT_SEC_FORMAT),
            },
        ),
        (
            "https://vnexpress.net/google-news-sitemap.xml",
            {
                "url": "loc",
                "title": "news:title",
                "keywords": "news:keywords",
                "date_xml": ("news:publication_date", ISO_8601_DATE_FORMAT),
            },
        ),
        (
            "https://vietnamnews.vn/sitemap.xml",
            {"url": "loc", "date_xml": ("lastmod", YEAR_MONTH_DAY_FORMAT),},
        ),
    ],
    "zh_CN": [
        (
            "http://www.gov.cn/google.xml",
            {"url": "loc", "date_xml": ("lastmod", ISO_8601_DATE_FORMAT),},
        ),
    ],
    "zh_TW": [
        (
            "https://news.cts.com.tw/sitemap.xml",
            {"url": "loc", "date_xml": ("lastmod", YEAR_MONTH_DAY_FORMAT),},
        ),
        ("https://news.pts.org.tw/dailynews.php", {"not_xml": True},),
        (
            "https://www.taiwannews.com.tw/ch/sitemap.xml",
            {
                "title": "news:title",
                "url": "loc",
                "date_xml": ("news:publication_date", YEAR_MONTH_DAY_FORMAT),
            },
        ),
        (
            "https://www.ettoday.net/news-sitemap.xml",
            {
                "title": "news:title",
                "url": "loc",
                "date_xml": ("news:publication_date", ISO_8601_DATE_WITHOUT_SEC_FORMAT),
            },
        ),
    ],
}

NEWS = Director.construct()