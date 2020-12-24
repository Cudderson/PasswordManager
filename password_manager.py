
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

# Let's start by getting info to read/write from file successfully with encryption
#a = input('Enter data: ')
#a = a.encode("UTF-8") # a in bytes
#encrypted = fk.encrypt(a)
#print(encrypted) # encrypted message in bytes
#with open("my_passwords.txt", "wb") as f:
#    f.write(encrypted)
#print("data in file....attempting to retrieve and decrypt....")
#with open("my_passwords.txt", "rb") as f:
#    secret = f.read()
#decrypted = fk.decrypt(secret)
#print(decrypted)
#decrypted = decrypted.decode()
#print(decrypted)
# The above is a working example of encryption/decryption with files

# Next, let's get it working where the user can continually add/access data
# Needs new format. Perhaps the data could be converted as one single string?
# Maybe we can turn encrypted bytes into a string, then save to file (would make working with files easier
a = input("Username: ")
b = input("Password: ")
c = "Your password for " + a + " is: " + b
c = c.encode("UTF-8")
print(c)
secret = fk.encrypt(c)
secret = secret.decode()

with open("my_passwords.txt", "a") as f:
    f.write(secret)
    f.write("\n")

with open("my_passwords.txt", "r") as f:
    line = f.readline()
    while line != "":
        line = line.encode()
        decrypted = fk.decrypt(line)
        print(decrypted)
        line = f.readline()

