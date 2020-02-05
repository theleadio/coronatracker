import mysql.connector
import json

mydb = None

def connect():
    global mydb

    #populate this from env file
    path_to_json = "./db.json"

    with open(path_to_json, "r") as handler:
        info = json.load(handler)
        print(info)

    
        mydb = mysql.connector.connect(
          host=info["host"],
          user=info["user"],
          passwd=info["passwd"],
          database=info["database"]
        )

    print(mydb)

def select():
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM newsapi_oceania")
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)

def insert(data_dict):

    mycursor = mydb.cursor()
    sql = "INSERT INTO newsapi_oceania (`title`, `description`, `author`, `url`, `summary`, `content`, `urlToImage`, `publishedAt`, `source`, `accessDateTime`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (data_dict["title"], data_dict["description"], data_dict["author"], data_dict["url"], data_dict["summary"],
           data_dict["content"], data_dict["urlToImage"], data_dict["publishedAt"], data_dict["source"], data_dict["accessDateTime"])
    print(sql)
    try:
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")
    except Exception as ex:
        print(ex)
        print("Record not inserted")


def check_news(title, source):
    mycursor = mydb.cursor()
    mycursor.execute(f"SELECT * FROM newsapi_oceania WHERE title = \"{title}\" and source = \"{source}\"")
    myresult = mycursor.fetchall()
    return myresult
