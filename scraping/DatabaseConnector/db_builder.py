from abc import ABCMeta, abstractmethod

class SQLBuilder(metaclaass=ABCMeta):
    #The Builder interface

    @staticmethod
    @abstractmethod
    def build_state():
        pass

    @staticmethod
    @abstractmethod
    def build_country():
        pass

    @staticmethod
    @abstractmethod
    def build_last_update():
        pass

    @staticmethod
    @abstractmethod
    def build_lat():
        pass

    @staticmethod
    @abstractmethod
    def build_lng():
        pass

    @staticmethod
    @abstractmethod
    def build_confirmed():
        pass

    @staticmethod
    @abstractmethod
    def build_deaths():
        pass

    @staticmethod
    @abstractmethod
    def build_recovered():
        pass

    @staticmethod
    @abstractmethod
    def build_posted_date():
        pass
    
    @staticmethod
    @abstractmethod
    def build_case():
        pass
    
    @staticmethod
    @abstractmethod
    def build_status_date():
        pass

    @staticmethod
    @abstractmethod
    def build_confirmed_date():
        pass

    @staticmethod
    @abstractmethod
    def build_nationality():
        pass

    @staticmethod
    @abstractmethod
    def build_age():
        pass

    @staticmethod
    @abstractmethod
    def build_gender():
        pass

    @staticmethod
    @abstractmethod
    def build_hospital():
        pass

    @staticmethod
    @abstractmethod
    def build_description():
        pass
    
    @staticmethod
    @abstractmethod
    def build_increment_count():
        pass

    @staticmethod
    @abstractmethod
    def build_total_count():
        pass

    @staticmethod
    @abstractmethod
    def build_hospital_count():
        pass

    @staticmethod
    @abstractmethod
    def build_recovered_count():
        pass

    @staticmethod
    @abstractmethod
    def build_death_count():
        pass

    @staticmethod
    @abstractmethod
    def build_last_updated():
        pass

    @staticmethod
    @abstractmethod
    def get_result(self):
        pass

class ConcreteSQLBuilder(SQLBuilder):
    #The Concrete Builder

    def __init__(self):
        self.product = Product()

    def build_state(self):
        self.product.parts["state": None]
        return self

    def build_country(self):
        self.product.parts["country": None]
        return self

    def build_last_update(self):
        self.product.parts["last_update": None]
        return self

    def build_lat(self):
        self.product.parts["lat": None]
        return self

    def build_lng(self):
        self.product.parts["lng": None]

    def build_confirmed(self):
        self.product.parts["confirmed": None]
        return self

    def build_deaths(self):
        self.product.parts["deaths": None]
        return self

    def build_recovered(self):
        self.product.parts["recovered": None]
        return self

    def build_posted_date(self):
        self.product.parts["posted_date": None]
        return self

    def build_case(self):
        self.product.parts["case": None]
        return self

    def build_status_date(self):
        self.product.parts["status_date": None]
        return self

    def build_confirmed_date(self):
        self.product.parts["confirmed_date": None]
        return self

    def build_nationality(self):
        self.product.parts["nationality": None]
        return self

    def build_age(self):
        self.product.parts["age": None]
        return self

    def build_gender(self):
        self.product.parts["gender": None]
        return self

    def build_hospital(self):
        self.product.parts["hospital": None]
        return self

    def build_description(self):
        self.product.parts["description": None]
        return self

    def build_increment_count(self):
        self.product.parts["increment_count": None]
        return self

    def build_total_count(self):
        self.product.parts["total_count": None]
        return self

    def build_hospital_count(self):
        self.product.parts["hospital_count": None]
        return self

    def build_recovered_count(self):
        self.product.parts["recovered_count": None]
        return self

    def build_death_count(self):
        self.product.parts["death_count": None]
        return self

    def build_last_updated(self):
        self.product.parts["last_updated": None]
        return self

    def get_result(self):
        return self.product


class Product():
    #The Product
    def __init__(self):
        self.parts = {}
    
class Director:
    #The Director
    
    @staticmethod
    def construct_bc():
        return SQLBuilder()\
            .build_state()\
            .build_country()\
            .build_last_update()\
            .build_lat()\
            .build_lng()\
            .build_confirmed()\
            .build_deaths()\
            .build_recovered()\
            .build_posted_date()\
            .build_state()\
            .build_country()\
            .build_confirmed()\
            .build_deaths()\
            .build_recovered()\
            .get_result()
    
    @staticmethod
    def construct_mpc():
        return SQLBuilder()\
            .build_case()\
            .build_status()\
            .build_status_date()\
            .build_confirmed_date()\
            .build_nationality()\
            .build_age()\
            .build_gender()\
            .build_hospital()\
            .build_description()\
            .build_case()\
            .build_status()\
            .build_status_date()\
            .build_confirmed_date()\
            .build_nationality()\
            .build_age()\
            .build_gender()\
            .build_hospital()\
            .build_description()\
            .get_result()
    
    @staticmethod
    def construct_ms():
        return SQLBuilder()\
            .build_state()\
            .build_increment_count()\
            .build_total_count()\
            .build_hospital_count()\
            .build_recovered_count()\
            .build_death_count()\
            .build_last_updated()\
            .build_state()\
            .build_increment_count()\
            .build_total_count()\
            .build_hospital_count()\
            .build_recovered_count()\
            .build_death_count()\
            .get_result()