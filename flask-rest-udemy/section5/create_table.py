import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

create_table_users = "CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username text, password text )"

cursor.execute(create_table_users)

create_table_item = "CREATE TABLE IF NOT EXISTS item(name text, price real)"

cursor.execute(create_table_item)

connection.commit()
connection.close()
