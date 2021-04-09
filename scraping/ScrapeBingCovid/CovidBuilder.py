class CovidBuilder:
    """
    The Builder interface.
    Concrete classes that implement it include
    those that store scraped covid-19 information
    from the web like the BingCovidBuilder concrete class.
    """
    def add_state(self):
        pass

    def add_country(self):
        pass

    def add_last_update(self):
        pass

    def add_lat(self):
        pass

    def add_lng(self):
        pass

    def add_confirmed(self):
        pass

    def add_deaths(self):
        pass

    def add_recovered(self):
        pass

    def posted_date(self):
        pass

    def build(self):
        pass