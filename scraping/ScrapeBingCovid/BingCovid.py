from datetime import datetime
from dateutil import parser

class CaseInfo:
    def __init__(
        self,
        confirmed=None,
        deaths=None,
        recovered=None,
        stateInfo=None,
    ):
        self.confirmed = confirmed
        self.deaths = deaths
        self.recovered = recovered
        self.stateInfo = stateInfo

class CountryInfo:
    def __init__(
        self,
        country=None,
        lat=None,
        lng=None,
    ):
        self.country = country
        self.lat = lat
        self.lng = lng


class StateInfo:
    def __init__(
        self,
        state=None,
        countryInfo=None,
    ):
        self.state = state
        self.countryInfo = countryInfo


class BingCovid:
    def __init__(
        self,
        confirmed=None,
        deaths=None,
        recovered=None,
        last_update=None,
        lat=None,
        lng=None,
        state=None,
        country=None,
        posted_date=datetime.utcnow(),
    ):
        self.countryInfo = CountryInfo(country, lat, lng)
        self.stateInfo = StateInfo(state, self.countryInfo)
        self.caseInfo = CaseInfo(confirmed, deaths, recovered, self.stateInfo)

        self.last_update = parser.parse(last_update) if last_update else last_update
        self.posted_date = posted_date

    def getDataAsDict(self):
        rt = {}
        rt["confirmed"] = self.caseInfo.confirmed
        rt["deaths"] = self.caseInfo.deaths
        rt["recovered"] = self.caseInfo.recovered
        rt["last_update"] = self.last_update
        rt["lat"] = self.countryInfo.lat
        rt["lng"] = self.countryInfo.lng
        rt["state"] = self.stateInfo.state
        rt["country"] = self.countryInfo.country
        rt["posted_date"] = self.posted_date
        return rt