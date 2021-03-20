# CONSTANT VALUES

import queue


class Globals:

    def __init__(self):
        
        self.__SEED_QUEUE = queue.Queue()
        self.__EXTRACT_QUEUE = queue.Queue()
        self.__RSS_STACK = {}
        self.__CACHE = set()


        # "Sat, 25 Jan 2020 01:52:22 +0000"
        self.__DATE_RFC_2822_REGEX_RULE = r"[\d]{1,2} [ADFJMNOS]\w* [\d]{4} \b(?:[01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9] [\+]{1}[0-9]{4}\b"
        self.__DATE_RFC_2822_DATE_FORMAT = "%d %b %Y %H:%M:%S %z"
        # ISO 8601 | 2020-01-31T22:10:38+0800 | 2020-02-05T08:13:54.000Z | 2017-04-17T22:23:24+00:00
        self.__DATE_ISO_8601_REGEX_RULE = (
            r"\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:?\d{0,2}[\+\.]\d{2,4}\:?[0-9]{0,2}Z?"
        )
        self.__ISO_8601_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
        self.__ISO_8601_DATE_WITHOUT_SEC_FORMAT = "%Y-%m-%dT%H:%M%z"
        self.__DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
        self.__YEAR_MONTH_DAY_FORMAT = "%Y-%m-%d"

        self.__URL_BLACKLIST_KEYWORDS = set(
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
        self.__CORONA_KEYWORDS = set(
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
        self.__SPECIAL_LANG = {
            ("zh", "TW"): "zh_TW",
            ("zh", "CN"): "zh_CN",
            ("zh", "MY"): "zh_CN",
        }

        self.__CACHE_FILE = "cache.txt"
        self.__OUTPUT_FILENAME = "output.jsonl"
        self.__THREAD_LIMIT = 10
        self.__THREAD_TIMEOUT = 180  # seconds
        self.__REQUEST_TIMEOUT = 10
        self.__HEADER = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
        }

    def get_seed_queue(self):
        return self.__SEED_QUEUE
    
    def get_extract_queue(self):
        return self.__EXTRACT_QUEUE
    
    def get_rss_stack(self):
        return self.__RSS_STACK
    
    def get_cache(self):
        return self.__CACHE

    def get_date_rfc_2822_regex_rule(self):
        return self.__DATE_RFC_2822_REGEX_RULE

    def get_date_rfc_2822_date_format(self):
        return self.__DATE_RFC_2822_DATE_FORMAT

    def get_date_iso_8601_regex_rule(self):
        return self.__DATE_ISO_8601_REGEX_RULE

    def get_iso_8601_date_format(self):
        return self.__ISO_8601_DATE_FORMAT

    def get_iso_8601_date_without_sec_format(self):
        return self.__ISO_8601_DATE_WITHOUT_SEC_FORMAT

    def get_date_format(self):
        return self.__DATE_FORMAT

    def get_year_month_day_format(self):
        return self.__YEAR_MONTH_DAY_FORMAT

    def get_url_blacklist_keywords(self):
        return self.__URL_BLACKLIST_KEYWORDS

    def get_corona_keywords(self):
        return self.__CORONA_KEYWORDS

    def get_special_lang(self):
        return self.__SPECIAL_LANG

    def get_cache_file(self):
        return self.__CACHE_FILE

    def get_output_filename(self):
        return self.__OUTPUT_FILENAME

    def get_thread_limit(self):
        return self.__THREAD_LIMIT

    def get_thread_timeout(self):
        return self.__THREAD_TIMEOUT

    def get_request_timeout(self):
        return self.__REQUEST_TIMEOUT

    def get_header(self):
        return self.__HEADER


    

    