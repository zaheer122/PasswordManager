from pathlib import Path
from datetime import datetime
from pathlib import Path
from encryption.salt_manager import SaltManager

import json

from database.db_manager import DatabaseManager


class BackupManager:
    """
    Handles vault backup and restore.
    """

    def __init__(self, database: DatabaseManager):
        self.database = database

        self.backup_directory = Path("backups")
        self.backup_directory.mkdir(exist_ok=True)

    def export_backup(self) -> Path:
        """
        Export all credentials to a JSON file.
        """

        credentials = self.database.get_credentials()

        data = {
        "vault_salt": SaltManager.get_vault_salt(),
        "credentials": [],
        }

        for credential in credentials:
            data["credentials"].append(
                {
                    "name": credential.name,
                    "website": credential.website,
                    "username": credential.username,
                    "email": credential.email,
                    "encrypted_password": credential.encrypted_password,
                    "notes": credential.notes,
                    "category": credential.category,
                    "favorite": credential.favorite,
                    "created_at": credential.created_at,
                    "updated_at": credential.updated_at,
                }
            )

        filename = (
            f"backup_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
        )

        backup_path = self.backup_directory / filename

        with open(backup_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        return backup_path

    def import_backup(self, backup_file: str | Path) -> None:
        """
        Import credentials from a backup file.
        """

        with open(backup_file, "r", encoding="utf-8") as file:
            backup = json.load(file)
 
        Path("data").mkdir(exist_ok=True)

        Path("data/vault.salt").write_text(
            backup["vault_salt"]
        )
        # Clear current vault
        self.database.delete_all_credentials()

        for credential in backup["credentials"]:

            self.database.add_credential(
                name=credential["name"],
                website=credential["website"],
                username=credential["username"],
                email=credential["email"],
                encrypted_password=credential["encrypted_password"],
                notes=credential["notes"],
                category=credential["category"],
                favorite=int(credential["favorite"]),
                created_at=credential["created_at"],
                updated_at=credential["updated_at"],
            )