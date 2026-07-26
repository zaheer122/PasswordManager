from datetime import datetime

from database.db_manager import DatabaseManager

from encryption.password_hasher import (
    hash_password,
    verify_password,
    derive_encryption_key,
)

from encryption.salt_manager import SaltManager


class AuthenticationManager:
    """
    Handles user registration and login.
    """

    def __init__(self) -> None:
        self.db = DatabaseManager()

    def user_exists(self) -> bool:
        """
        Check whether a master user already exists.
        """
        return self.db.get_user() is not None

    def register(self, master_password: str) -> bool:
        """
        Register a new master user.

        Returns:
            True if registration succeeds.
            False if a user already exists.
        """

        if self.user_exists():
            return False

        # Persistent salts
        auth_salt = SaltManager.get_auth_salt()
        SaltManager.get_vault_salt()  # Create vault.salt if it doesn't exist

        # Hash the master password using auth.salt
        password_hash = hash_password(
            master_password,
            auth_salt,
        )

        created_at = datetime.now().isoformat()

        self.db.save_user(
            password_hash=password_hash,
            salt=auth_salt,
            created_at=created_at,
        )

        return True

    def login(self, master_password: str) -> bool:
        """
        Authenticate the master user.
        """

        user = self.db.get_user()

        if user is None:
            return False

        return verify_password(
            password=master_password,
            stored_hash=user["password_hash"],
            salt=user["salt"],
        )

    def get_encryption_key(
        self,
        master_password: str,
    ) -> bytes:
        """
        Derive the vault encryption key.
        """

        vault_salt = SaltManager.get_vault_salt()

        return derive_encryption_key(
            master_password,
            vault_salt,
        )