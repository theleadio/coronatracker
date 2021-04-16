from db_connector import DatabaseConnectorWrapper

print(DatabaseConnectorWrapper.getInstance().getAllDBConnections())
db_connector = DatabaseConnectorWrapper.getInstance().getDb(config_path="./db.json")
print(DatabaseConnectorWrapper.getInstance().getAllDBConnections())
print(db_connector.config_path)

db_connector = DatabaseConnectorWrapper.getInstance().getDb(config_path="./db.prodv2.json")
print(DatabaseConnectorWrapper.getInstance().getAllDBConnections())
print(db_connector.config_path)