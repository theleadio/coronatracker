import mysql.connector
import json

# BING_COVID TABLE_SCHEMA
# ['nid', 'state', 'country', 'last_update', 'lat', 'lng', 'confirmed', 'deaths', 'recovered', 'posted_date']





##### Grouping multiple methods and aggregating into one class called BingDB


TEST_TABLE_NAME = "bing_covid_temp"
PROD_TABLE_NAME = "bing_covid"
class BingDB:  
    def __init__(self, mycursor):
        self.mydb = None
        self.mycursor = mydb.cursor

    def connect(self):
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

    def select(self):
        self.mycursor.execute("SELECT * FROM {}".format(TABLE_NAME))
        myresult = self.mycursor.fetchall()
        for x in myresult:
            print(x)

    def insert(self, data_dict, target_table="test"):
        table_name = PROD_TABLE_NAME if target_table == "prod" else TEST_TABLE_NAME
        mycursor = mydb.cursor()
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
            mydb.commit()
            print(mycursor.rowcount, "record inserted.")
        except Exception as ex:
            print(ex)
            print("Record not inserted")


#####



