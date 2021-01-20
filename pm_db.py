import mysql.connector

from cryptography.fernet import Fernet

# FERNET BRANCH - get encryption working and create a mysql table to store the crypt_key
# NOTES: may need to change the table to accept bytes rather than UTF-8

# Connect to database
pw_db = mysql.connector.connect(
    host='localhost',
    user='cudderson',
    passwd='baseball2',
    database='pw_db'
)

# cursor for interacting with database
my_cursor = pw_db.cursor()


def create_tables():

    create_site_table_query = 'CREATE TABLE Sites (entryID int AUTO_INCREMENT, ' \
                              'Site VARCHAR(100) NOT NULL, ' \
                              'PRIMARY KEY (entryID))'

    create_pass_table_query = 'CREATE TABLE Passwords ' \
                              '(entryID int AUTO_INCREMENT, ' \
                              'Passwords BINARY(120) NOT NULL, ' \
                              'FOREIGN KEY (entryID) REFERENCES Sites(entryID))'

    key_table_query = 'CREATE TABLE CRYPT ' \
                      '(key_id int AUTO_INCREMENT, ' \
                      'crypt_key BINARY(120) NOT NULL, ' \
                      'PRIMARY KEY (key_id))'

    my_cursor.execute(key_table_query)
    my_cursor.execute(create_site_table_query)
    my_cursor.execute(create_pass_table_query)
    pw_db.commit()


def create_crypt_key():
    """
    Checks mysql table for a Fernet key and stores a newly generated one if it does not exist
    """

    #create a crypt key
    crypt_key = Fernet.generate_key() # key is type = bytes


    #query for storing crypt_key:
    crypt_query = 'INSERT INTO Crypt (crypt_key) VALUES (%s)'
    my_cursor.execute(crypt_query, (crypt_key,))
    pw_db.commit()


def get_crypt_key():
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

    pass_to_encrypt = pass_to_encrypt.encode("UTF-8")
    return fk.encrypt(pass_to_encrypt)


def decrypt_password(pass_to_decrypt):
    """Decrypts and returns the passed value for the user to read"""

    pass_to_decrypt = fk.decrypt(pass_to_decrypt)
    return pass_to_decrypt.decode()


def insert_entry(site_name, password):
    """Adds a single entry to mysql database (site, password)"""

    # writing = working(second argument in execute is a tuple, that is why ',' is included) (pass table same)
    insert_query_site = 'INSERT INTO Sites (Site) VALUES (%s)'
    insert_query_pass = 'INSERT INTO Passwords (Passwords) VALUES (%s)'
    my_cursor.execute(insert_query_site, (site_name,))
    my_cursor.execute(insert_query_pass, (password,))
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

    # move the dialogue to the script
    # site_to_find = input("Specify the name of the site for the password you need. (ex. 'Twitter'): ")
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

# NOTE: SQL db will not be uploaded to github. instead, just include a copy of the schema. (seed info)
# TASK: set up table structure for project***
# TASK: successfully read/write to database***
# TASK: successfully read/write to database with fernet***
# TASK*: mirror functionality from original passwordmanager program (master password later)


#  -------------------working syntax--------------------------

# full-cryptography flow: -------------

# 1: get key and instantiate it:
# my_key = get_crypt_key()
# fk = Fernet(my_key)

# 2: encode data with UTF-8
# 3: 'fk.encrypt()' the data
# 4: mysql INSERT query statement
# 5: commit()
# 6: RETRIEVE:
# 7: mysql SELECT query statement
# 8: execute, fetchone(), and take first value of tuple (what you want)
# 9: encode data with UTF-8
# 10: 'fk.decrypt()' the data

# -----------------------------------

# SCRIPT:


my_key = get_crypt_key()
fk = Fernet(my_key)

read_all_entries()
# simulate adding an entry, then retrieving it
# create func that does the encryption. 'insert' func should only write data to db
# a = input("new site name: ")
#b = input("new pass: ")
#print(a, b)
#encrypted_pass = encrypt_password(b) # send this to insert query
#print(encrypted_pass)
#insert_entry(a, encrypted_pass)

# all working. now, let's get that password back and decrypt it
# create func that decrypts the password
#

#desired = input("site name for pass looking for: ")
#x = read_one_entry(desired)
#y = x[1] # encrypted password
#print(y)
#y = y.encode("UTF-8") # encoding for decryption
#print(y)
#z = decrypt_password(y) # password in english
#print(z)

# let's start on the script:

print("Welcome to Password Manager!\n"
      "Your passwords will be encrypted and decrypted for viewing here.\n"
      "What would you like to do today?\n")

while True:

    mode = input("Please enter a letter to access one of the following modes:\n"
                 "\t- Press 'a' to add a new password\n"
                 "\t- Press 'v' to view a password\n"
                 "\t- Press 'q' to quit program"
                 "\nEnter mode : "
                 )

    if mode == 'a':

        new_site = input("Creating a new entry.\n"
                         "Please type the name of the site for your new password (youtube): ")
        new_pass = input(f"Please type your new password for {new_site}: ")

        pass_confirm = input(f"For confirmation, type your new password for {new_site} again: ")
        if new_pass == pass_confirm:

            print(f"Ready to insert new entry for site: '{new_site}' with password: {new_pass}")
            confirm_new_entry = input("Type 'confirm' to proceed if this is correct. ('q' to quit)")

            if confirm_new_entry == 'confirm':
                # encrypt password and send entry to insert_entry

                encrypted_pass = encrypt_password(new_pass)
                insert_entry(new_site, encrypted_pass)
                print("\nNew entry successful!")

            elif confirm_new_entry == 'q':
                print("Quitting operation. No changes were made.\n")
                pass
            else:
                print("Command not recognized.\n")
        else:
            print("Passwords did not match. No changes were made.")
    elif mode == 'v':
        site_to_find = input("Please enter the site name for the password you need. (twitter): ")
        desired_pass = read_one_entry(site_to_find)
        desired_pass = desired_pass[1]
        print(f"Here is your encrypted password for {site_to_find}:\n{desired_pass}")
        input("type 'decrypt' to view your password:")
        desired_pass = desired_pass.encode("UTF-8")
        password = decrypt_password(desired_pass)
        print(f"Your password for {site_to_find} is: {password}")
        input("Press enter to continue: ")
    elif mode == 'q':
        quit()

# fix foreign key bug
