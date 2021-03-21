import DBConnector

class DBMalaysiaPatientCases(DBConnector):
    def __init__(self, testTableName, prodTableName):
        super().__init__(testTableName, prodTableName)

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
