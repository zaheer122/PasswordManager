from database.db_manager import DatabaseManager

db = DatabaseManager()

credentials = db.get_credentials()

for c in credentials:
    print(c.name)