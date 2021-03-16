from ScrapeRss.globals import (
    ISO_8601_DATE_FORMAT,
    ISO_8601_DATE_WITHOUT_SEC_FORMAT,
    YEAR_MONTH_DAY_FORMAT,
)

class CrawlCheck: # uses letters to represent a given source
def _init_(self, Iscrawl, SourceName, SourceGroup):
self.IsCrawl =IsCrawl # shows wether or not a news source should be crawled
self.SourceName = SourceName #shows source's http source.
self.SourceGroup = SourceGroup #show NEWS_SOURCES group the source belongs to.

#create all instances that represent all sources that were in list

#Crawl
source-a1= CrawlCheck(True, "http://www.dailytelegraph.com.au/news/breaking-news/rss", "en_AU")
source-b1= CrawlCheck(True,"http://www.dailytelegraph.com.au/newslocal/rss","en_AU")
source-c1= CrawlCheck(True,"http://www.news24.jp/sitemap_economy.xml","ja_JP")
source-d1= CrawlCheck(True,"http://www.news24.jp/sitemap_international.xml","ja_JP")
source-e1= CrawlCheck(True,"http://www.news24.jp/sitemap_society.xml","ja_JP")
source-f1= CrawlCheck(True,"http://www.taipeitimes.com/sitemap.xml","en_TW")
source-g1= CrawlCheck(True,"https://baomoi.com/sitemaps/sitemap-news.xml","vi_VN")
source-h1= CrawlCheck(True,"https://news.kompas.com/web/sitemap.xml","id_ID")
source-i1= CrawlCheck(True,"https://toyokeizai.net/sitemap.xml","ja_JP")
source-j1= CrawlCheck(True,"https://vietnamnews.vn/sitemap.xml","vi_VN")

source-k1= CrawlCheck(True,"https://vnexpress.net/google-news-sitemap.xml","vi_VN")
source-l1= CrawlCheck(True,"https://www.channelnewsasia.com/googlenews/cna_news_sitemap.xml","en_SG")
source-m1= CrawlCheck(True,"https://www.ettoday.net/news-sitemap.xml","zh_TW")
source-n1= CrawlCheck(True,"https://www.liputan6.com/sitemap_post.xml","none")
source-o1= CrawlCheck(True,"https://www.news.com.au/content-feeds/latest-news-national/","en_AU")
source-p1= CrawlCheck(True,"https://www.news.com.au/content-feeds/latest-news-world/","en_AU")
source-q1= CrawlCheck(True,"https://www.sbs.com.au/news/topic/latest/feed","en_AU")
source-r1= CrawlCheck(True,"https://www.scmp.com/rss/318208/feed","en_HK")
source-s1= CrawlCheck(True,"https://www.shine.cn/sitemap-news.xml","en_CN")
source-t1= CrawlCheck(True,"https://www.taiwannews.com.tw/ch/sitemap.xml","zh_TW")
source-u1= CrawlCheck(True,"https://www.taiwannews.com.tw/en/sitemap.xml","en_TW")
source-v1= CrawlCheck(True,"https://www.theage.com.au/rss/feed.xml","en_AU")
source-w1= CrawlCheck(True,"https://www.tienphong.vn/event/virus-covid19-2302.tpo","vi_VN")
source-x1= CrawlCheck(True,"http://www.hani.co.kr/arti/RSS/sitemap_www.xml","ko_KR")
source-y1= CrawlCheck(True,"http://www.koreatimes.co.kr/www/rss/world.xml","en_KR")
source-z1= CrawlCheck(True,"http://www.koreatimes.co.kr/www/rss/nation.xml","en_KR")
source-a2= CrawlCheck(True,"http://koreajoongangdaily.joins.com/sitemap_google_news.xml","en_KR")
source-b2= CrawlCheck(True,"https://news.joins.com/sitemap/latest-articles","ko_KR")
source-c2= CrawlCheck(True,"http://www.donga.com/sitemap/donga-newsmap.xml","ko_KR")
source-d2= CrawlCheck(True,"https://news.chosun.com/google/rss.html","ko_KR")
source-e2= CrawlCheck(True,"https://news.chosun.com/site/data/rss/rss.xml","ko_KR")
source-f2= CrawlCheck(True,"http://english.chosun.com/site/data/rss/rss.xml","en_KR")
source-g2= CrawlCheck(True,"https://thestandard.co/coronavirus-coverage/","th_TH")
source-h2= CrawlCheck(True,"https://www.thairath.co.th/sitemap-daily.xml","th_TH")
source-i2= CrawlCheck(True,"https://rss.komchadluek.net/latest_news_google_news.xml","th_TH",)
source-j2= CrawlCheck(True,"https://www.ilmessaggero.it/?sez=XML&p=MapNews","it_IT")
source-k2= CrawlCheck(True,"https://www.leggo.it/?sez=XML&p=MapNews","it_IT")
source-l2= CrawlCheck(True,"https://www.lastampa.it/sitemap.xml","it_IT")
source-m2= CrawlCheck(True,"https://www.malaymail.com/sitemap.xml","en_MY")
source-n2= CrawlCheck(True,"https://www.projekmm.com/sitemap.xml","ms_MW")
source-o2= CrawlCheck(True,"https://www.orientaldaily.com.my/sitemap.xml","zh_MW")
source-p2= CrawlCheck(True,"https://www.welt.de/sitemaps/newssitemap/newssitemap.xml","de_DE")
source-q2= CrawlCheck(True,"https://www.welt.de/sitemaps/sitemap/today.xml","de_DE")
source-r2= CrawlCheck(True,"https://www.focus.de/","de_DE")
source-s2= CrawlCheck(True,"https://www.faz.net/aktuell/","de_DE")
source-t2= CrawlCheck(True,"http://www.gov.cn/google.xml","zh_CN")
source-u2= CrawlCheck(True,"https://www.nu.nl/sitemap_news.xml","nl_NL")
source-v2= CrawlCheck(True,"https://www.rivm.nl/sitemap.xml","nl_NL")
source-w2= CrawlCheck(True,"https://www.nrc.nl/sitemap/index.xml","nl_NL")
source-x2= CrawlCheck(True,"https://www.thehindu.com/sitemap/googlenews.xml","en_IN")
source-y2= CrawlCheck(True,"https://www.dailythanthi.com/Sitemap/googlesitemap.xml","ta_IN")
source-z2= CrawlCheck(True,"https://www.maalaimalar.com/Sitemap/googlesitemap.xml","ta_IN")
source-a3= CrawlCheck(True,"https://www.hindutamil.in/feed/news-corona-virus-518.xml","ta_IN")
source-b3= CrawlCheck(True,"https://www.livehindustan.com/news-sitemap.xml","hi_IN")
source-c3= CrawlCheck(True,"https://www.bhaskar.com/sitemapgoogle/topnews_1.xml","hi_IN")
source-d3= CrawlCheck(True,"https://www.jagran.com/news-sitemap.xml","hi_IN")
source-e3= CrawlCheck(True,"https://www.timestamilnews.com/","ta_IN")

#Don't Crawl
source-f3= CrawlCheck(False,"http://www.heraldsun.com.au/news/breaking-news/rss","en_AU")
source-g3= CrawlCheck(False,"http://www.heraldsun.com.au/rss","en_AU")
source-h3= CrawlCheck(False,"https://www.theage.com.au/rss/world.xml","en_AU")
source-i3= CrawlCheck(False,"http://www.dailytelegraph.com.au/news/national/rss","en_AU")
source-j3= CrawlCheck(False,"http://www.dailytelegraph.com.au/news/world/rss","en_AU")

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
