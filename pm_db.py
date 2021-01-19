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
    my_cursor.execute('CREATE TABLE Sites (entryID int AUTO_INCREMENT, '
                      'Site VARCHAR(100) NOT NULL, '
                      'PRIMARY KEY (entryID))')

    my_cursor.execute('CREATE TABLE Passwords '
                      '(entryID int AUTO_INCREMENT, '
                      'Passwords VARCHAR(50) NOT NULL, '
                      'FOREIGN KEY (entryID) REFERENCES Sites(entryID))')

    my_cursor.execute('CREATE TABLE CRYPT '
                      '(crypt_key VARBINARY(100))')

    pw_db.commit()


def create_crypt_key():
    """
    Checks mysql table for a Fernet key and stores a newly generated one if it does not exist
    """

    #create a crypt key
    crypt_key = Fernet.generate_key() # key is type = bytes


    #query for creating crypt_key table
    key_table_query = 'CREATE TABLE CRYPT ' \
                      '(key_id int AUTO_INCREMENT, ' \
                      'crypt_key BINARY(100) NOT NULL, ' \
                      'PRIMARY KEY (key_id))'
    my_cursor.execute(key_table_query)
    pw_db.commit()

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


def read_one_entry(site_to_find):
    """Displays the password for a user-specified site"""

    read_one_query = 'SELECT sites.site, passwords.passwords ' \
                     'FROM sites, passwords ' \
                     'WHERE sites.entryid = passwords.entryid ' \
                     'AND sites.site = (%s) '

    # move the dialogue to the script
    # site_to_find = input("Specify the name of the site for the password you need. (ex. 'Twitter'): ")
    my_cursor.execute(read_one_query, (site_to_find,))
    one_entry = my_cursor.fetchone()
    print(one_entry)


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
# TASK*: successfully read/write to database with fernet
# TASK: mirror functionality from original passwordmanager program (master password later)

# Table structure (encryption later):
#   1: Sites (entry_number (PK), site_name)
#   2: Passwords (entry_number (FK), password)

#  -------------------working syntax--------------------------
