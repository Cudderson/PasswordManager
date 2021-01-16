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
#                 'Site VARCHAR(100) NOT NULL, '
#                 'PRIMARY KEY (entryID))')

# my_cursor.execute('CREATE TABLE Passwords '
#                   '(entryID int AUTO_INCREMENT, '
#                   'Passwords VARCHAR(50) NOT NULL, '
#                   'PRIMARY KEY (entryID))')

# writing = working(second argument in execute is a tuple, that is why ',' is included) (should be same for other table)
# query = 'INSERT INTO Sites (Site) VALUES (%s)'
# site_name = 'reddit'
# my_cursor.execute(query, (site_name,))
# pw_db.commit()

# query2 = 'INSERT INTO Passwords (Passwords) VALUES (%s)'
# p_name = 'tiger123'
# my_cursor.execute(query2, (p_name,))
# pw_db.commit()

# reading all from a column:
query3 = 'SELECT * FROM Sites'
my_cursor.execute(query3)
x = my_cursor.fetchall()
for x in x:
    print(x)
# pw_db.commit()
# -----------------------------------------------------------------
pw_db.commit()
