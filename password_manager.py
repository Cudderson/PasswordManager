from os import path
from cryptography.fernet import Fernet
import time

def Introduction():
    print("Welcome to Password Manager!")
    time.sleep(.2)
    print("Your passwords will be encrypted and decrypted for viewing here.")
    time.sleep(1)

def CreateCryptKey():
    if path.isfile('encryption_key.txt'):
        pass
    else:
        with open("encryption_key.txt", "wb") as new_file:  # 'wb' so we can write bytes
            crypt_key = Fernet.generate_key()
            new_file.write(crypt_key)  # key still in bytes
            new_file.close()

    if path.isfile('my_passwords.txt'):
        pass
    else:
        with open("my_passwords.txt", "x"):
            pass

def Requirements():
    CreateCryptKey()
    with open("encryption_key.txt", "rb") as f:
        crypt_key = f.read()
        f.close()
    global fk
    fk = Fernet(crypt_key)

def AddPassword():
    new_id = input("New ID (ex. 'Twitter'): ")
    time.sleep(.8)
    new_pass = input("New Password for " + new_id + ": ")
    time.sleep(.8)
    plain_string = "Your password for " + new_id + " is: " + new_pass
    time.sleep(.8)
    plain_string = plain_string.encode("UTF-8")
    secret = fk.encrypt(plain_string)
    secret = secret.decode()

    with open("my_passwords.txt", "a") as f:
        f.write(secret)
        f.write("\n")
        print("\nSuccessfully encrypted and saved data for ID: " + new_id + " with password: " + new_pass)
        time.sleep(1)

def ViewPasswords():
    print("Decrypting your file...")
    time.sleep(2)
    with open("my_passwords.txt", "r") as f:
        line = f.readline()
        while line != "":
            line = line.encode()
            decrypted = fk.decrypt(line)
            print(decrypted.decode())
            line = f.readline()
    time.sleep(1)

def ModifyPassword():
    print("Decrypting file...")
    time.sleep(.8)
    print("\nMake sure to type ID/Password identical to how it is provided. Otherwise, changes may not commit!\n")
    time.sleep(.8)
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
    time.sleep(.8)
    id_to_mod = input("\nPlease input the ID or Password  you would like to modify/remove (ex. 'Playstation': ")
    time.sleep(.8)
    for data in temp_list:
        z = data.find(id_to_mod)
        if z == -1:
            pass
        else:
            print("\n" + data)
            time.sleep(.8)
            print("\nWould you like to modify your password for " + id_to_mod + ", or remove it from record?: ")
            mod_or_rem = input("Type 'm' to modify\n"
                               "Type 'r' to remove\n"
                               "Type 'q' to quit: ")
            if mod_or_rem == 'r':
                temp_list.remove(data)
                with open("my_passwords.txt", "w") as f:
                    for plain_data in temp_list:
                        plain_data = plain_data.encode("UTF-8")
                        e_data = fk.encrypt(plain_data)
                        e_data = e_data.decode()
                        f.write(e_data)
                        f.write("\n")
                time.sleep(.8)
                print("\nSuccessfully deleted data for " + id_to_mod + ".")
            elif mod_or_rem == 'm':
                pass_to_mod = input("Enter your current password for " + id_to_mod + ": ")
                new_pass = input("Enter your new password for " + id_to_mod + ": ")
                time.sleep(.8)
                print("Ready to change password for " + id_to_mod + " from " + pass_to_mod + " to " + new_pass + ",")
                confirm_new_pass = input("Type 'confirm' to apply change, or type 'q' to quit: ")
                if confirm_new_pass == 'confirm':  # this entire 'if' works as intended
                    temp_list.remove(data)
                    temp_list.append(data.replace(pass_to_mod, new_pass))
                    print("New data:")
                    print(temp_list)
                    with open("my_passwords.txt", "w") as f:
                        for plain_data in temp_list:
                            plain_data = plain_data.encode("UTF-8")
                            e_data = fk.encrypt(plain_data)
                            e_data = e_data.decode()
                            f.write(e_data)
                            f.write("\n")
                    time.sleep(.8)
                    print("\nNew data successfully saved.")
                    break
                else:
                    print("\nOperation cancelled. Nothing was altered.")
            else:
                print("\nOperation cancelled. Nothing was altered.")

def ViewEncryptedFile():
    print("Here is your secret encrypted data on file:\n")
    time.sleep(.8)
    with open("my_passwords.txt", "r") as f:
        line = f.read()
        print(line)
    time.sleep(.8)
    print("To decrypt this data and view it, type 'v' in the prompt.")

# program start:
Requirements()
Introduction()
while True:
    mode = input("\nType 'v' to view your passwords\n"
                 "Type 'a' to add a new password\n"
                 "Type 'm' to modify passwords\n"
                 "Type 'e' to view your encrypted file\n"
                 "Type 'q' to quit: ")
    if mode == 'v':
        print("\n")
        ViewPasswords()
    elif mode == 'a':
        print("\n")
        AddPassword()
    elif mode == 'm':
        print("\n")
        ModifyPassword()
    elif mode == 'q':
        print("\n" + "Quitting program. Thank you for using Password Manager.")
        time.sleep(.4 )
        quit()
    elif mode == 'e':
        print("\n")
        ViewEncryptedFile()
    else:
        print("\n" + "Your input was not recognized. Please enter one of the given commands.")