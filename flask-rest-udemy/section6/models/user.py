import sqlite3
from db import db


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def get_user_by_username(cls, username):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        select_query = 'SELECT * FROM users WHERE username=?'
        result = cursor.execute(select_query, (username,))
        row = result.fetchone()

        if row:
            # return User(row[0], row[1], row[2])
            user =  cls(*row)
        else:
            user=None
        conn.close()
        return user

    @classmethod
    def get_user_by_id(cls, _id):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        select_query = 'SELECT * FROM users WHERE id=?'
        result = cursor.execute(select_query, (_id,))
        row = result.fetchone()

        if row:
            # return User(row[0], row[1], row[2])
            user = cls(*row)
        else:
            user = None
        conn.close()
        return user