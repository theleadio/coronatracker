from __future__ import annotations
from abc import ABC, abstractmethod
import json
import mysql.connector
from webscraper import insert


class Context:
    """
    The Context defines the interface of interest to clients. It also maintains
    a reference to an instance of a State subclass, which represents the current
    state of the Context.
    """

    _state = None
    """
    A reference to the current state of the Context.
    """

    def __init__(self, state: State) -> None:
        self.transition_to(state)

    def transition_to(self, state: State):
        """
        The Context allows changing the State object at runtime.
        """

        print(f"Context: Transition to {type(state).__name__}")
        self._state = state
        self._state.context = self

    """
    The Context delegates part of its behavior to the current State object.
    """

    def request_connect(self):
        self._state.connectDB()

    def request_save_to_db(self):
        self._state.saveDB()


class State(ABC):
    """
    The base State class declares methods that all Concrete State should
    implement and also provides a backreference to the Context object,
    associated with the State. This backreference can be used by States to
    transition the Context to another State.
    """

    @property
    def context(self) -> Context:
        return self._context

    @context.setter
    def context(self, context: Context) -> None:
        self._context = context

    @abstractmethod
    def connectDB(self) -> None:
        pass

    @abstractmethod
    def saveDB(self) -> None:
        pass


"""
Concrete States implement various behaviors, associated with a state of the
Context.
"""


class ConcreteConnectState(State):
    def connectDB(self) -> None:
        path_to_json = "./db.json"

        with open(path_to_json, "r") as handler:
            info = json.load(handler)
            print(info)

        mydb = mysql.connector.connect(
            host=info["host"],
            user=info["user"],
            passwd=info["passwd"],
            database=info["database"],
        )

        print(mydb)
        print("ConcreteStateA handles request1.")
        print("ConcreteStateA wants to change the state of the context.")
        self.context.transition_to(ConcreteSaveState())

    def saveDB(self) -> None:
        print("ConcreteStateA handles request2.")


class ConcreteSaveState(State):
    def connectDB(self) -> None:
        print("ConcreteStateB handles request1.")

    def saveDB(self, newsObject_stack) -> None:
        for newsObject in newsObject_stack:
            insert(newsObject)
        print("ConcreteStateB handles request2.")
        print("ConcreteStateB wants to change the state of the context.")
        self.context.transition_to(ConcreteConnectState())
