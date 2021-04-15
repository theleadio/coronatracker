import mysql.connector
import json
from abc import ABCMeta, abstractmethod

class ISQL(metaclass=ABCMeta):
    #abstraction interface

    @staticmethod
    @abstractmethod
    def connect():
        pass

    @staticmethod
    @abstractmethod
    def select():
        pass

class ISQLImplementer(metaclass=ABCMeta):
    #sql methods implementer

    @staticmethod
    @abstractmethod
    def connecting():
        pass

    @staticmethod
    @abstractmethod
    def selecting():
        pass

class DBConnection(ISQL):
    #this is a refined abstraction

    def __init__(self, implementer):
        self.implementer = implementer()
    
    def connect(self):
        self.implementer.connecting()

    def select(self):
        self.implementer.selecting()

class DBSources(ISQL):
    #this is a refined abstraction

    def __init__(self, implementer):
        self.implementer = implementer()
    
    def connect(self):
        self.implementer.connecting()

    def select(self):
        self.implementer.selecting()

class DBConnectionImplementer(ISQLImplementer):
    #implementer for dbconnection

    def connecting(self):
        config_path = "./"
        with open(config_path, "r") as handler:
            info = json.load(handler)
            self.mydb = db_sql_connect(info)
            print("Database connected: {}".format(info))

    def selecting(self):
        cursor = self.mydb.cursor()
        mycursor.execute("SELECT * FROM {}".format(TABLE_NAME))
        return cursor.fetchall()

class DBSourcesImplementer(ISQLImplementer):
    #implementer for DBSources

    def connecting(self):
        # populate this from env file
        path_to_json = "./db.json"

        with open(path_to_json, "r") as handler:
            info = json.load(handler)
            print(info)

            mydb = db_sql_connect(info)

        print(mydb)

    def selecting(self, mydb):
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM {}".format(TABLE_NAME))
        myresult = mycursor.fetchall()
        for x in myresult:
            print(x)

def db_sql_connect(info):
    mydb = mysql.connector.connect(
        host=info["host"],
        user=info["user"],
        passwd=info["passwd"],
        database=info["database"],
    )
    return mydb