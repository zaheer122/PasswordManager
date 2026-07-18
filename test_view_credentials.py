from database.db_manager import DatabaseManager
from auth.auth_manager import AuthenticationManager
from encryption.encryption_manager import EncryptionManager
from vault.vault_manager import VaultManager


MASTER_PASSWORD = "Zaheer@123"

auth = AuthenticationManager()

key = auth.get_encryption_key(
    MASTER_PASSWORD
)

db = DatabaseManager()

encryption = EncryptionManager(key)

vault = VaultManager(
    db,
    encryption,
)

credentials = vault.get_credentials()

for credential in credentials:

    print("-" * 40)

    print("Name:", credential.name)
    print("Website:", credential.website)
    print("Username:", credential.username)
    print("Password:", credential.password)