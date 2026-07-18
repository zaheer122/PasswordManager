from datetime import datetime

from database.db_manager import DatabaseManager
from encryption.encryption_manager import EncryptionManager


class VaultManager:
    """
    Handles all vault operations.
    """

    def __init__(
        self,
        database: DatabaseManager,
        encryption: EncryptionManager,
    ):
        self.database = database
        self.encryption = encryption

    def add_credential(
        self,
        name: str,
        website: str | None,
        username: str | None,
        email: str | None,
        password: str,
        notes: str | None,
        category: str | None,
        favorite: bool = False,
    ) -> None:

        encrypted_password = self.encryption.encrypt(password)

        now = datetime.now().isoformat()

        self.database.add_credential(
            name=name,
            website=website,
            username=username,
            email=email,
            encrypted_password=encrypted_password,
            notes=notes,
            category=category,
            favorite=int(favorite),
            created_at=now,
            updated_at=now,
        )
    
    def get_credentials(self):

        credentials = self.database.get_credentials()

        for credential in credentials:
            credential.password = self.encryption.decrypt(
                credential.encrypted_password
            )

        return credentials
    
    def get_credential_by_id(
        self,
        credential_id: int,
    ):

        credential = self.database.get_credential_by_id(
            credential_id
        )

        if credential is None:
            return None

        credential.password = self.encryption.decrypt(
            credential.encrypted_password
        )

        return credential
    
    def update_credential(
        self,
        credential_id: int,
        name: str,
        website: str | None,
        username: str |None,
        email: str | None,
        password: str,
        notes: str | None,
        category: str | None,
        favorite: bool,
    ):
        """
        Update an existing credential.
        """

        encrypted_password = self.encryption.encrypt(password)

        updated_at = datetime.now().isoformat()

        self.database.update_credential(
            credential_id=credential_id,
            name=name,
            website=website,
            username=username,
            email=email,
            encrypted_password=encrypted_password,
            notes=notes,
            category=category,
            favorite=int(favorite),
            updated_at=updated_at,
        )

    def delete_credential(
        self,
        credential_id: int,
    ) -> None:
        """
        Delete a credential.
        """

        self.database.delete_credential(
            credential_id
        )