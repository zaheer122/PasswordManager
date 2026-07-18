from dataclasses import dataclass

@dataclass
class Credential:
    id: int | None

    name: str
    website: str | None
    username: str | None
    email: str | None

    encrypted_password: str
    password: str | None = None

    password: str | None = None

    notes: str | None = None
    category: str | None = None
    favorite: bool = False

    created_at: str = ""
    updated_at: str = ""