import mysql.connector
import json


class DatabaseSingleton:
   __instance = None

   @staticmethod
   def getInstance():
      """ Static access method. """
      if Singleton.__instance == None:
         Singleton()
      return Singleton.__instance

   def __init__(self):
      """ Virtually private constructor. """
      if Singleton.__instance != None:
         raise Exception("This class is a singleton!")
      else:
         Singleton.__instance = self

    def connect():
        global mydb
        # populate this from env file
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


    def select():
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM {}".format(TABLE_NAME))
        myresult = mycursor.fetchall()
        for x in myresult:
            print(x)
