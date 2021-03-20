import mysql.connector
import json

class MalaysiaStateCases:
    def __init__(
        self,
        state,
        confirmed,
        deaths,
        recovered,
    ):
        self.state = state # the field that identifies individual MalaysiaStateCases objects
        self.confirmed = confirmed
        self.deaths = deaths
        self.recovered = recovered

    # Copy and pasted the code from db_malaysia_patient_cases so that deep references are now avoided.

    # malaysia_patient_case TABLE_SCHEMA
    # case, status, status_date, confirmed_date, nationality, age, gender, hospital, description

    mydb = None
    TEST_TABLE_NAME = "malaysia_patient_case_temp"
    PROD_TABLE_NAME = "malaysia_patient_case"

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

    def insert(data_dict, target_table="test"):
        table_name = PROD_TABLE_NAME if target_table == "prod" else TEST_TABLE_NAME
        mycursor = mydb.cursor()
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
            mydb.commit()
            print(mycursor.rowcount, "record inserted.")
        except Exception as ex:
            print(ex)
            print("Record not inserted")
