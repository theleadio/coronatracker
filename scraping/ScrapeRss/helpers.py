from ScrapeRss.globals import DATE_FORMAT, URL_BLACKLIST_KEYWORDS, CORONA_KEYWORDS
from ScrapeRss.globals import (
    DATE_RFC_2822_DATE_FORMAT,
    DATE_RFC_2822_REGEX_RULE,
    DATE_ISO_8601_REGEX_RULE,
    ISO_8601_DATE_FORMAT,
)
from ScrapeRss.globals import REQUEST_TIMEOUT, HEADER

from newspaper import Article

from datetime import datetime, timezone
from dateutil import parser
import logging
import requests
import re

TODAY_TIME = datetime.now()


def is_valid_url(url, blacklist):
    # not empty
    if len(url.strip()) == 0:
        return False

    # TODO
    # incorrect domain (link to other sites)
    # domain = re.findall(r"^(?:https?:\/\/)?(?:www\.)?([^:\/?\n]+)", url, re.IGNORECASE)
    # root_domain = re.findall(r"^(?:https?:\/\/)?(?:www\.)?([^:\/?\n]+)", root_url, re.IGNORECASE)
    # logging.debug("URL: {}. DOMAIN: {}, ROOT_DOMAIN: {}".format(url, domain, root_domain))

    # missing http(s):// or contain blacklist
    if not re.findall(
        r"^https?://", url, re.IGNORECASE
    ) or is_blacklist_keywords_in_url(url, blacklist):
        return False
    return True


def is_blacklist_keywords_in_url(url, blacklist):
    # global blacklist and site specific blacklist
    for keyword in blacklist.union(URL_BLACKLIST_KEYWORDS):
        if keyword in url:
            return True
    return False


def get_title_from_for_html(node):
    title = node.find("title")
    if not title:
        title = node.find("h1")
    if not title:
        title = node.find("h2")
    return title.text if title else ""


def get_description_from_for_html(node):
    description = node.find("p")
    return description.text if description else ""


def get_seed_page(url):
    try:
        logging.debug("Get seed url: {}".format(url))
        res = requests.get(url, headers=HEADER, timeout=REQUEST_TIMEOUT)
        return res
    except Exception as e:
        logging.error("Fail to get url: {}".format(url))
        raise e


def corona_keyword_exists_in_string(string):
    # this works well if for words that are split by space/comma
    # fails for languages that doesn't need space/comma
    # hence, do brute force to check keyword in string
    # eg: 武漢肺炎中國確診逾, where 武漢肺炎 is coronavirus
    if len(set(re.findall(r"\w+", string)).intersection(CORONA_KEYWORDS)) != 0:
        return True
    # Fallback: if can't find, search each keyword in string, brute force
    for keyword in CORONA_KEYWORDS:
        if keyword in string:
            return True
    return False


def valid_dt_value(dt_object):
    # this function is to capture if we got the dt object from
    # %Y-%m-%d (without any timezone information)
    # if no timezone, return invalid, try to find from soup page or meta
    if dt_object.hour == 0 and dt_object.minute == 0 and dt_object.second == 0:
        return False
    return True


def attempt_extract_from_meta_data(meta_data, attribute, original_value):
    logging.debug(
        "Start attempt look for attribute: {}. Original value: {}".format(
            attribute, original_value if original_value else "None"
        )
    )

    # in meta_data
    if attribute in meta_data and isinstance(meta_data[attribute], str):
        logging.debug(
            "Found attribute: {} in meta_data. value: {}".format(
                attribute, meta_data[attribute]
            )
        )
        return meta_data[attribute]

    # try og tag
    if (
        "og" in meta_data
        and attribute in meta_data["og"]
        and len(meta_data["og"][attribute].strip())
    ):
        logging.debug(
            "Found attribute: {} in og. value: {}".format(
                attribute, meta_data["og"][attribute]
            )
        )
        return meta_data["og"][attribute]

    # article tag
    if (
        "article" in meta_data
        and attribute in meta_data["article"]
        and len(meta_data["article"][attribute].strip())
    ):
        logging.debug(
            "Found attribute: {} in article. value: {}".format(
                attribute, meta_data["article"][attribute]
            )
        )
        return meta_data["article"][attribute]

    # if all fails, return default value
    logging.debug(
        "Fail to find attribute: {} using default value: {}".format(
            attribute, original_value
        )
    )
    return original_value


def convert_date_to_datetime_object(date_string):
    if not isinstance(date_string, str):
        # could already be a datetime object as initial value extracted in NewsParser
        logging.debug(
            "Input date already in datetime value: {}. UTC: {}. Skipping convertion...".format(
                date_string, date_string.astimezone(timezone.utc)
            )
        )
        return date_string.astimezone(timezone.utc)
    return parser.parse(date_string).astimezone(timezone.utc)


def is_article_uploaded_today(dt_object):
    if dt_object is None:
        return True
    if (
        dt_object.year != TODAY_TIME.year
        or dt_object.month != TODAY_TIME.month
        or abs(dt_object.day - TODAY_TIME.day) > 2
    ):
        return False
    return True


def get_title_from_article(article, news_object):
    if article.title:
        return article.title

    return attempt_extract_from_meta_data(article.meta_data, "title", news_object.title)


def get_published_at_value(published_at_dt_object, article, soup_page):
    published_at_value = ""
    published_at_source = ""
    dt_object = published_at_dt_object
    if dt_object and valid_dt_value(dt_object):
        dt_object = convert_date_to_datetime_object(dt_object)
        source = "from seed page"

    elif attempt_extract_from_meta_data(article.meta_data, "publish-date", dt_object):
        dt_object = convert_date_to_datetime_object(
            attempt_extract_from_meta_data(article.meta_data, "publish-date", dt_object)
        )
        source = "meta_data -> published-date"

    elif attempt_extract_from_meta_data(article.meta_data, "published_time", dt_object):
        dt_object = convert_date_to_datetime_object(
            attempt_extract_from_meta_data(
                article.meta_data, "published_time", dt_object
            )
        )
        source = "meta_data -> published_time"

    elif attempt_extract_from_meta_data(article.meta_data, "modified_time", dt_object):
        dt_object = convert_date_to_datetime_object(
            attempt_extract_from_meta_data(
                article.meta_data, "modified_time", dt_object
            )
        )
        source = "meta_data -> modified_time"

    elif soup_page.lastBuildDate:
        dt_object = convert_date_to_datetime_object(soup_page.lastBuildDate.text)
        source = "soup_page -> lastBuildDate"

    else:
        # Worst case: put current date and tmie
        # Reason: since we're constantly crawling (on cron)
        #           sites that publishes latest articles only
        #           it's highly likely we're getting today's article
        dt_object = datetime.utcnow()
        source = "None, using current time."

    published_at_log_msg = "Found publishedAt in: {} with unix timestamp value: {} | Current unix timestamp: {} | Is timestamp > current timestamp: {}"
    unix_extracted = datetime.timestamp(dt_object)
    unix_now = datetime.timestamp(datetime.utcnow())
    if unix_extracted < unix_now:
        logging.debug(
            published_at_log_msg.format(
                source, unix_extracted, unix_now, unix_extracted > unix_now,
            )
        )
    else:
        logging.warning(
            published_at_log_msg.format(
                "meta_data -> modified_time",
                unix_extracted,
                unix_now,
                unix_extracted > unix_now,
            )
        )

    # reset if extracted time is greater than current time
    if unix_extracted > unix_now:
        logging.warning(
            "Extracted timestamp is greater than current timestamp. Resetting to current timestamp"
        )
        dt_object = datetime.utcnow()
    return str(dt_object.strftime(DATE_FORMAT))


def get_author_value(author_default_value, article):
    author_value = author_default_value
    if author_default_value:
        source = "from seed page -> author"

    elif attempt_extract_from_meta_data(article.meta_data, "author", author_value):
        author_value = attempt_extract_from_meta_data(
            article.meta_data, "author", get_author_value
        )
        source = "meta_data -> author"

    elif article.authors:
        author_value = " ".join(article.authors)
        source = "article -> authors"
    else:
        source = "author not found."

    logging.debug("Found author in: {} ".format(source))
    return author_value


def extract_article(link):
    logging.debug("Extracting from: {}".format(link))
    try:
        article = Article(link, headers=HEADER)
        # Do some NLP
        article.download()  # Downloads the link's HTML content
        article.parse()  # Parse the article
        article.nlp()  # Keyword extraction wrapper
    except Exception as e:
        logging.error("Fail to extract Article. Error: {}".format(e))
        return None, False
    return article, True
