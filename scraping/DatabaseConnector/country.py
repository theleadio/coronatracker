import mysql.connector
import json

class Country():
    def __init__(self,country):
            self.country=country
            self.language=language
            self.countryCode=countryCode
            self.url=url
            self.keyword=keyword
            self.total_case=total_case
            self.total_deaths=total_deaths
            self.total_recovered=total_recovered

    #insert a country to the data base
    def insert(self,country):
        if country not in DatabaseConnector.connect.mysql
            DatabaseConnector.connect.mysql.append(country)

    #delete a country to the data base
    def delete(self,country):
        try:
            DatabaseConnector.connect.mysql.remove(country)
        except ValueError:
            pass

class Data(Country):
    def __init__(self,name=''):
        Country.__init__(self)
        self.name=name
        self._data=''

    def data(self):
        return self._data

    def data(self,language,countryCode,url,keyword,total_case,total_deaths,total_recovered):
        self._data=(data_dict["language"],
                    data_dict["countryCode"],
                    data_dict["url"],
                    data_dict["keyword"],
                    data_dict["total_case"],
                    data_dict["total_deaths"],
                    data_dict["total_recovered"],
                    )
