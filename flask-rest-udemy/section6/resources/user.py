import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="User name required"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="Password required"
                        )

    def post(self):

        data = UserRegister.parser.parse_args()

        if UserModel.get_user_by_username(data['username']):
            return {"message": "User already exists!!"}, 400

        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        query = "INSERT INTO users values(NULL , ?, ?)"
        cursor.execute(query, (data['username'], data['password']))

        connection.commit()
        connection.close()

        return {'message': "User register successfully!!"}, 201

