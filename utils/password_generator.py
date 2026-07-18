import secrets
import string


class PasswordGenerator:
    """
    Generates secure random passwords.
    """

    @staticmethod
    def generate(
        length: int = 20,
        uppercase: bool = True,
        lowercase: bool = True,
        digits: bool = True,
        symbols: bool = True,
    ) -> str:

        characters = ""

        if uppercase:
            characters += string.ascii_uppercase

        if lowercase:
            characters += string.ascii_lowercase

        if digits:
            characters += string.digits

        if symbols:
            characters += "!@#$%^&*()-_=+[]{}<>?"

        if not characters:
            raise ValueError(
                "At least one character set must be selected."
            )

        return "".join(
            secrets.choice(characters)
            for _ in range(length)
        )