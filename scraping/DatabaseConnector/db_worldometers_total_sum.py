import mysql.connector
import json

# worldometers_total_sum TABLE_SCHEMA
# total_cases, total_deaths, total_recovered, new_cases, new_deaths, active_cases, serious_critical_cases, total_cases_per_million_pop, last_updated

mydb = None
TEST_TABLE_NAME = "worldometers_total_sum"
PROD_TABLE_NAME = "worldometers_total_sum"


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
    sql = "INSERT INTO {} (total_cases, total_deaths, total_recovered, new_cases, new_deaths, active_cases, serious_critical_cases, total_cases_per_million_pop, last_updated) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE total_cases = %s, total_deaths = %s, total_recovered = %s, new_cases = %s, new_deaths = %s, active_cases = %s, serious_critical_cases = %s, total_cases_per_million_pop = %s".format(
        table_name
    )
    val = (
        data_dict["total_cases"],
        data_dict["total_deaths"],
        data_dict["total_recovered"],
        data_dict["new_cases"],
        data_dict["new_deaths"],
        data_dict["active_cases"],
        data_dict["serious_critical_cases"],
        data_dict["total_cases_per_million_pop"],
        data_dict["last_updated"],
        data_dict["total_cases"],
        data_dict["total_deaths"],
        data_dict["total_recovered"],
        data_dict["new_cases"],
        data_dict["new_deaths"],
        data_dict["active_cases"],
        data_dict["serious_critical_cases"],
        data_dict["total_cases_per_million_pop"]
    )
    print("SQL query: ", sql, val)
    try:
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")
    except Exception as ex:
        print(ex)
        print("Record not inserted")
