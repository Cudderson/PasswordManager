import mysql.connector

from cryptography.fernet import Fernet

# Structure project and deploy

# Connect to database
pw_db = mysql.connector.connect(
    host='localhost',
    user='cudderson',
    passwd='baseball2',
    database='pw_db'
)

# cursor for interacting with database
my_cursor = pw_db.cursor()


def requirements():
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


def create_tables():
    """Creates necessary tables in db for program to run correctly"""

    create_site_table_query = 'CREATE TABLE Sites (entryID int AUTO_INCREMENT, ' \
                              'Site VARCHAR(100) NOT NULL, ' \
                              'PRIMARY KEY (entryID))'

    create_pass_table_query = 'CREATE TABLE Passwords ' \
                              '(entryID int AUTO_INCREMENT, ' \
                              'Passwords BINARY(100) NOT NULL, ' \
                              'FOREIGN KEY (entryID) REFERENCES Sites(entryID))'

    key_table_query = 'CREATE TABLE Crypt ' \
                      '(key_id int AUTO_INCREMENT, ' \
                      'crypt_key BINARY(120) NOT NULL, ' \
                      'PRIMARY KEY (key_id))'

    create_master_table_query = 'CREATE TABLE Master ' \
                                '(master_key_id int AUTO_INCREMENT, ' \
                                'master_key BINARY(100) NOT NULL, ' \
                                'PRIMARY KEY (master_key_id))'

    my_cursor.execute(key_table_query)
    my_cursor.execute(create_site_table_query)
    my_cursor.execute(create_pass_table_query)
    my_cursor.execute(create_master_table_query)
    pw_db.commit()


def create_crypt_key():
    """
    Checks mysql table for a Fernet key and stores a newly generated one if it does not exist
    """

    crypt_key = Fernet.generate_key() # key is type = bytes

    crypt_query = 'INSERT INTO Crypt (crypt_key) VALUES (%s)'
    my_cursor.execute(crypt_query, (crypt_key,))
    pw_db.commit()


def get_crypt_key():
    """Finds and returns encryption key in db"""

    get_crypt_query = 'SELECT crypt.crypt_key ' \
                      'FROM crypt ' \
                      'WHERE key_id = 1'

    my_cursor.execute(get_crypt_query)
    stored_key = my_cursor.fetchone()

    # 'fetchone()' returns a union or tuple. To get the key, we take the first value:
    stored_key = stored_key[0]
    return stored_key


def encrypt_password(pass_to_encrypt):
    """Encrypts and returns the passed value as a Fernet token"""

    temp_key = get_crypt_key()
    tk = Fernet(temp_key)

    pass_to_encrypt = pass_to_encrypt.encode("UTF-8")
    return tk.encrypt(pass_to_encrypt)


def decrypt_password(pass_to_decrypt):
    """Decrypts and returns the passed value for the user to read"""

    pass_to_decrypt = fk.decrypt(pass_to_decrypt)
    return pass_to_decrypt.decode()


def insert_master(master_password):
    """Inserts user master password to db"""

    insert_master_query = 'INSERT INTO Master (master_key) ' \
                          'VALUES (%s)'

    my_cursor.execute(insert_master_query, (master_password,))
    pw_db.commit()


def insert_entry(new_site_name, new_password):
    """Adds a single entry to mysql database (site, password)"""

    insert_query_site = 'INSERT INTO Sites (Site) VALUES (%s)'
    insert_query_pass = 'INSERT INTO Passwords (Passwords) VALUES (%s)'
    my_cursor.execute(insert_query_site, (new_site_name,))
    pw_db.commit()
    my_cursor.execute(insert_query_pass, (new_password,))
    pw_db.commit()


def read_all_entries():
    """Displays all database information, in the form: (entryid, site, password)"""

    read_all_query = 'SELECT sites.entryid, sites.site, passwords.passwords ' \
                     'FROM sites, passwords ' \
                     'WHERE sites.entryid = passwords.entryid'

    my_cursor.execute(read_all_query)
    all_entries = my_cursor.fetchall()

    for entry in all_entries:
        print(entry)


def read_one_entry(site_to_match):
    """Displays the password for a user-specified site"""

    read_one_query = 'SELECT sites.site, passwords.passwords ' \
                     'FROM sites, passwords ' \
                     'WHERE sites.entryid = passwords.entryid ' \
                     'AND sites.site = (%s) '

    my_cursor.execute(read_one_query, (site_to_match,))
    one_entry = my_cursor.fetchone()
    return one_entry


def modify_one_password(site_to_mod, pass_to_mod):
    """Updates/Modifies the password for a user-given site"""

    modify_pass_query = 'UPDATE Passwords, Sites ' \
                        'SET passwords = (%s) ' \
                        'WHERE sites.site = (%s) ' \
                        'AND sites.entryid = passwords.entryid'

    my_cursor.execute(modify_pass_query, (pass_to_mod, site_to_mod))
    pw_db.commit()


def entry_exists(site):
    """Makes sure that a given entry exists in database before handling"""

    entry_exists_query = "SELECT sites.site, passwords.passwords " \
                         "FROM Sites, Passwords " \
                         "WHERE sites.site = (%s) " \
                         "AND sites.entryid = passwords.entryid"

    my_cursor.execute(entry_exists_query, (site,))
    existing_entry = my_cursor.fetchone()
    return existing_entry


def tables_exist():
    """Checks if db schema is set up properly and returns a boolean"""

    tables_in_db = False
    tables_exist_query = 'SHOW TABLES'
    my_cursor.execute(tables_exist_query)
    my_tables = my_cursor.fetchall()

    if len(my_tables) == 4:
        tables_in_db = True

    return tables_in_db


def create_master_key():
    """Creates and returns master password if it does not exist"""

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
    decrypted_master = fk.decrypt(master_key_found[0].encode())

    return decrypted_master


def master_login():
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