from utils.password_generator import PasswordGenerator

password = PasswordGenerator.generate()

print(password)
print(len(password))