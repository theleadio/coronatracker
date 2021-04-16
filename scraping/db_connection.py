import mysql.connector
import json

class Factory_Demo:

    def __init__(self,mydb=None):
        self.mydb=None

    def connect():

        global self.mydb

     # populate this from env file
       path_to_json = "./db.json"

     with open(path_to_json, "r") as handler:
        info = json.load(handler)
        print(info)

     self.mydb = mysql.connector.connect(
        host=info["host"],
        user=info["user"],
        passwd=info["passwd"],
        database=info["database"],
        )

     print(self.mydb)


    def select():

     mycursor = self.mydb.cursor()
     mycursor.execute("SELECT * FROM {}".format(TABLE_NAME))
     myresult = mycursor.fetchall()
     for x in myresult:
        print(x)

    def Factory(db="Malaysia_patient_case"):
     """Factory Method"""
     databases = {
        "Malaysia_patient_case":Malaysia_patient_case,
        "Malaysia_states_temp":Malaysia_states_temp,
        "Bing_covid":Bing_covid
     }
      return databases[db]



class Bing_covid():

    def __init__(self,mydb,TEST_TABLE_NAME,PROD_TABLE_NAME):
        self.mydb = None
        self.TEST_TABLE_NAME="bing_covid_temp"
        self.PROD_TABLE_NAME="bing_covid"

    def insert(data_dict,target_table="test"):

        table_name = self.PROD_TABLE_NAME if target_table == "prod" else self.TEST_TABLE_NAME
        mycursor = self.mydb.cursor()
        sql = "INSERT INTO {} (state, country, last_update, lat, lng, confirmed, deaths, recovered, posted_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE state = %s, country = %s, confirmed = %s, deaths = %s, recovered = %s".format(
        table_name
        )
        val = (
        data_dict["state"],
        data_dict["country"],
        data_dict["last_update"],
        data_dict["lat"],
        data_dict["lng"],
        data_dict["confirmed"],
        data_dict["deaths"],
        data_dict["recovered"],
        data_dict["posted_date"],
        data_dict["state"],
        data_dict["country"],
        data_dict["confirmed"],
        data_dict["deaths"],
        data_dict["recovered"],
        )
        print("SQL query: ", sql, val)
        try:
        mycursor.execute(sql, val)
        self.mydb.commit()
        print(mycursor.rowcount, "record inserted.")
        except Exception as ex:
        print(ex)
        print("Record not inserted")

class Malaysia_states_temp():

        def __init__(self,mydb,TEST_TABLE_NAME,PROD_TABLE_NAME):
            self.mydb = None
            self.TEST_TABLE_NAME="malaysia_states_temp"
            self.PROD_TABLE_NAME="malaysia_states"

        def insert(data_dict,target_table="test"):
            table_name = self.PROD_TABLE_NAME if target_table == "prod" else self.TEST_TABLE_NAME
            mycursor = self.mydb.cursor()
            sql = "INSERT INTO {} (state, increment_count, total_count, hospital_count, recovered_count, death_count, last_updated) VALUES (%s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE state = %s, increment_count = %s, total_count = %s, hospital_count = %s, recovered_count = %s, death_count = %s".format(
         table_name
          )
          val = (
         data_dict["state"],
         data_dict["increment_count"],
         data_dict["total_count"],
         data_dict["hospital_count"],
         data_dict["recovered_count"],
         data_dict["death_count"],
         data_dict["last_updated"],
         data_dict["state"],
         data_dict["increment_count"],
         data_dict["total_count"],
         data_dict["hospital_count"],
         data_dict["recovered_count"],
         data_dict["death_count"],
          )
          print("SQL query: ", sql, val)
         try:
         mycursor.execute(sql, val)
         self.mydb.commit()
         print(mycursor.rowcount, "record inserted.")
         except Exception as ex:
         print(ex)
         print("Record not inserted")
      
class Malaysia_patient_case():

        def __init__(self,mydb,TEST_TABLE_NAME,PROD_TABLE_NAME):
            self.mydb = None
            self.TEST_TABLE_NAME="malaysia_states_temp"
            self.PROD_TABLE_NAME="malaysia_states"

        def insert(data_dict,target_table="test"):
            table_name = self.PROD_TABLE_NAME if target_table == "prod" else self.TEST_TABLE_NAME
            mycursor = self.mydb.cursor()
            sql = "INSERT INTO {} (caseId, status, statusDate, confirmedDate, nationality, age, gender, hospital, description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE caseId = %s, status = %s, statusDate = %s, confirmedDate = %s, nationality = %s, age = %s, gender = %s, hospital = %s, description = %s".format(
         table_name
         )
         val = (
         data_dict["case"],
         data_dict["status"],
         data_dict["status_date"],
         data_dict["confirmed_date"],
         data_dict["nationality"],
         data_dict["age"],
         data_dict["gender"],
         data_dict["hospital"],
         data_dict["description"],
         data_dict["case"],
         data_dict["status"],
         data_dict["status_date"],
         data_dict["confirmed_date"],
         data_dict["nationality"],
         data_dict["age"],
         data_dict["gender"],
         data_dict["hospital"],
         data_dict["description"],
         )
         print("SQL query: ", sql, val)
         try:
         mycursor.execute(sql, val)
         self.mydb.commit()
         print(mycursor.rowcount, "record inserted.")
         except Exception as ex:
         print(ex)
         print("Record not inserted")
      

