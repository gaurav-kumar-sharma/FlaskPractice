from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'secret-key'

api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth

items = []


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This is mandatory float field!!"
                        )

    @jwt_required()
    def get(self, name):
        # for item in items:
        #     if item['name'] == name:
        #         return item

        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item else 404

    def post(self, name):
        # parser = reqparse.RequestParser()
        # parser.add_argument('price',
        #                     type=float,
        #                     required=True,
        #                     help="This is mandatory float field!!"
        #                     )
        if next(filter(lambda x: x['name'] == name, items), None) is not None:
            return {'message': 'Item with name {} already exists'.format(name)}, 400
        # data = request.get_json()
        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {"message": "Item deleted"}

    def put(self, name):
        # parser = reqparse.RequestParser()
        # parser.add_argument('price',
        #                     type=float,
        #                     required=True,
        #                     help="This is mandatory float field!!"
        #                     )
        data = Item.parser.parse_args()
        # data = request.get_json()
        item = next(filter(lambda x: x['name'] == name, items), None)

        if item is not None:
            # item['price'] = data['price']
            item.update(data)

        else:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        return item


class ItemsList(Resource):
    def get(self):
        return {'items': items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemsList, '/items')

app.run(debug=True)
