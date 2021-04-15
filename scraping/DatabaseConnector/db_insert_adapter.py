class DBInsertAdapter: 
    mydb = None
    db_connector = DatabaseSingleton.getInstance()

    def connect():
        db_connector.connect()

        

    def select():
        db_connector.select()

# Type - /news /malaysia_states /malaysia_patients /bing 

    def insert(data_dict, target_table="test", type):
        if type == "news": 
            
            db = DB_News()          
        elif type == "malaysia_states":
            db = DB_Malaysia_States()
        elif type == "malaysia_patients":
            db = DB_Malaysia_Patients()
        elif type == "bing":
            db = DB_Bing()
            
        db.insert(data_dict, target_table="test")
