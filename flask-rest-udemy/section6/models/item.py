import sqlite3
from db import db


class ItemModel(db.Model):
    __table__ = "item"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))
    
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def get_item_by_name(cls, name):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        query = "SELECT * FROM item WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()
        if row:
            return cls(*row)
        return None

    def insert_item(self):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        query = "INSERT INTO item VALUES(?, ?)"
        cursor.execute(query, (self.name, self.price))
        connection.commit()
        connection.close()

    @classmethod
    def delete_item(cls, name):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        query = "DELETE FROM item WHERE name=?"
        cursor.execute(query, (name,))
        connection.commit()
        connection.close()

    def update_item(self):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        query = "UPDATE item SET price=? WHERE name=?"
        cursor.execute(query, (self.price, self.name))
        connection.commit()
        connection.close()

    @classmethod
    def get_items(cls):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        query = "SELECT * FROM item"
        result = cursor.execute(query)
        rows = result.fetchall()
        connection.close()

        if rows:
            items = [cls(*i).json() for i in rows]
            return items
        return None
