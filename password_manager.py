from os import path
from cryptography.fernet import Fernet
import time

# This branch will add final features and finalize product
# Next feature: convert strings to f-strings and add proper docstrings
# 2nd feature(maybe): SQL database to parallel file writing, for extra safety

def Introduction():
    with open("pmpin.txt", "r") as f:
        e_master_password = f.read()
        e_master_password = e_master_password.encode()
        master_password = fk.decrypt(e_master_password)
        master_password = master_password.decode()
    print("--------------------------------------------")
    master_user = input("To gain access to Password Manager, please provide your Master password: ")
    time.sleep(1)
    if master_user == master_password:
        print("Access granted!")
        time.sleep(1)
        print("--------------------------------------------")
        print("Welcome to Password Manager!")
        time.sleep(.2)
        print("Your passwords will be encrypted and decrypted for viewing here.")
        time.sleep(1)
    else:
        print("Umm.. that's not the Master password we were looking for.\n")
        print("To try again, enter 't'\n"
              "To get help, enter 'h'\n"
              "To quit, enter 'q'\n")
        retry = input("Enter mode: ")
        if retry == 't':
            Introduction()
        elif retry == 'h':
            print("Luckily, you saved a hint/clue for your Master password!\nHint:\n")
            time.sleep(1)
            with open("master_hint.txt", "r") as f:
                e_hint = f.read()
                e_hint = e_hint.encode()
                hint = fk.decrypt(e_hint)
                hint = hint.decode()
            print(hint + "\n")
            time.sleep(.8)
            print("Let's try again. Rerouting...")
            time.sleep(1)
            Introduction()
        elif retry == 'q':
            time.sleep(1)
            print("Come again!")
            quit()
        else:
            print("Couldn't understand command. Quitting program.")
            time.sleep(.8)
            quit()

def CreateCryptKey():
    if path.isfile('encryption_key.txt'):
        pass
    else:
        with open("encryption_key.txt", "wb") as new_file:  # 'wb' so we can write bytes
            crypt_key = Fernet.generate_key()
            new_file.write(crypt_key)  # key still in bytes
            new_file.close()

def CreateFiles():
    if path.isfile('my_passwords.txt'):
        pass
    else:
        with open("my_passwords.txt", "x"):
            pass

    if path.isfile('pmpin.txt'):
        pass
    else:
        with open("pmpin.txt", "x"):
            pass

    if path.isfile('master_hint.txt'):
        pass
    else:
        with open('master_hint.txt', "x"):
            pass

def Requirements():
    CreateCryptKey()
    CreateFiles()
    with open("encryption_key.txt", "rb") as f:
        crypt_key = f.read()
        f.close()

    global fk
    fk = Fernet(crypt_key)

    with open('pmpin.txt', 'r') as f:
        pin_exists = f.read(1)
    if pin_exists:
        pass
    else:
        time.sleep(1)
        print("Hello! Before we get started, you will need to create a Master password.\n"
              "This 'Master' password will be encrypted before it's saved, so don't forget it!\n"
              "You will need your Master password whenever you want to access Password Manager.\n")
        master_p = input("Enter your new master password: ")
        master_p2 = input("Enter your new master password again: ")
        if master_p == master_p2:
            print("Great! Now, add a hint or clue for your Master password!")
            print("Your hint will be encrypted as well for security.")
            time.sleep(.8)
            hint = input("Hint/Clue for Master password '" + master_p + "': ")
            time.sleep(.8)
            print("\nReady to save new Master password '" + master_p + "' with hint '" + hint + "'")
            time.sleep(.8)
            master_confirm = input("Type 'confirm' to save your Master password and get started!: ")

            if master_confirm == 'confirm':
                time.sleep(1)
                master_e = master_p.encode("UTF-8")
                secret_master = fk.encrypt(master_e)
                secret_master = secret_master.decode()

                hint_e = hint.encode("UTF-8")
                secret_hint = fk.encrypt(hint_e)
                secret_hint = secret_hint.decode()

                with open("pmpin.txt", "w") as f:
                    f.write(secret_master)

                with open("master_hint.txt", "w") as f:
                    f.write(secret_hint)

                print("New master password successfully saved! Enjoy using Password Manager!\n")
                print("-----------------------------------------")
                time.sleep(1)
            else:
                print("Command '" + master_confirm + "' not recognized. Let's try again.")
                Requirements()
        else:
            print("Passwords did not match. Let's try again.")
            Requirements()

def AddPassword():
    new_id = input("New ID (ex. 'Twitter'): ")
    time.sleep(.8)
    new_pass = input("New Password for " + new_id + ": ")
    time.sleep(.8)
    plain_string = "Your password for " + new_id + " is: " + new_pass
    print(plain_string)
    confirm_add = input("If this is correct, type 'confirm', or type 'q' to cancel: ")
    if confirm_add == 'confirm':
        time.sleep(.8)
        plain_string = plain_string.encode("UTF-8")
        secret = fk.encrypt(plain_string)
        secret = secret.decode()

        with open("my_passwords.txt", "a") as f:
            f.write(secret)
            f.write("\n")
            print("\nSuccessfully encrypted and saved data for ID: " + new_id + " with password: " + new_pass)
            time.sleep(1)
    else:
        time.sleep(.8)
        print("\nOperation cancelled. Rerouting to main menu...")
        time.sleep(.8)

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

def ChangeMaster():
    with open("pmpin.txt", "r") as f:
        e_master_password = f.read()
        e_master_password = e_master_password.encode()
        master_password = fk.decrypt(e_master_password)
        master_password = master_password.decode()

    print("Your current master password is: " + master_password + "\n")
    new_master = input("Enter your new master password: ")
    time.sleep(.8)
    new_master2 = input("Enter your new master password again: ")
    time.sleep(.8)
    if new_master == new_master2:
        print("\n" + "Ready to change master password from '" + master_password + "' to '" + new_master + "'\n")
        time.sleep(.8)
        finalize = input("Type 'confirm' to finalize change: ")
        time.sleep(.8)

        if finalize == 'confirm':
            print("\n" + "Before the change is made, please include a hint/clue for your new master password: " + new_master)
            new_hint = input("Hint: ")
            time.sleep(.8)

            new_hint_e = new_hint.encode()
            secret_hint = fk.encrypt(new_hint_e)
            secret_hint = secret_hint.decode()

            new_master_e = new_master.encode()
            secret_master = fk.encrypt(new_master_e)
            secret_master = secret_master.decode()

            with open("pmpin.txt", "w") as f:
                f.write(secret_master)
            with open("master_hint.txt", "w") as f:
                f.write(secret_hint)

            print("\n" + "Your master password has been changed successfully! Don't lose it!!!\n")
            time.sleep(.8)

        else:
            print("\n" + "Command not recognized. Nothing was changed.\n")
            time.sleep(1)
            print("Rerouting...")
            time.sleep(.8)
    else:
        print("Passwords did not match. Nothing was altered.")
        time.sleep(1)

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
                 "Type 'c' to change master password\n"
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
    elif mode == 'c':
        print("\n")
        ChangeMaster()
    else:
        print("\n" + "Your input was not recognized. Please enter one of the given commands.")