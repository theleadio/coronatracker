import mysql.connector
import json

# BING_COVID TABLE_SCHEMA
# ['nid', 'state', 'country', 'last_update', 'lat', 'lng', 'confirmed', 'deaths', 'recovered', 'posted_date']



mydb = None
TEST_TABLE_NAME = "bing_covid_temp"
PROD_TABLE_NAME = "bing_covid"

#Making a client function that will call the adaptee function when given the adaptor object
def clientcode(target: "Target"):
    target.adapterConnect()

class DatabaseBingCovid:
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

#Creating a target class that will have the signature that the client code will use
    class Target:
        #we define the interface that will be used in the client code, we can make it return none because we won't actually be needing
        #the return value of this class as we will be using an adapter to call an adaptee instead
        def adapterConnect(self):
            return None

    class Adapter(Target, DatabaseBingCovid):
        #The adapter will allow us to make the Target's interface work with the connect interface, DatabaseBingCovid is our adaptee
        def adapterConnect(self):
            return self.connect()


def select():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM {}".format(TABLE_NAME))
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)


def insert(data_dict, target_table="test"):
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
