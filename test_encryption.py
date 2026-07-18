from encryption.password_hasher import (
    generate_salt,
    derive_encryption_key,
)

from encryption.encryption_manager import EncryptionManager

master_password = "Zaheer@123"

salt = generate_salt()

key = derive_encryption_key(
    master_password,
    salt,
)

manager = EncryptionManager(key)

password = "GithubPassword@123"

encrypted = manager.encrypt(password)

print("Encrypted:", encrypted)

print("Decrypted:", manager.decrypt(encrypted))