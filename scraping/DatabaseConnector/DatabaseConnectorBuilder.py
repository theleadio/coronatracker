class DatabaseConnectorBuilder(ConnectorBuilder):
    #dbconnector builder

    def __init__(self):
        self =self

    def get_title(self,title):
        self.title=title

    def get_description(self,description):
        self.description=description

    def get_author(self,author):
        self.author=author

    def get_url(self,url):
        self.url=url

    def get_content(self,content):
        self.content=content

    def get_urlToImage(self,urlToImage):
        self.urlToImage=urlToImage

    def get_publishedAt(self,publishedAt):
        self.publishedAt=publishedAt

    def get_addedOn(self,addedOn):
        self.addedOn=addedOn

    def get_siteName(self,siteName):
        self.siteName=siteName

    def get_language(self,language):
        self.language=language

    def get_countryCode(self,countryCod):
        self.countryCod=countryCod

    def get_country(self,country):
        self.country=country

    def get_total_cases(self,total_cases):
        self.total_cases=total_cases

    def get_total_deaths(self,total_deaths):
        self.total_deaths=total_deaths

    def get_total_recovered(self,total_recovered):
        self.total_recovered=total_recovered

    def get_total_tests(self,total_tests):
        self.total_tests=total_tests

    def get_new_cases(self,new_cases):
        self.new_cases=new_cases

    def get_new_deaths(self,new_deaths):
        self.new_deaths=new_deaths

    def get_active_cases(self,active_cases):
        self.active_cases=active_cases

    def get_serious_critical_cases(self,serious_critical_cases):
        self.serious_critical_cases=serious_critical_cases

    def get_total_cases_per_million_pop(self,total_cases_per_million_pop):
        self.total_cases_per_million_pop=total_cases_per_million_pop

    def get_total_deaths_per_million_pop(self,total_deaths_per_million_pop):
        self.total_deaths_per_million_pop=total_deaths_per_million_pop

    def get_total_tests_per_million_pop(self,total_tests_per_million_pop):
        self.total_tests_per_million_pop=total_tests_per_million_pop

    def get_last_updated(self,last_updated):
        self.last_updated=last_updated

class Build:
    #build method

    def build_news_article():
        return ConnectorBuilder()\
                .get_title()\
                .get_description()\
                .get_url()\
                .get_content()\
                .get_urlToImage()\
                .get_publishedAt()\
                .get_addedOn()\
                .get_siteName()\
                .get_language()\
                .get_countryCode()\
                .get_title()\
                .get_description()\
                .get_content()\
                .get_urlToImage()\
                .get_publishedAt()\
                .get_addedOn()\
                .get_siteName()\
                .get_language()\
                .get_countryCode()\

    def build_worldometer_stats():
        return ConnectorBuilder()\
                .get_country()\
                .get_total_cases()\
                .get_total_deaths()\
                .get_total_recovered()\
                .get_total_tests()\
                .get_new_cases()\
                .get_new_deaths()\
                .get_active_cases()\
                .get_serious_critical_cases()\
                .get_total_cases_per_million_pop()\
                .get_total_deaths_per_million_pop()\
                .get_total_tests_per_million_pop()\
                .get_last_updated()\
                .get_country()\
                .get_total_cases()\
                .get_total_deaths()\
                .get_total_recovered()\
                .get_total_tests()\
                .get_new_cases()\
                .get_new_deaths()\
                .get_active_cases()\
                .get_serious_critical_cases()\
                .get_total_cases_per_million_pop()\
                .get_total_deaths_per_million_pop()\
                .get_total_tests_per_million_pop()\

    def build_worldometers_total_sum():
        return ConnectorBuilder()\
                .get_total_cases()\
                .get_total_deaths()\
                .get_total_recovered()\
                .get_total_tests()\
                .get_new_cases()\
                .get_new_deaths()\
                .get_active_cases()\
                .get_serious_critical_cases()\
                .get_total_cases_per_million_pop()\
                .get_total_deaths_per_million_pop()\
                .get_total_tests_per_million_pop()\
                .get_last_updated()\
                .get_total_cases()\
                .get_total_deaths()\
                .get_total_recovered()\
                .get_total_tests()\
                .get_new_cases()\
                .get_new_deaths()\
                .get_active_cases()\
                .get_serious_critical_cases()\
                .get_total_cases_per_million_pop()\
                .get_total_deaths_per_million_pop()\
                .get_total_tests_per_million_pop()\
