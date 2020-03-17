import mysql.connector
import json

# NEWS TABLE_SCHEMA
# ['nid', 'title', 'description', 'author', 'url', 'content', 'urlToImage', 'publishedAt', 'addedOn', 'siteName', 'language', 'countryCode', 'status']

mydb = None
TEST_TABLE_NAME = "newsapi_n_temp"
PROD_TABLE_NAME = "newsapi_n"


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
    sql = "INSERT INTO {} (title, description, author, url, content, urlToImage, publishedAt, addedOn, siteName, language, countryCode, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE title = %s, description = %s, author = %s, content = %s, urlToImage = %s, publishedAt = %s, addedOn = %s, siteName = %s, language = %s, countryCode = %s".format(
        table_name
    )
    val = (
        data_dict["title"],
        data_dict["description"],
        data_dict["author"],
        data_dict["url"],
        data_dict["content"],
        data_dict["urlToImage"],
        data_dict["publishedAt"],
        data_dict["addedOn"],
        data_dict["siteName"],
        data_dict["language"],
        data_dict["countryCode"],
        1,  # Status
        data_dict["title"],
        data_dict["description"],
        data_dict["author"],
        data_dict["content"],
        data_dict["urlToImage"],
        data_dict["publishedAt"],
        data_dict["addedOn"],
        data_dict["siteName"],
        data_dict["language"],
        data_dict["countryCode"],
    )
    print("SQL query: ", sql, val)
    try:
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")
    except Exception as ex:
        print(ex)
        print("Record not inserted")
