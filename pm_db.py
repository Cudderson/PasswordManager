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

# pw_db.commit() <-- must run this line to commit changes to database
# my_cursor.execute("CREATE TABLE users (entry int AUTO_INCREMENT PRIMARY KEY, username VARCHAR(50), site VARCHAR(50))")

my_cursor.execute("INSERT INTO users (username, site) VALUES (%s,%s)", ("Lucy", "Youtube"))

my_cursor.execute("SELECT * FROM users")
for x in my_cursor:
    print(x)

# pw_db.commit()
