from scraping.DatabaseConnector.mysql_connector import MySQL_Connector


mydb = None
TEST_TABLE_NAME = "malaysia_patient_case_temp"
PROD_TABLE_NAME = "malaysia_patient_case"

class Malaysia_db_connector(MySQL_Connector):

    ''' malaysia_patient_case TABLE_SCHEMA
        case, status, status_date, confirmed_date, nationality, age, gender, hospital, description
    '''
    def __init__(self, config_path):
        self.mydb = MySQL_Connector(config_path)

    def connect(self):
        self.mydb.connect()

    def select(self, query):
        self.mydb.select(query)

def insert(self, data_dict, target_table="test"):

    table_name = PROD_TABLE_NAME if target_table == "prod" else TEST_TABLE_NAME
    _query = "INSERT INTO {} (caseId, status, statusDate, confirmedDate, nationality, age, gender, hospital, description) VALUES \
            (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE caseId = %s, status = %s, statusDate = %s, \
            confirmedDate = %s, nationality = %s, age = %s, gender = %s, hospital = %s, description = %s".format(table_name)
    _val = (
        data_dict["case"],
        data_dict["status"],
        data_dict["status_date"],
        data_dict["confirmed_date"],
        data_dict["nationality"],
        data_dict["age"],
        data_dict["gender"],
        data_dict["hospital"],
        data_dict["description"],
        data_dict["case"],
        data_dict["status"],
        data_dict["status_date"],
        data_dict["confirmed_date"],
        data_dict["nationality"],
        data_dict["age"],
        data_dict["gender"],
        data_dict["hospital"],
        data_dict["description"],
    )
    self.mydb.insert(target_table, _query, _val)