from datetime import datetime

from database.db_manager import DatabaseManager

db = DatabaseManager()

# Add a sample credential
db.add_credential(
    credential_name="GitHub",
    username="zaheer@example.com",
    password="encrypted_password_here",
    created_at=datetime.now().isoformat(),
    updated_at=datetime.now().isoformat(),
)

print("All Credentials:")
for credential in db.get_credentials():
    print(dict(credential))

print("\nSearch Results:")
for credential in db.search_credentials("Git"):
    print(dict(credential))