from encryption.password_hasher import (
    generate_salt,
    hash_password,
    verify_password,
)

password = "Zaheer@123"

salt = generate_salt()

stored_hash = hash_password(password, salt)

print("Salt:", salt)
print("Stored Hash:", stored_hash)

print("\nCorrect password:")
print(verify_password("Zaheer@123", stored_hash, salt))

print("\nWrong password:")
print(verify_password("WrongPassword", stored_hash, salt))