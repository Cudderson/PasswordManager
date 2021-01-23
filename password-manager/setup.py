# python cryptography package:
# 'pip install cryptography'

# install mysql from 'mysql.com'

# Command line (from mysql.com):
# mysql --host=localhost --user='your username' --password pw_db
# mysql -h localhost -u 'your username' -p pw_db


# Python db connect:

# pw_db = mysql.connector.connect(
#     host='localhost',
#     user='',  <-- your info
#     passwd='',  <-- your info
#     database='pw_db'
# )

# MySQL db schema (setup handled in 'pm_db.py' script):

#    create_site_table_query = 'CREATE TABLE Sites (entryID int AUTO_INCREMENT, ' \
#                              'Site VARCHAR(100) NOT NULL, ' \
#                              'PRIMARY KEY (entryID))'
#
#    create_pass_table_query = 'CREATE TABLE Passwords ' \
#                              '(entryID int AUTO_INCREMENT, ' \
#                              'Passwords BINARY(100) NOT NULL, ' \
#                              'FOREIGN KEY (entryID) REFERENCES Sites(entryID))'
#
#    key_table_query = 'CREATE TABLE Crypt ' \
#                      '(key_id int AUTO_INCREMENT, ' \
#                      'crypt_key BINARY(120) NOT NULL, ' \
#                      'PRIMARY KEY (key_id))'
#
#    create_master_table_query = 'CREATE TABLE Master ' \
#                                '(master_key_id int AUTO_INCREMENT, ' \
#                                'master_key BINARY(100) NOT NULL, ' \
#                                'PRIMARY KEY (master_key_id))'
#
#    my_cursor.execute(key_table_query)
#    my_cursor.execute(create_site_table_query)
#    my_cursor.execute(create_pass_table_query)
#    my_cursor.execute(create_master_table_query)
#    pw_db.commit()
