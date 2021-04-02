from scraping.DatabaseConnector.mysql_connector import MySQL_Connector

TEST_TABLE_NAME = "bing_covid_temp"
PROD_TABLE_NAME = "bing_covid"


class Bing_db_connector(MySQL_Connector):
    ''' BING_COVID TABLE_SCHEMA
        ['nid', 'state', 'country', 'last_update', 'lat', 'lng', 'confirmed', 'deaths', 'recovered', 'posted_date']
    '''

    def __init__(self, config_path):
        self.mydb = MySQL_Connector(config_path)

    def connect(self):
        self.mydb.connect()

    def select(self, query):
        self.mydb.select(query)

    def insert(self, data_dict, target_table="test"):

        table_name = PROD_TABLE_NAME if target_table == "prod" else TEST_TABLE_NAME
        _query = "INSERT INTO {} (state, country, last_update, lat, lng, confirmed, deaths, recovered, posted_date) VALUES \
                (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE state = %s, country = %s, confirmed = %s, deaths = %s, recovered = %s".format(table_name)
        _val = (
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
        self.mydb.insert(target_table, _query, _val)
