# Extracts latest data from JHU G-Sheets based on Maryland Timezone
# https://gisanddata.maps.arcgis.com/apps/opsdashboard/index.html?fbclid=IwAR2mWEw0X_B5jbR0Fm23t2TVJGzVqUY6ok98DzrGLMrMXCR_c5joZV5AdNU#/bda7594740fd40299423467b48e9ecf6

import requests
from datetime import datetime, timedelta


if __name__== "__main__":
    # Data posted by JHU at Maryland. Considering the time difference
    now = datetime.now() - timedelta(hours=16, minutes=0)

    date = now.date()
    Month = date.strftime("%b")
    day_of_month = date.strftime("%d")
    hour_12 = date.strftime("%I")
    am_pm = date.strftime("%p")

    # Concat required fields for URL
    date_time_ampm = Month + day_of_month + '_' + hour_12 + am_pm.lower()

    # Download Contents
    url = 'https://docs.google.com/spreadsheets/d/169AP3oaJZSMTquxtrkgFYMSp4gTApLTTWqo25qCpjL0/gviz/tq?tqx=out:csv&sheet=' + date_time_ampm
    r = requests.get(url, allow_redirects=True)
    open('JHU_data/'+date_time_ampm + '_JHU_data.csv', 'wb').write(r.content)
