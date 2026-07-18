import secrets
import base64
import hashlib
import hmac



def generate_salt(length: int = 16) -> str:
    """
    Generate a cryptographically secure random salt.

    Args:
        length: Number of random bytes.

    Returns:
        Base64-encoded salt as a string.
    """

    # Generate secure random bytes
    salt = secrets.token_bytes(length)

    # Convert bytes into Base64 text
    encoded_salt = base64.b64encode(salt).decode("utf-8")

    return encoded_salt

def hash_password(password: str, salt: str) -> str:
    """
    Derive a secure password hash using PBKDF2-HMAC-SHA256.

    Args:
        password: The master password entered by the user.
        salt: The Base64-encoded salt stored in the database.

    Returns:
        Base64-encoded derived key.
    """

    # Convert the Base64 salt back into bytes
    salt_bytes = base64.b64decode(salt)

    # Derive a secure key from the password
    derived_key = hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode("utf-8"),
        salt=salt_bytes,
        iterations=600_000
    )

    # Convert the derived key to Base64 for storage
    return base64.b64encode(derived_key).decode("utf-8")

def verify_password(password: str, stored_hash: str, salt: str) -> bool:
    """
    Verify whether the provided password matches the stored hash.

    Args:
        password: Password entered by the user.
        stored_hash: Hash stored in the database.
        salt: Base64-encoded salt stored in the database.

    Returns:
        True if the password is correct, False otherwise.
    """

    # Generate a new hash using the entered password and stored salt
    new_hash = hash_password(password, salt)

    # Compare hashes securely
    return hmac.compare_digest(new_hash, stored_hash)

def derive_encryption_key(password: str, salt: str) -> bytes:
    """
    Derive a Fernet-compatible encryption key from
    the master password and stored salt.
    """

    # Convert Base64 salt back to bytes
    salt_bytes = base64.b64decode(salt)

    # Derive 32 bytes using PBKDF2
    key = hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode(),
        salt=salt_bytes,
        iterations=100_000,
        dklen=32,
    )

    # Fernet expects a URL-safe Base64 encoded key
    return base64.urlsafe_b64encode(key)