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

print("Before Delete")
print("----------------")

for credential in vault.get_credentials():
    print(credential.id, credential.name)

vault.delete_credential(1)

print("\nAfter Delete")
print("----------------")

credentials = vault.get_credentials()

if not credentials:
    print("No credentials found.")
else:
    for credential in credentials:
        print(credential.id, credential.name)