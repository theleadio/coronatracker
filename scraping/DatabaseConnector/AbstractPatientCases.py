# Abstract class that is implemented by DatabasePatientCases.

class AbstractPatientCases():

    # The class has-a country
    country = None

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def select(self):
        pass

    @abstractmethod
    def insert(self):
        pass