from auth.auth_manager import AuthenticationManager
from database.db_manager import DatabaseManager
from encryption.encryption_manager import EncryptionManager
from vault.vault_manager import VaultManager

MASTER_PASSWORD = "Zaheer@123"

auth = AuthenticationManager()
key = auth.get_encryption_key(MASTER_PASSWORD)

db = DatabaseManager()
encryption = EncryptionManager(key)

vault = VaultManager(db, encryption)

vault.update_credential(
    credential_id=1,
    name="GitHub Updated",
    website="https://github.com",
    username="zaheer",
    email="zaheer@example.com",
    password="NewPassword@456",
    notes="Updated account",
    category="Development",
    favorite=True,
)

credential = vault.get_credential_by_id(1)

print(credential.name)
print(credential.password)