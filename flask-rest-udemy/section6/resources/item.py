import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


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
            item = ItemModel.get_item_by_name(name)
            if item:
                return {'item': item.json()}
            return {'message': 'Item not found'}
        except:
            return {"message": "Something went wrong. Please try again later."}, 500

    def post(self, name):

        item = ItemModel.get_item_by_name(name)
        if item:
            return {'message': 'Item with name {} already exists'.format(name)}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'])
        try:
            item.insert_item()
            return item.json(), 201
        except:
            return {"message": "Something went wrong. Please try again later."}, 500

    def delete(self, name):
        try:
            ItemModel.delete_item(name)
            return {"message": "Item deleted"}
        except:
            return {"message": "Something went wrong. Please try again later."}, 500

    def put(self, name):

        try:
            item = ItemModel.get_item_by_name(name)
            data = Item.parser.parse_args()
            if item:
                item.price = data['price']
                item.update_item()
            else:
                item = ItemModel(name, data['price'])
                item.insert_item()
            return item.json(), 201
        except:
            return {"message": "Something went wrong. Please try again later."}, 500


class ItemsList(Resource):
    def get(self):
        try:
            return {'items': ItemModel.get_items()}
        except:
            return {"message": "Something went wrong. Please try again later."}, 500



