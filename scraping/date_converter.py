import re
from datetime import datetime, timezone

# new class created to be referenced
class conv_date
def _init_(self,string,regex,datetimeobject):
        self.string = string
        self.regex = regex
        self.datetimeobject = datetimeobject


datetime_str = all[0] # '09/19/18 13:55:26'

# referencing class conv_date
dateconv = conv_date(x="Sat, 25 Jan 2020 01:52:22 +2000",
y = re.findall(r"[\d]{1,2} [ADFJMNOS]\w* [\d]{4} \b(?:[01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9] [\+]{1}[0-9]{4}\b", str),
z = datetime.strptime(datetime_str, '%d %b %Y %H:%M:%S %z'))

# printing datetime_object from dateconv
print(type(dateconv.z))
print(dateconv.z)  # printed in default format
print(dateconv.z.astimezone(timezone.utc))
