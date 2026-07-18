from database.db_manager import DatabaseManager
from auth.auth_manager import AuthenticationManager
from encryption.encryption_manager import EncryptionManager
from vault.vault_manager import VaultManager

master_password = "Zaheer@123"

auth = AuthenticationManager()

key = auth.get_encryption_key("Zaheer@123")

db = DatabaseManager()

encryption = EncryptionManager(key)

vault = VaultManager(db, encryption)

vault.add_credential(
    name="GitHub",
    website="https://github.com",
    username="zaheer",
    email="zaheer@example.com",
    password="MyGitHubPassword@123",
    notes="Personal account",
    category="Development",
    favorite=True,
)

print("Credential added successfully!")