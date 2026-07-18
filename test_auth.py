from auth.auth_manager import AuthenticationManager

auth = AuthenticationManager()

# First-time registration
if not auth.user_exists():
    print("Creating master password...")
    auth.register("Zaheer@123")

print("Correct password:", auth.login("Zaheer@123"))
print("Wrong password:", auth.login("Password123"))