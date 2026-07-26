from pathlib import Path
import secrets
import base64


class SaltManager:
    """
    Handles persistent salts used by the application.
    """

    DATA_DIR = Path("data")

    AUTH_SALT_FILE = DATA_DIR / "auth.salt"
    VAULT_SALT_FILE = DATA_DIR / "vault.salt"

    @classmethod
    def _load_or_create(cls, path: Path) -> str:

        cls.DATA_DIR.mkdir(exist_ok=True)

        if path.exists():
            return path.read_text().strip()

        salt = base64.b64encode(
            secrets.token_bytes(16)
        ).decode()

        path.write_text(salt)

        return salt

    @classmethod
    def get_auth_salt(cls) -> str:
        return cls._load_or_create(
            cls.AUTH_SALT_FILE
        )

    @classmethod
    def get_vault_salt(cls) -> str:
        return cls._load_or_create(
            cls.VAULT_SALT_FILE
        )