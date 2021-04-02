# Extracts latest data from JHU G-Sheets based on Maryland Timezone
# https://gisanddata.maps.arcgis.com/apps/opsdashboard/index.html?fbclid=IwAR2mWEw0X_B5jbR0Fm23t2TVJGzVqUY6ok98DzrGLMrMXCR_c5joZV5AdNU#/bda7594740fd40299423467b48e9ecf6

import requests
from datetime import datetime, timedelta

class JHUGsheetDataExtraction():

    def __init__(self):
        self.now = datetime.now() - timedelta(hours=16, minutes=0)
        self.date = now.date()

        #Extract Month and day
        Month = date.strftime("%b")
        day_of_month = date.strftime("%d")

        am_pm = ""
        #Extract Time
        if now.hour > 11:
            am_pm = "pm"
        else:
            am_pm = "am"

        # Concat required fields for URL
        self.date_time_ampm = Month + day_of_month + '_' + "12" + am_pm.lower()

        print(self.date_time_ampm)

    def download(self):
        # Download Contents
        url = 'https://docs.google.com/spreadsheets/d/169AP3oaJZSMTquxtrkgFYMSp4gTApLTTWqo25qCpjL0/gviz/tq?tqx=out:csv&sheet=' + self.date_time_ampm
        r = requests.get(url, allow_redirects=True)
        open('JHU_data/'+self.date_time_ampm + '_JHU_data.csv', 'wb').write(r.content)


