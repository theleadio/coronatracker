import mysql.connector
import json

# malaysia_patient_case TABLE_SCHEMA
# case, status, status_date, confirmed_date, nationality, age, gender, hospital, description

mydb = None
TEST_TABLE_NAME = "malaysia_states_temp"
PROD_TABLE_NAME = "malaysia_states"

class DBConnector:
    def __init__(self, testTableName, prodTableName):
        self.testTableName = testTableName
        self.prodTableName = prodTableName

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
