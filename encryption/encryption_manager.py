from cryptography.fernet import Fernet


class EncryptionManager:
    """
    Encrypts and decrypts credential passwords.
    """

    def __init__(self, key: bytes):
        self.cipher = Fernet(key)

    def encrypt(self, text: str) -> str:
        return self.cipher.encrypt(text.encode()).decode()

    def decrypt(self, encrypted_text: str) -> str:
        return self.cipher.decrypt(
            encrypted_text.encode()
        ).decode()