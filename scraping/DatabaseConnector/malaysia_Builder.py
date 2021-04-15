from abc import ABCMeta, abstractmethod
#Builder Interface
class IBuilder(metaclass=ABCMeta):
    "The Builder Interface"

    @staticmethod
    @abstractmethod
    def add_case():
        pass

    @staticmethod
    @abstractmethod
    def add_status():
        pass

    @staticmethod
    @abstractmethod
    def add_status_date():
        pass
    
    @staticmethod
    @abstractmethod
    def add_confirmed_date():
        pass

    @staticmethod
    @abstractmethod
    def add_nationality():
        pass

    @staticmethod
    @abstractmethod
    def add_age():
        pass

    @staticmethod
    @abstractmethod
    def add_gender():
        pass

    @staticmethod
    @abstractmethod
    def add_hospital():
        pass

    @staticmethod
    @abstractmethod
    def add_description():
        pass


    @staticmethod
    @abstractmethod
    def add_state():
        pass

   @staticmethod
   @abstractmethod
    def add_increment_count():
        pass

    @staticmethod
    @abstractmethod
    def add_total_count():
        pass

    @staticmethod
    @abstractmethod
    def add_hospital_count():
        pass
    
    @staticmethod
    @abstractmethod
    def add_recovered_count():
        pass
    
    @staticmethod
    @abstractmethod
    def add_death_count():
        pass

    @staticmethod
    @abstractmethod
    def add_last_updated():
        pass

    @staticmethod
    @abstractmethod
    def get_result():
        pass

class Builder(IBuilder):
    "The Concrete Builder."

    #Attributes


    def __init__(self):
        self.product = Product()

   
    def build_case():
        self.product.parts["case": None]
        return self

  
    def build_status():
        self.product.parts["status": None]
        return self

  
    def build_status_date(self):
        self.product.parts["status_date": None]
        return self
    
    def build_confirmed_date(self):
        self.product.parts["gender": None]
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


    def build_state(self):
        self.product.parts["state": None]
        return self

    def build_increment_count(self):
        self.product.parts["increment_count": None]
        return self

    def build_total_count(self):
        self.product.parts["total_count": None]
        return self
    
    def build_hospital_count(self):
        self.product.parts.product.parts["hospital_count": None]
        return self
    
    def build_recovered_count(self):
        self.product.parts.product.parts["recovered_count": None]
        return self

    def build_death_count(self):
        self.product.parts.product.parts["death_count": None]
        return self
    
    def build_last_updated(self):
        self.product.parts.product.parts["last_updated": None]
        return self

    def get_result(self):
        return self.product

class Product():
    "The Product"

    def __init__(self):
        self.parts = []

class Director:
    "The Director, building a complex representation."

    @staticmethod
    def construct_mpc():
        "Constructs and returns the final product"
        return Builder()\
            .build_case()\
            .build_status()\
            .build_status_date()\
            .build_confirmed_date()\
            .build_nationality()\
            .build_age()\
            .build_gender()\
            .build_hospital()\
            .build_description()\
     def construct_ms():
        "Constructs and returns the final product"
        return Builder()\
            .build_state()\
            .build_increment_count()\
            .build_total_count()\
            .build_hospital_count()\
            .build_recovered_count()\
            .build_death_count()\
            .build_last_updated()\
            .get_result()

# The Client
PRODUCT = Director.construct()
print(PRODUCT.parts)
