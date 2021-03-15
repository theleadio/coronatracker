# Start ignoring PyImportSortBear because of dependency chains!
from coala_utils.string_processing.Match import Match
from coala_utils.string_processing.InBetweenMatch import InBetweenMatch
from coala_utils.string_processing.Core import (
     search_for, unescaped_search_for, split, unescaped_split,
     search_in_between, unescaped_search_in_between, nested_search_in_between,
     escape, convert_to_raw, unescape, unescaped_rstrip, unescaped_strip,
     position_is_escaped)
# Stop ignoring
