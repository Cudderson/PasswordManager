import mysql.connector

# Connect to database
pw_db = mysql.connector.connect(
    host='localhost',
    user='cudderson',
    passwd='baseball2',
    database='pw_db'
)

# NOTE: SQL db will not be uploaded to github. instead, just include a copy of the schema.
# TASK: set up table structure for project
#   - one table holding user info, one holding (encrypted) passwords. attached by primary key 'entry'
# TASK: successfully read/write to database
# TASK: successfully read/write to database with fernet

# cursor for interacting with database
my_cursor = pw_db.cursor()

# pw_db.commit() <-- must run this line to commit changes to database
# my_cursor.execute("CREATE TABLE users (entry int AUTO_INCREMENT PRIMARY KEY, username VARCHAR(50), site VARCHAR(50))")
# my_cursor.execute("INSERT INTO users (username, site) VALUES (%s,%s)", ("Lucy", "Youtube"))
# my_cursor.execute("CREATE TABLE Passwords (entry int AUTO_INCREMENT PRIMARY KEY, password VARCHAR(50))")
pw_db.commit()
