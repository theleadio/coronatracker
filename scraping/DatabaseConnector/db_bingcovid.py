import mysql.connector
import json
from db_builder import Director

# BING_COVID TABLE_SCHEMA
# ['nid', 'state', 'country', 'last_update', 'lat', 'lng', 'confirmed', 'deaths', 'recovered', 'posted_date']

mydb = None
TEST_TABLE_NAME = "bing_covid_temp"
PROD_TABLE_NAME = "bing_covid"


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


def insert(target_table="test"):
    table_name = PROD_TABLE_NAME if target_table == "prod" else TEST_TABLE_NAME
    mycursor = mydb.cursor()
    sql = "INSERT INTO {} (state, country, last_update, lat, lng, confirmed, deaths, recovered, posted_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE state = %s, country = %s, confirmed = %s, deaths = %s, recovered = %s".format(
        table_name
    )
    
    #passing the value as a dict instead of a tuple
    #will output the same value once put into the method execute() below
    val = Director.construct_bc()

    print("SQL query: ", sql, val)
    try:
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")
    except Exception as ex:
        print(ex)
        print("Record not inserted")
