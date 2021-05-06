from ScrapeRss.globals import (
    ISO_8601_DATE_FORMAT,
    ISO_8601_DATE_WITHOUT_SEC_FORMAT,
    YEAR_MONTH_DAY_FORMAT,
)
import rss_sites
from contracts import contract




# Preconditions: IsCrawl should be a boolean whose value is determined by whether or not the site is crawled. SourceName should be non empty (as shown in the contract) and should be a valid link that leads to a valid site. SourceGroup should also be a non empty string that is also a valid locale.
@contract(IsCrawl='boolean',SourceGroup='str[>0]',SourceName='str[>0]')
class WebsiteInfo: # Uses name of website in the links, along with extra tidbits to deal with similar links.

def _init_(self, IsCrawl, SourceName, SourceGroup):
self.IsCrawl =IsCrawl # shows wether or not a news source should be crawled
self.SourceName = SourceName #shows source's http source.
self.SourceGroup = SourceGroup #show NEWS_SOURCES group the source belongs to.

#Create all instances that represent all sources that were in list.

#Crawl
dailytelegraph-breaking= WebsiteInfo(True, "http://www.dailytelegraph.com.au/news/breaking-news/rss", "en_AU")
dailytelegraph-local= WebsiteInfo(True,"http://www.dailytelegraph.com.au/newslocal/rss","en_AU")
news24-economy= WebsiteInfo(True,"http://www.news24.jp/sitemap_economy.xml","ja_JP")
news24-international= WebsiteInfo(True,"http://www.news24.jp/sitemap_international.xml","ja_JP")
news24-society= WebsiteInfo(True,"http://www.news24.jp/sitemap_society.xml","ja_JP")
taipietimes= WebsiteInfo(True,"http://www.taipeitimes.com/sitemap.xml","en_TW")
baomoi= WebsiteInfo(True,"https://baomoi.com/sitemaps/sitemap-news.xml","vi_VN")
kompas= WebsiteInfo(True,"https://news.kompas.com/web/sitemap.xml","id_ID")
toyokeizai= WebsiteInfo(True,"https://toyokeizai.net/sitemap.xml","ja_JP")
vietnamnews= WebsiteInfo(True,"https://vietnamnews.vn/sitemap.xml","vi_VN")

vnexpress= WebsiteInfo(True,"https://vnexpress.net/google-news-sitemap.xml","vi_VN")
channelnewsasia= WebsiteInfo(True,"https://www.channelnewsasia.com/googlenews/cna_news_sitemap.xml","en_SG")
ettoday= WebsiteInfo(True,"https://www.ettoday.net/news-sitemap.xml","zh_TW")
liputan6= WebsiteInfo(True,"https://www.liputan6.com/sitemap_post.xml","none")
news-national= WebsiteInfo(True,"https://www.news.com.au/content-feeds/latest-news-national/","en_AU")
news-world= WebsiteInfo(True,"https://www.news.com.au/content-feeds/latest-news-world/","en_AU")
sbs= WebsiteInfo(True,"https://www.sbs.com.au/news/topic/latest/feed","en_AU")
scmp= WebsiteInfo(True,"https://www.scmp.com/rss/318208/feed","en_HK")
shine= WebsiteInfo(True,"https://www.shine.cn/sitemap-news.xml","en_CN")
taiwannews-ch= WebsiteInfo(True,"https://www.taiwannews.com.tw/ch/sitemap.xml","zh_TW")
taiwannews-en= WebsiteInfo(True,"https://www.taiwannews.com.tw/en/sitemap.xml","en_TW")
theage-feed= WebsiteInfo(True,"https://www.theage.com.au/rss/feed.xml","en_AU")
teinphong= WebsiteInfo(True,"https://www.tienphong.vn/event/virus-covid19-2302.tpo","vi_VN")
hani= WebsiteInfo(True,"http://www.hani.co.kr/arti/RSS/sitemap_www.xml","ko_KR")
koreatimes-world= WebsiteInfo(True,"http://www.koreatimes.co.kr/www/rss/world.xml","en_KR")
koreatimes-nation= WebsiteInfo(True,"http://www.koreatimes.co.kr/www/rss/nation.xml","en_KR")
koreajoongangdaily= WebsiteInfo(True,"http://koreajoongangdaily.joins.com/sitemap_google_news.xml","en_KR")
joins= WebsiteInfo(True,"https://news.joins.com/sitemap/latest-articles","ko_KR")
donga= WebsiteInfo(True,"http://www.donga.com/sitemap/donga-newsmap.xml","ko_KR")
chosun-google= WebsiteInfo(True,"https://news.chosun.com/google/rss.html","ko_KR")
chosun-site= WebsiteInfo(True,"https://news.chosun.com/site/data/rss/rss.xml","ko_KR")
chosun-english= WebsiteInfo(True,"http://english.chosun.com/site/data/rss/rss.xml","en_KR")
thestandard= WebsiteInfo(True,"https://thestandard.co/coronavirus-coverage/","th_TH")
thairath= WebsiteInfo(True,"https://www.thairath.co.th/sitemap-daily.xml","th_TH")
komchadluek= WebsiteInfo(True,"https://rss.komchadluek.net/latest_news_google_news.xml","th_TH",)
ilmessaggero= WebsiteInfo(True,"https://www.ilmessaggero.it/?sez=XML&p=MapNews","it_IT")
leggo= WebsiteInfo(True,"https://www.leggo.it/?sez=XML&p=MapNews","it_IT")
lastampa= WebsiteInfo(True,"https://www.lastampa.it/sitemap.xml","it_IT")
malaymail= WebsiteInfo(True,"https://www.malaymail.com/sitemap.xml","en_MY")
projekmm= WebsiteInfo(True,"https://www.projekmm.com/sitemap.xml","ms_MW")
orientaldaily= WebsiteInfo(True,"https://www.orientaldaily.com.my/sitemap.xml","zh_MW")
welt-newssitemap= WebsiteInfo(True,"https://www.welt.de/sitemaps/newssitemap/newssitemap.xml","de_DE")
welt-sitemap= WebsiteInfo(True,"https://www.welt.de/sitemaps/sitemap/today.xml","de_DE")
focus= WebsiteInfo(True,"https://www.focus.de/","de_DE")
faz= WebsiteInfo(True,"https://www.faz.net/aktuell/","de_DE")
gov= WebsiteInfo(True,"http://www.gov.cn/google.xml","zh_CN")
nu= WebsiteInfo(True,"https://www.nu.nl/sitemap_news.xml","nl_NL")
rivm= WebsiteInfo(True,"https://www.rivm.nl/sitemap.xml","nl_NL")
nrc= WebsiteInfo(True,"https://www.nrc.nl/sitemap/index.xml","nl_NL")
thehindu= WebsiteInfo(True,"https://www.thehindu.com/sitemap/googlenews.xml","en_IN")
dailythanthi= WebsiteInfo(True,"https://www.dailythanthi.com/Sitemap/googlesitemap.xml","ta_IN")
maalaimalar= WebsiteInfo(True,"https://www.maalaimalar.com/Sitemap/googlesitemap.xml","ta_IN")
hindutamil= WebsiteInfo(True,"https://www.hindutamil.in/feed/news-corona-virus-518.xml","ta_IN")
livehindustan= WebsiteInfo(True,"https://www.livehindustan.com/news-sitemap.xml","hi_IN")
bhaskar= WebsiteInfo(True,"https://www.bhaskar.com/sitemapgoogle/topnews_1.xml","hi_IN")
jagran= WebsiteInfo(True,"https://www.jagran.com/news-sitemap.xml","hi_IN")
timestamilnews= WebsiteInfo(True,"https://www.timestamilnews.com/","ta_IN")

#Don't Crawl
heraldsun-breaking= WebsiteInfo(False,"http://www.heraldsun.com.au/news/breaking-news/rss","en_AU")
heraldsun= WebsiteInfo(False,"http://www.heraldsun.com.au/rss","en_AU")
theage= WebsiteInfo(False,"https://www.theage.com.au/rss/world.xml","en_AU")
dailytelegraph-national= WebsiteInfo(False,"http://www.dailytelegraph.com.au/news/national/rss","en_AU")
dailytelegraph-world= WebsiteInfo(False,"http://www.dailytelegraph.com.au/news/world/rss","en_AU")

