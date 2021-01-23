import mysql.connector

from cryptography.fernet import Fernet

import crypt_mod, sql_mod

# Structure project and deploy


def requirements():
    #split into 2 requirments funcs, one for sql, one for fernet
    """Prepares db schema and handles creation of encryption key and master key"""

    tables_exist()

    if not tables_exist():

        create_tables()
        create_crypt_key()
        master_to_store = create_master_key()
        encrypted_master = encrypt_password(master_to_store)
        insert_master(encrypted_master)
        print(f"\nNew master password '{master_to_store}' was encrypted and stored. Don't forget it!!!")

    else:
        pass
        # requirements satisfied


def create_crypt_key():
    """
    Checks mysql table for a Fernet key and stores a newly generated one if it does not exist
    """

    crypt_key = Fernet.generate_key() # key is type = bytes
    #insert crypt key func:
    crypt_query = 'INSERT INTO Crypt (crypt_key) VALUES (%s)'
    my_cursor.execute(crypt_query, (crypt_key,))
    pw_db.commit()


def create_master_key():
    """Creates and returns new master password"""

    print("\nBefore we begin, let's set a master password for this program.\n"
          "Your master password will be required to access your stored passwords.")

    new_master = input("\nEnter your new master password: ")
    new_master_confirm = input("To confirm, enter your new master password again: ")

    if new_master == new_master_confirm:

        store_new_master_confirm = input(f"\nStore new master password '{new_master}' ? (yes/no): ")

        if store_new_master_confirm == 'yes':

            return new_master

        elif store_new_master_confirm == 'no':

            print("\nNew master password was not created. To use Password Manager, you must create one.")
            return create_master_key()

        else:
            print("\nCommand not recognized. No changes were made.")
            return create_master_key()
    else:
        print("\nPasswords did not match. Nothing was altered.")
        return create_master_key()


def get_master_key():
    """Retrieves, decrypts, and returns master key from db"""

    get_master_query = 'SELECT master.master_key ' \
                       'FROM master ' \
                       'WHERE master.master_key_id = 1'

    my_cursor.execute(get_master_query)
    master_key_found = my_cursor.fetchone()
    # split this up into 2 funcs, sql and fernet
    decrypted_master = fk.decrypt(master_key_found[0].encode())

    return decrypted_master


def master_login():
    # goes in sql mods
    """Retrieves master key and allows access to db if matched correctly"""

    master_key = get_master_key().decode()
    login_master = input("\nEnter your master password to begin using Password Manager: ")

    if login_master == master_key:

        print("Access granted!\n")
        access_granted = True

        return access_granted

    else:

        print("Uh oh, that is not your master password. Try again.")
        return master_login()


requirements()
# requirments2()
my_key = get_crypt_key()
fk = Fernet(my_key)
master_login()


print("Welcome to Password Manager!\n"
      "Your passwords will be encrypted and decrypted for viewing here.\n"
      "What would you like to do today?\n")

while True:

    mode = input("\nPlease enter a letter to access one of the following modes:\n"
                 "\t- Press 'a' to add a new password\n"
                 "\t- Press 'v' to view a password\n"
                 "\t- Press 's' to view all sites you have stored\n"
                 "\t- Press 'm' to modify an existing password\n"
                 "\t- Press 'q' to quit program\n"
                 "\nEnter mode : "
                 )

    if mode == 'a':

        new_site = input("\nCreating a new entry.\n"
                         "Please type the name of the site for your new password (ex. 'youtube'): ")
        new_pass = input(f"\nPlease type your new password for {new_site}: ")

        pass_confirm = input(f"\nFor confirmation, type your new password for {new_site} again: ")
        if new_pass == pass_confirm:

            print(f"\nReady to insert new entry for site '{new_site}' with password: {new_pass}")
            confirm_new_entry = input("\nType 'confirm' to proceed if this is correct. ('q' to quit): ")

            if confirm_new_entry == 'confirm':
                # encrypt password and send entry to insert_entry

                encrypted_pass = encrypt_password(new_pass)
                insert_entry(new_site, encrypted_pass)
                print("\nNew entry successful!\n")

            elif confirm_new_entry == 'q':
                print("Quitting operation. No changes were made.\n")
                pass

            else:
                print("Command not recognized.\n")

        else:
            print("Passwords did not match. No changes were made.")

    elif mode == 'v':

        site_to_find = input("\nPlease enter the site name for the password you need. (twitter): ")
        entry_to_view = entry_exists(site_to_find)

        if entry_to_view is not None:

            desired_pass = read_one_entry(site_to_find)
            desired_pass = desired_pass[1]
            print(f"\nHere is your encrypted password for {site_to_find}:\n{desired_pass}")
            confirm_decrypt = input("\nType 'decrypt' to view your password: ")

            if confirm_decrypt == 'decrypt':

                desired_pass = desired_pass.encode("UTF-8")
                password = decrypt_password(desired_pass)
                print(f"\nYour password for {site_to_find} is: {password}")
                input("\nPress enter to continue: ")

            else:
                print("\nCommand not recognized. No changes were made.\n")

        else:
            print(f"\nCould not find entry with site name '{site_to_find}'")
            print(f"Cancelling operation. Nothing was altered.")

    elif mode == 'm':

        site_to_modify = input("\nPlease enter the site name for the password you are modifying: ")
        # make sure site name exists in db:
        found_entry = entry_exists(site_to_modify)

        if found_entry is not None:

            found_site = found_entry[0]
            found_pass = found_entry[1]

            print(f"\nReady to change password for {found_site}")

            # decrypt current password
            x = decrypt_password(found_pass.encode("UTF-8"))

            print(f"\nCurrent password for {found_site} is {x}")
            modded_pass = input(f"\nEnter your new password for {found_site}: ")
            confirm_modded_pass = input(f"Confirm new password for {found_site}: ")

            if modded_pass == confirm_modded_pass:

                y = encrypt_password(modded_pass)
                modify_one_password(found_site, y)

                print(f"\nNew entry added successfully!"
                      f"\nYour new password for {found_site} is '{modded_pass}'\n")

            else:
                print("\nNew passwords did not match. No changes were made.\n")

        else:
            print(f"Could not find site '{site_to_modify}' in database.")

    elif mode == 's':

        print("\nHere are the sites you have stored. To get a password, press 'v'\n")
        read_all_entries()

    elif mode == 'q':
        print("\nSee you next time! Quitting program.")
        quit()

    else:
        print("\nCommand not recognized.\n")

# NOTE: SQL db will not be uploaded to github. instead, just include a copy of the schema. (seed info)
