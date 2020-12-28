
import os.path
from os import path
from cryptography.fernet import Fernet
import time

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

# All current functionality working.
# Next, work on dialogue smoothness/readability, and patch holes in the dialogue

def AddPassword():
    new_id = input("New ID (ex. 'Twitter'): ")
    time.sleep(1)
    new_pass = input("New Password for " + new_id + ": ")
    time.sleep(1)
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

def ModifyPassword():
    temp_list = []
    with open("my_passwords.txt", "r") as f:
        line = f.readline()
        while line != "":
            line = line.encode()
            decrypted = fk.decrypt(line)
            decrypted = decrypted.decode()
            print(decrypted)
            temp_list.append(decrypted)
            line = f.readline()
    print(temp_list)
    id_to_mod = input("Please input the ID you would like to modify/remove (ex. 'Playstation': ")
    for data in temp_list:
        z = data.find(id_to_mod)
        if z == -1:
            pass
        else:
            print(data)
            print("Would you like to modify your password for " + id_to_mod + ", or remove it from record?: ")
            mod_or_rem = input("Type 'm' to modify\n"
                               "Type 'r' to remove\n"
                               "Type 'q' to quit: ")
            if mod_or_rem == 'r': # this 'if' works as intended!
                temp_list.remove(data)
                with open("my_passwords.txt", "w") as f:
                    for plain_data in temp_list:
                        plain_data = plain_data.encode("UTF-8")
                        e_data = fk.encrypt(plain_data)
                        e_data = e_data.decode()
                        f.write(e_data)
                        f.write("\n")
                    print("DONEZO")
            elif mod_or_rem == 'm':
                pass_to_mod = input("Enter your current password for " + id_to_mod + ": ")
                new_pass = input("Enter your new password for " + id_to_mod + ": ")
                print("Ready to change password for " + id_to_mod + " from " + pass_to_mod + " to " + new_pass + ",")
                confirm_new_pass = input("Type 'confirm' to apply change, or type 'q' to quit: ")
                if confirm_new_pass == 'confirm': #this entire 'if' works as intended
                    temp_list.remove(data)
                    temp_list.append(data.replace(pass_to_mod, new_pass))
                    print(temp_list)
                    print("^^^new data")
                    with open("my_passwords.txt", "w") as f:
                        for plain_data in temp_list:
                            plain_data = plain_data.encode("UTF-8")
                            e_data = fk.encrypt(plain_data)
                            e_data = e_data.decode()
                            f.write(e_data)
                            f.write("\n")
                    print("DONE")
                    break
                else:
                    print("Operation cancelled. Nothing was altered.")
                    quit()
            else:
                print("Operation cancelled. Nothing was altered.")
                quit()

while True:
    mode = input("Welcome to Password Manager!\n"
          "Type 'v' to view your passwords\n"
          "Type 'a' to add a new password\n"
          "Type 'm' to modify passwords: ")
    if mode == 'v':
        ViewPasswords()
    elif mode == 'a':
        AddPassword()
    elif mode == 'm':
        ModifyPassword()
    else:
        break