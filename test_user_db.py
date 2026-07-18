from datetime import datetime

from database.db_manager import DatabaseManager

db = DatabaseManager()

# Only create a user if one doesn't already exist
if db.get_user() is None:
    db.save_user(
        password_hash="dummy_hash",
        salt="dummy_salt",
        created_at=datetime.now().isoformat(),
    )
    print("User created!")
else:
    print("User already exists.")

print(db.get_user())