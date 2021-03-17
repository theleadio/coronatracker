#Aggregate root for BingCovid.py and db_bingcovid.py

class covid_Data_Table:

    mydb = None
    TEST_TABLE_NAME = "bing_covid_temp"
    PROD_TABLE_NAME = "bing_covid"

    def __init__(
        self,
        state=None,
        country=None,
        last_update=None,
        lat=None,
        lng=None,
        confirmed=None,
        deaths=None,
        recovered=None,
        posted_date=datetime.utcnow(),
    ):
        self.state = state
        self.country = country
        self.last_update = parser.parse(last_update) if last_update else last_update
        self.lat = lat
        self.lng = lng
        self.confirmed = confirmed
        self.deaths = deaths
        self.recovered = recovered
        self.posted_date = posted_date

    def get_insert_data(data_dict, target_table="test"):
        return db_bingcovid.insert(data_dict, target_table="test")

    def get_select_function():
        return db_bingcovid.select()

    def is_connected():
        return db_bingcovid.connect()
