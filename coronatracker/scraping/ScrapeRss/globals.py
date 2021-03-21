# CONSTANT VALUES

import queue

SEED_QUEUE = queue.Queue()
EXTRACT_QUEUE = queue.Queue()
RSS_STACK = {}
CACHE = set()


# "Sat, 25 Jan 2020 01:52:22 +0000"
DATE_RFC_2822_REGEX_RULE = r"[\d]{1,2} [ADFJMNOS]\w* [\d]{4} \b(?:[01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9] [\+]{1}[0-9]{4}\b"
DATE_RFC_2822_DATE_FORMAT = "%d %b %Y %H:%M:%S %z"
# ISO 8601 | 2020-01-31T22:10:38+0800 | 2020-02-05T08:13:54.000Z | 2017-04-17T22:23:24+00:00
DATE_ISO_8601_REGEX_RULE = (
    r"\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:?\d{0,2}[\+\.]\d{2,4}\:?[0-9]{0,2}Z?"
)
ISO_8601_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
ISO_8601_DATE_WITHOUT_SEC_FORMAT = "%Y-%m-%dT%H:%M%z"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
YEAR_MONTH_DAY_FORMAT = "%Y-%m-%d"

URL_BLACKLIST_KEYWORDS = set(
    [
        "/archives/",
        "/videos/",
        "/images/",
        "/author/",
        "facebook.com",
        "twitter.com",
        "youtube.com",
        "/politik/",
        "/print/",
        "/404/",
        "/uploads/",
    ]
)
CORONA_KEYWORDS = set(
    [
        "covid-19",
        "corona virus",
        "coronavirus",
        "武漢肺炎",
        "冠状病毒",
        "新冠肺炎",  # new crown pneumonia (used by orientaldaily)
        "virus corona",
        "viêm phổi",  # pneumonia
        "コロナウィルス",  # coronavirus
        "新型肺炎",  # new pneumonia
        "新型コロナ",  # new corona
        "โคโรน่า",  # corona
        "ไวรัสโคโรนา",  # corona virus
        "โควิด-19",  # covid-19
        "코로나 바이러스",  # coronavirus
        "코로나",  # corona
        "우한 코로나",  # wuhan corona
        "코로나19",  # corona19
        "கொரோனா வைரஸ்",  # corona virus
        "கொரோனா",  # corona
    ]
)
SPECIAL_LANG = {
    ("zh", "TW"): "zh_TW",
    ("zh", "CN"): "zh_CN",
    ("zh", "MY"): "zh_CN",
}

CACHE_FILE = "cache.txt"
OUTPUT_FILENAME = "output.jsonl"
THREAD_LIMIT = 10
THREAD_TIMEOUT = 180  # seconds
REQUEST_TIMEOUT = 10
HEADER = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
}
