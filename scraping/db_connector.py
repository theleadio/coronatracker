import mysql.connector
import json
from abc import ABCMeta, abstractmethod

# TABLE_SCHEMA
# ['nid', 'title', 'description', 'author', 'url', 'content', 'urlToImage', 'publishedAt', 'addedOn', 'siteName', 'language', 'countryCode', 'status']

mydb = None
TEST_TABLE_NAME = "newsapi_en"
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

    

    class I_Data_Dict_Builder(metaclass=ABCMeta):
    	"The Builder Interface"

	    @staticmethod
	    @abstractmethod
	    def build_dict_title():
	    	"Data Dictionary Title"

	    @staticmethod
	    @abstractmethod
	    def build_dict_description():
	    	"Data Dictionary Description"

	    @staticmethod
	    @abstractmethod
	    def build_dict_author():
	    	"Data Dictionary Author"

	    @staticmethod
	    @abstractmethod
	    def build_dict_url():
	    	"Data Dictionary url"

	    @staticmethod
	    @abstractmethod
	    def build_dict_content():
	    	"Data Dictionary Content"

	    @staticmethod
	    @abstractmethod
	    def build_dict_urlToImage():
	    	"Data Dictionary url to Image Conversion"

	    @staticmethod
	    @abstractmethod
	    def build_dict_publishedAt():
	    	"Data Dictionary publication Date"

	    @staticmethod
	    @abstractmethod
	    def build_dict_addedOn():
	    	"Data Dictionary Add Ons"


	    @staticmethod
	    @abstractmethod
	    def build_dict_siteName():
	    	"Data Dictionary Website Name"

	    @staticmethod
	    @abstractmethod
	    def build_dict_language():
	    	"Data Dictionary language"

	    @staticmethod
	    @abstractmethod
	    def build_dict_countryCode():
	    	"Data Dictionary Country Code"

	    @staticmethod
	    @abstractmethod
	    def get_dict():
	    	"Return the final dictionary"

	class Data_Dict_Builder(I_Data_Dict_Builder):
		"The Concrete Data Dictionary Builder"

		def __init__(self):
			self.dictionary_prod = Dictionary_Product()

		def build_dict_title(self):
	    	self.dictionary_prod.components.append(data_dict["title"])
	    	return self

	    def build_dict_description(self):
	    	self.dictionary_prod.components.append(data_dict["description"])
	    	return self

	    def build_dict_author(self):
	    	self.dictionary_prod.components.append(data_dict["author"])
	    	return self

	    def build_dict_url(self):
	    	self.dictionary_prod.components.append(data_dict["url"])
	    	return self

	    def build_dict_content(self):
			self.dictionary_prod.components.append(data_dict["content"])
			return self

	    def build_dict_urlToImage(self):
	    	self.dictionary_prod.components.append(data_dict["urlToImage"])
	    	return self

	    def build_dict_publishedAt(self):
	    	self.dictionary_prod.components.append(data_dict["publishedAt"])
	    	return self

	    def build_dict_addedOn(self):
	    	self.dictionary_prod.components.append(data_dict["addedOn"])
	    	return self

	    def build_dict_siteName(self):
	    	self.dictionary_prod.components.append(data_dict["siteName"])
	    	return self

	    def build_dict_language(self):
	    	self.dictionary_prod.components.append(data_dict["language"])
	    	return self

	    def build_dict_countryCode(self):
	    	self.dictionary_prod.components.append(data_dict["countryCode"])
	    	return self

	    def get_dict(self):
	    	return self.dictionary_prod

	class Dictionary_Product():
		"The Dictionary Product"

		def __init__(self):
			self.components = []

	class Dictionary_Director():
		"The Dictionary Director"

		@staticmethod
		def construct():
			"Constructs and returns the final product"
			return Data_Dict_Builder()\
				.build_dict_title()\
			    .build_dict_description()\
			    .build_dict_author()\
			    .build_dict_url()\
				.build_dict_content()\
			    .build_dict_urlToImage()\
			    .build_dict_publishedAt()\
			    .build_dict_addedOn()\
			    .build_dict_siteName()\
			    .build_dict_language()\
			    .build_dict_countryCode()\
			    .get_dict()



    print("SQL query: ", sql)
    try:
        mycursor.execute(sql, Dictionary_Director.construct())
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")
    except Exception as ex:
        print(ex)
        print("Record not inserted")
