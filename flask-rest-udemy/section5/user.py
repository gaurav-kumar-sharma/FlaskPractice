import sqlite3
from flask_restful import Resource, reqparse


class User:
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

        if User.get_user_by_username(data['username']):
            return {"message": "User already exists!!"}, 400

        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        query = "INSERT INTO users values(NULL , ?, ?)"
        cursor.execute(query, (data['username'], data['password']))

        connection.commit()
        connection.close()

        return {'message': "User register successfully!!"}, 201

