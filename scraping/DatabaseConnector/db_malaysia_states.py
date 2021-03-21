import DBConnector

class DBMalaysiaStates(DBConnector):
    def __init__(self, testTableName, prodTableName):
        super().__init__(testTableName, prodTableName)

    def insert(data_dict, target_table="test"):
        table_name = PROD_TABLE_NAME if target_table == "prod" else TEST_TABLE_NAME
        mycursor = mydb.cursor()
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
            mydb.commit()
            print(mycursor.rowcount, "record inserted.")
        except Exception as ex:
            print(ex)
            print("Record not inserted")
