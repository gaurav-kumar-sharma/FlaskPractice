import sqlite3

conn = sqlite3.connect('database.db')

cursor = conn.cursor()

create_table = "CREATE TABLE users(id int, username text, password text)"

cursor.execute(create_table)

user = (1, 'gaurav', 'Pgaurav')

insert_query = "INSERT INTO users VALUES(?, ?, ?)"

cursor.execute(insert_query, user)

users = [
    (2, 'gaurav2', 'Pgaurav2'),
    (3, 'gaurav3', 'Pgaura3')
]

cursor.executemany(insert_query, users)
conn.commit()

select_query = "SELECT * FROM  users"

for row in cursor.execute(select_query):
    print(row)

conn.close()
