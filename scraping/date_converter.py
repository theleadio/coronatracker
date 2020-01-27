import re
from datetime import datetime

str = "Sat, 25 Jan 2020 01:52:22 +0000"
all = re.findall(r"[\d]{1,2} [ADFJMNOS]\w* [\d]{4} \b(?:[01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]\b", str)



datetime_str = all[0] # '09/19/18 13:55:26'

datetime_object = datetime.strptime(datetime_str, '%d %b %Y %H:%M:%S')

print(type(datetime_object))
print(datetime_object)  # printed in default format
