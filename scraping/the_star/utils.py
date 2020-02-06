"""
    Copyright 2020 Edmund Hee, All Right Reserved
    Email: edmund.hee05@gmail.com
"""

import datetime
import logging
import pytz


def parse_date(text, tz=None):
    """
    Parse JSON data to date
    :param text: date in string
    :return: datetime object
    """
    if text == '' or text is None:
        return None

    for fmt in ["%A, %d %b %Y %I:%M %p"]:
        try:
            dt = datetime.datetime.strptime(text, fmt)
            if tz:
                timezone = pytz.timezone(tz)
                dt = timezone.localize(dt)
            else:
                dt = dt.replace(tzinfo=None)
            return dt
        except ValueError:
            pass
    return None


def parse_date_to_string(dt, fmt="%Y-%m-%d %H:%M:%S.%f"):
    """
    Convert date time to string format of %Y-%m-%d %H:%M:%S.%f
    :param datetime: datetime object
    :param fmt: datetime format (default: %Y-%m-%d %H:%M:%S.%f)
    :return: string datetime
    """
    try:
        if dt:
            return dt.strftime(fmt)
        else:
            return None
    except Exception as e:
        logging.error("Error: parse_date_to_string Exception - {}".format(str(e)))
        return None
