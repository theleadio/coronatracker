"The Iterator Pattern Concept"
from abc import ABCMeta, abstractmethod
from temporary_cron import sql_query

class IIterator(metaclass=ABCMeta):
    "An Iterator Interface"
    @staticmethod
    @abstractmethod
    def has_next():
        pass

    @staticmethod
    @abstractmethod
    def next():
        pass

class Iterable(IIterator):
    "The concrete iterator (iterable)"

    def __init__(self, aggregates):
        self.index = 0
        self.aggregates = aggregates

    def next(self):
        if self.index < len(self.aggregates):
            aggregate = self.aggregates[self.index]
            self.index += 1
            return aggregate
        raise Exception("AtEndOfIteratorException", "At End of Iterator")

    def has_next(self):
        return self.index < len(self.aggregates)

class IAggregate(metaclass=ABCMeta):
    "An interface that the aggregates should implement"
    @staticmethod
    @abstractmethod
    def query():
        pass

class Aggregate(IAggregate):
    "A concrete object"
    @staticmethod
    def query(command):
        sql_query(command)
