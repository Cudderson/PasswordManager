
# long-term updates
# 1: encrypt password before sending it to file
# 2: create GUI for app
### Open in 'rb' to read bytes!!

import os.path
from os import path
from cryptography.fernet import Fernet

keys = {}  # dict to be read into from file



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
