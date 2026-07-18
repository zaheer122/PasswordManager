from database.db_manager import DatabaseManager

db = DatabaseManager()

credentials = db.get_credentials()

for credential in credentials:
    print(credential)