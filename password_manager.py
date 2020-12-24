
import os.path
from os import path
from cryptography.fernet import Fernet

def CreateCryptKey():
    if path.isfile('encryption_key.txt'):
        pass
    else:
        with open("encryption_key.txt", "wb") as new_file: # 'wb' so we can write bytes
            crypt_key = Fernet.generate_key()
            new_file.write(crypt_key) # key still in bytes
            new_file.close()

    if path.isfile('my_passwords.txt'):
        pass
    else:
        with open("my_passwords.txt", "x"):
            pass

# get crypt_key:
CreateCryptKey()

with open("encryption_key.txt", "rb") as f:
    crypt_key = f.read()
    f.close()

fk = Fernet(crypt_key)

def AddPassword():
    new_id = input("New ID (ex. 'Twitter'): ")
    new_pass = input("New Password for " + new_id + ": ")
    plain_string = "Your password for " + new_id + " is: " + new_pass
    plain_string = plain_string.encode("UTF-8")
    print(plain_string)
    secret = fk.encrypt(plain_string)
    secret = secret.decode()

    with open("my_passwords.txt", "a") as f:
        f.write(secret)
        f.write("\n")

def ViewPasswords():
    with open("my_passwords.txt", "r") as f:
        line = f.readline()
        while line != "":
            line = line.encode()
            decrypted = fk.decrypt(line)
            print(decrypted.decode())
            line = f.readline()

# current state: viewing and adding work. Next, it would be good to have functionality for
# changing a password, or deleting one.
while True:
    mode = input("Welcome to Password Manager!\n"
          "Type 'v' to view your passwords\n"
          "Type 'a' to add a new password: ")
    if mode == 'v':
        ViewPasswords()
    elif mode == 'a':
        AddPassword()
    else:
        break