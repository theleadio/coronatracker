# Extracts latest data from JHU G-Sheets based on Maryland Timezone
# https://gisanddata.maps.arcgis.com/apps/opsdashboard/index.html?fbclid=IwAR2mWEw0X_B5jbR0Fm23t2TVJGzVqUY6ok98DzrGLMrMXCR_c5joZV5AdNU#/bda7594740fd40299423467b48e9ecf6

import requests
from datetime import datetime, timedelta

class DatePosted:
    # Data posted by JHU at Maryland. Considering the time difference
    now = datetime.now() - timedelta(hours=16, minutes=0)
    date = now.date()

    # Extract Month and day
    Month = date.strftime("%b")
    day_of_month = date.strftime("%d")


class ExtractTime(DatePosted):
    def am_to_pm(self, am_pm):
        am_pm = ""
        # Extract Time
        if now.hour > 11:
            am_pm = "pm"
        else:
            am_pm = "am"
        return am_pm


class Concat(DatePosted,ExtractTime):
    def concat(self, Month, day_of_month, am_pm):
        # Concat required fields for URL
        date_time_ampm = Month + day_of_month + '_' + "12" + am_pm.lower()

        return date_time_ampm


if __name__== "__main__":

    # Download Contents
    url = 'https://docs.google.com/spreadsheets/d/169AP3oaJZSMTquxtrkgFYMSp4gTApLTTWqo25qCpjL0/gviz/tq?tqx=out:csv&sheet=' + date_time_ampm
    r = requests.get(url, allow_redirects=True)
    open('JHU_data/'+date_time_ampm + '_JHU_data.csv', 'wb').write(r.content)

    dp = DatePosted
    et = ExtractTime
    cc = Concat

    et.am_to_pm(dp.now)
    cc.concat(dp.Month,et.am_pm,dp.day_of_month)
