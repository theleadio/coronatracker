# -*- coding: utf-8 -*-

import appdirs
import re

# Start ignoring PyImportSortBear, PyLintBear as BUS_NAME is imported as a
# constant from other files.
from coala_utils import VERSION
# Stop ignoring

TRUE_STRINGS = ['1',
                "on",
                'y',
                'yes',
                "yeah",
                "sure",
                'true',
                'definitely',
                'yup',
                'right']

FALSE_STRINGS = ['0',
                 'off',
                 'n',
                 'no',
                 'nope',
                 'nah',
                 'false',
                 'wrong',
                 'none']

URL_REGEX = re.compile(
    r'^(?:(?:http|ftp)[s]?://)?'  # scheme
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+'  # domain name
    r'(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
    r'localhost|'  # OR localhost
    r'(?:\d{1,3}\.){3}\d{1,3})'  # OR an ip
    r'(?::\d+)?'  # optional port number
    r'(?:/?|[/?]\S+)$',  # path
    re.IGNORECASE)
