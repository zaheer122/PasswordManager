from auth.auth_manager import AuthenticationManager
from database.db_manager import DatabaseManager
from encryption.encryption_manager import EncryptionManager
from vault.vault_manager import VaultManager

MASTER_PASSWORD = "Zaheer@123"

auth = AuthenticationManager()
key = auth.get_encryption_key(MASTER_PASSWORD)

db = DatabaseManager()

encryption = EncryptionManager(key)

vault = VaultManager(
    db,
    encryption,
)

results = vault.search_credentials("github")

print(f"\nFound {len(results)} credential(s)\n")

for credential in results:

    print("-" * 40)
    print("Name:", credential.name)
    print("Website:", credential.website)
    print("Username:", credential.username)
    print("Email:", credential.email)
    print("Password:", credential.password)
    print("Category:", credential.category)