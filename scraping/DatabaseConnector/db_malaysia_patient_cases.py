import mysql.connector
import json

class DB_Malaysia_Patients:
    # malaysia_patient_case TABLE_SCHEMA
    # case, status, status_date, confirmed_date, nationality, age, gender, hospital, description

    mydb = None
    TEST_TABLE_NAME = "malaysia_patient_case_temp"
    PROD_TABLE_NAME = "malaysia_patient_case"
    db_connector = DatabaseSingleton.getInstance()

    def connect():
        db_connector.connect()

    def select():
        db_connector.select()

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
