from pathlib import Path
import sqlite3

from database.schema import (
    USERS_TABLE,
    CREDENTIALS_TABLE,
    SETTINGS_TABLE,
)

from models.credential import Credential


class DatabaseManager:
    """
    Handles all SQLite database operations.
    """

    def __init__(self, db_name: str = "vault.db") -> None:

        self.data_directory = Path("data")
        self.data_directory.mkdir(exist_ok=True)

        self.database_path = self.data_directory / db_name

        self.connection = sqlite3.connect(self.database_path)
        self.connection.row_factory = sqlite3.Row

        self.cursor = self.connection.cursor()

        self.create_tables()

        print(f"Connected to database: {self.database_path}")

    # ----------------------------------------------------
    # Database Setup
    # ----------------------------------------------------

    def create_tables(self) -> None:

        self.cursor.execute(USERS_TABLE)
        self.cursor.execute(CREDENTIALS_TABLE)
        self.cursor.execute(SETTINGS_TABLE)

        self.connection.commit()

        print("Database tables created successfully.")

    # ----------------------------------------------------
    # Helper
    # ----------------------------------------------------

    def _row_to_credential(self, row: sqlite3.Row) -> Credential:
        """
        Convert a SQLite row into a Credential object.
        """

        return Credential(
            id=row["id"],
            name=row["name"],
            website=row["website"],
            username=row["username"],
            email=row["email"],
            encrypted_password=row["encrypted_password"],
            notes=row["notes"],
            category=row["category"],
            favorite=bool(row["favorite"]),
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    # ----------------------------------------------------
    # User Methods
    # ----------------------------------------------------

    def save_user(
        self,
        password_hash: str,
        salt: str,
        created_at: str,
    ) -> None:

        query = """
        INSERT INTO users(
            password_hash,
            salt,
            created_at
        )
        VALUES (?, ?, ?)
        """

        self.cursor.execute(
            query,
            (
                password_hash,
                salt,
                created_at,
            ),
        )

        self.connection.commit()

    def get_user(self):

        query = """
        SELECT *
        FROM users
        LIMIT 1
        """

        self.cursor.execute(query)

        return self.cursor.fetchone()

    def update_user(
        self,
        password_hash: str,
        salt: str,
    ) -> None:

        query = """
        UPDATE users
        SET
            password_hash = ?,
            salt = ?
        WHERE id = 1
        """

        self.cursor.execute(
            query,
            (
                password_hash,
                salt,
            ),
        )

        self.connection.commit()

    # ----------------------------------------------------
    # Credential Methods
    # ----------------------------------------------------

    def add_credential(
        self,
        name: str,
        website: str | None,
        username: str | None,
        email: str | None,
        encrypted_password: str,
        notes: str | None,
        category: str | None,
        favorite: int,
        created_at: str,
        updated_at: str,
    ) -> None:

        query = """
        INSERT INTO credentials(
            name,
            website,
            username,
            email,
            encrypted_password,
            notes,
            category,
            favorite,
            created_at,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        self.cursor.execute(
            query,
            (
                name,
                website,
                username,
                email,
                encrypted_password,
                notes,
                category,
                favorite,
                created_at,
                updated_at,
            ),
        )

        self.connection.commit()

    def get_credentials(self) -> list[Credential]:

        query = """
        SELECT *
        FROM credentials
        ORDER BY name
        """

        self.cursor.execute(query)

        rows = self.cursor.fetchall()

        return [
            self._row_to_credential(row)
            for row in rows
        ]

    def get_credential_by_id(
        self,
        credential_id: int,
    ) -> Credential | None:

        query = """
        SELECT *
        FROM credentials
        WHERE id = ?
        """

        self.cursor.execute(
            query,
            (credential_id,),
        )

        row = self.cursor.fetchone()

        if row is None:
            return None

        return self._row_to_credential(row)

    def update_credential(
        self,
        credential_id: int,
        name: str,
        website: str | None,
        username: str | None,
        email: str | None,
        encrypted_password: str,
        notes: str | None,
        category: str | None,
        favorite: int,
        updated_at: str,
    ) -> None:

        query = """
        UPDATE credentials
        SET
            name = ?,
            website = ?,
            username = ?,
            email = ?,
            encrypted_password = ?,
            notes = ?,
            category = ?,
            favorite = ?,
            updated_at = ?
        WHERE id = ?
        """

        self.cursor.execute(
            query,
            (
                name,
                website,
                username,
                email,
                encrypted_password,
                notes,
                category,
                favorite,
                updated_at,
                credential_id,
            ),
        )

        self.connection.commit()

    def delete_credential(
        self,
        credential_id: int,
    ) -> None:

        query = """
        DELETE FROM credentials
        WHERE id = ?
        """

        self.cursor.execute(
            query,
            (credential_id,),
        )

        self.connection.commit()

    def search_credentials(
        self,
        keyword: str,
    ) -> list[Credential]:

        query = """
        SELECT *
        FROM credentials
        WHERE
            name LIKE ?
            OR website LIKE ?
            OR username LIKE ?
            OR email LIKE ?
        ORDER BY name
        """

        pattern = f"%{keyword}%"

        self.cursor.execute(
            query,
            (
                pattern,
                pattern,
                pattern,
                pattern,
            ),
        )

        rows = self.cursor.fetchall()

        return [
            self._row_to_credential(row)
            for row in rows
        ]

    # ----------------------------------------------------
    # Close Database
    # ----------------------------------------------------

    def close(self) -> None:
        self.connection.close()