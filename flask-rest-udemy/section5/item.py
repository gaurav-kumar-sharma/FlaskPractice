import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This is mandatory float field!!"
                        )

    @jwt_required()
    def get(self, name):
        try:
            item = self.get_item_by_name(name)
            if item:
                return {'item': item}
            return {'message': 'Item not found'}
        except:
            return {"message": "Something went wrong. Please try again later."}, 500


    @classmethod
    def get_item_by_name(cls, name):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        query = "SELECT * FROM item WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()
        if row:
            return {'name': row[0], 'price': row[1]}
        return None

    @classmethod
    def insert_item(cls, item):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        query = "INSERT INTO item VALUES(?, ?)"
        cursor.execute(query, (item['name'], item['price']))
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

    @classmethod
    def update_item(cls, item):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        query = "UPDATE item SET price=? WHERE name=?"
        cursor.execute(query, (item['price'], item['name']))
        connection.commit()
        connection.close()

    def post(self, name):

        item = self.get_item_by_name(name)
        if item:
            return {'message': 'Item with name {} already exists'.format(name)}, 400

        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}
        try:
            self.insert_item(item)
            return item, 201
        except:
            return {"message": "Something went wrong. Please try again later."}, 500

    def delete(self, name):
        try:
            self.delete_item(name)
            return {"message": "Item deleted"}
        except:
            return {"message": "Something went wrong. Please try again later."}, 500

    def put(self, name):

        try:
            item = self.get_item_by_name(name)
            data = Item.parser.parse_args()
            if item:
                item['price'] = data['price']
                self.update_item(item)
            else:
                item = {'name': name, 'price': data['price']}
                self.insert_item(item)
            return item, 201
        except:
            return {"message": "Something went wrong. Please try again later."}, 500


class ItemsList(Resource):
    def get(self):
        try:
            return {'items': self.get_items()}
        except:
            return {"message": "Something went wrong. Please try again later."}, 500


    @classmethod
    def get_items(cls):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        query = "SELECT * FROM item"
        result = cursor.execute(query)
        rows = result.fetchall()
        connection.close()

        if rows:
            items = [{'name': i[0], 'price': i[1]} for i in rows]
            return items
        return None

