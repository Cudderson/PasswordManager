import mysql.connector


# Connect to database
pw_db = mysql.connector.connect(
    host='localhost',
    user='cudderson',
    passwd='baseball2',
    database='pw_db'
)

# cursor for interacting with database
my_cursor = pw_db.cursor()


def tables_exist():
    """Checks if db schema is set up properly and returns a boolean"""

    tables_in_db = False
    tables_exist_query = 'SHOW TABLES'
    my_cursor.execute(tables_exist_query)
    my_tables = my_cursor.fetchall()

    if len(my_tables) == 4:
        tables_in_db = True

    return tables_in_db


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


def insert_entry(new_site_name, new_password):
    """Adds a single entry to mysql database (site, password)"""

    insert_query_site = 'INSERT INTO Sites (Site) VALUES (%s)'
    insert_query_pass = 'INSERT INTO Passwords (Passwords) VALUES (%s)'
    my_cursor.execute(insert_query_site, (new_site_name,))
    pw_db.commit()
    my_cursor.execute(insert_query_pass, (new_password,))
    pw_db.commit()


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


def insert_master(master_password):
    """Inserts user master password to db"""

    insert_master_query = 'INSERT INTO Master (master_key) ' \
                          'VALUES (%s)'

    my_cursor.execute(insert_master_query, (master_password,))
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
