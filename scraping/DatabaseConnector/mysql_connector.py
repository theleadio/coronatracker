#import scraping.DatabaseConnector.dbFactory.DB_Connector as DB_Connector
import json
import inspect
from mysql.connector import pooling
from mysql.connector import Error

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        else:
            cls._instances[cls].__init__(*args, **kwargs)
        return cls._instances[cls]


class MySQL_Connector(metaclass=Singleton):

    def __init__(self, config_path="./"):
        self.config_path = config_path
        with open(self.config_path, "r") as handler:
            info = json.load(handler)
            self.mydb = pooling.MySQLConnectionPool(pool_name='covid_tracker',
                                                    pool_size=32,
                                                    pool_reset_session=True,
                                                    host=info["host"],
                                                    user=info["user"],
                                                    password=info["passwd"],
                                                    database=info["database"])
        try:
            self.connection = mydb.get_connection()
            print("Database connected: {}".format(self.connection.get_server_info()))
        except Error as e:
            print("Database connection failed", e)

    def connect(self):
        return self.connection


    def select(self, query):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            return cursor.fetchall()
        except Error as e:
            print('Select query failed', e)


    def retrieve_name(self, var):
            """
            Gets the name of var. Does it from the out most frame inner-wards.
            :param var: variable to get name from.
            :return: string
            """
            for fi in reversed(inspect.stack()):
                names = [var_name for var_name, var_val in fi.frame.f_locals.items() if var_val is var]
                if len(names) > 0:
                    return names[0]


    def insert(self, target_table, query, data_dict):
        cursor = self.connection.cursor()
        try:
            result = cursor.execute("SHOW TABLES LIKE '{}'".format(target_table))
            result.fetchone()
        except Error as e:
            print('{} not found'.format(target_table))

        try:
            cursor.execute(query.format(retrieve_name(data_dict), table_name=target_table))
            self.mydb.commit()
            print(cursor.rowcount, " record inserted.")
        except Exception as ex:
            print(ex)
            print("Record not inserted")

    def execute(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
  