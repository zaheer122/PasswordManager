from datetime import datetime
from encryption.password_hasher import derive_encryption_key

from database.db_manager import DatabaseManager
from encryption.password_hasher import (
    generate_salt,
    hash_password,
    verify_password,
)


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

    # Check if a user already exists
        if self.user_exists():
            return False

    # Generate a random salt
        salt = generate_salt()

    # Hash the password
        password_hash = hash_password(master_password, salt)

    # Current timestamp
        created_at = datetime.now().isoformat()

    # Save user
        self.db.save_user(
            password_hash=password_hash,
            salt=salt,
            created_at=created_at,
        )

        return True
    
    def login(self, master_password: str) -> bool:
        """
        Authenticate the master user.

        Args:
            master_password: Password entered by the user.

        Returns:
            True if authentication succeeds, False otherwise.
        """

    # Retrieve the stored user
        user = self.db.get_user()

    # No user registered yet
        if user is None:
            return False

    # Verify the entered password
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
        Return the encryption key for the logged-in user.
        """

        user = self.db.get_user()

        if user is None:
            raise ValueError("No registered user found.")

        return derive_encryption_key(
            master_password,
            user["salt"],
        )