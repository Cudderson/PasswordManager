import mysql.connector

# Connect to database
pw_db = mysql.connector.connect(
    host='localhost',
    user='cudderson',
    passwd='baseball2',
    database='pw_db'
)

# NOTE: SQL db will not be uploaded to github. instead, just include a copy of the schema. (seed info)
# TASK: set up table structure for project***
# TASK*: successfully read/write to database
# TASK: successfully read/write to database with fernet
# TASK: mirror functionality from original passwordmanager program (master password later)

# Table structure (encryption later):
#   1: Sites (entry_number (PK), site_name)
#   2: Passwords (entry_number (PK), password)


# cursor for interacting with database
my_cursor = pw_db.cursor()
#  -------------------working syntax---------------------------

# queries for creating tables
# my_cursor.execute('CREATE TABLE Sites (entryID int AUTO_INCREMENT, '
#                   'Site VARCHAR(100) NOT NULL, '
#                   'PRIMARY KEY (entryID))')

#  my_cursor.execute('CREATE TABLE Passwords '
#                    '(entryID int AUTO_INCREMENT, '
#                    'Passwords VARCHAR(50) NOT NULL, '
#                    'FOREIGN KEY (entryID) REFERENCES Sites(entryID))')

# writing = working(second argument in execute is a tuple, that is why ',' is included) (should be same for other table)
# query = 'INSERT INTO Sites (Site) VALUES (%s)'
# site_name = 'youtube'
# my_cursor.execute(query, (site_name,))
#  pw_db.commit()

# query2 = 'INSERT INTO Passwords (Passwords) VALUES (%s)'
# p_name = 'banana'
# my_cursor.execute(query2, (p_name,))
# pw_db.commit()

# reading all from a column:
# query3 = 'SELECT * FROM Sites'
# my_cursor.execute(query3)
# x = my_cursor.fetchall()
# for x in x:
#    print(x)
# pw_db.commit()


# displays a single entry. this one displays a specific site and its password, linked by primary key (entryid)
# SELECT sites.entryid, sites.site, passwords.passwords
# FROM sites, passwords
# WHERE sites.entryid = passwords.entryid
# AND sites.site = 'youtube';
# -----------------------------------------------------------------
# create a function for adding a new entry:


def insert_entry(site_name, password):
    # writing = working(second argument in execute is a tuple, that is why ',' is included) (pass table same)
    insert_query_site = 'INSERT INTO Sites (Site) VALUES (%s)'
    insert_query_pass = 'INSERT INTO Passwords (Passwords) VALUES (%s)'
    my_cursor.execute(insert_query_site, (site_name,))
    my_cursor.execute(insert_query_pass, (password,))

# script:


site_to_add = input("Site name: ")
pass_to_add = input("Password: ")
insert_entry(site_to_add, pass_to_add)
pw_db.commit()
