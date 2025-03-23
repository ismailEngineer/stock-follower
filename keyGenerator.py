from cryptography.fernet import Fernet
import getpass

key = Fernet.generate_key()

with open('logInURP.key', 'wb') as key_file:
    key_file.write(key)

cipher_suite = Fernet(key)

username = input("Enter username login (email) : ")
password = getpass.getpass("Enter your password (URP) : ")

encrypted_password = cipher_suite.encrypt(password.encode())

with open('config.yml', 'a+') as config_file:
    config_file.write(f"username: {username}\npassword: {encrypted_password.decode()}\n")
