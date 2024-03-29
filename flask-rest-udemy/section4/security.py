# users = [
#     {
#         'id': 1,
#         'username': 'gaurav',
#         'password': 'gaurav',
#     }
# ]
#
# username_mapping = { 'gaurav': {
#         'id': 1,
#         'username': 'gaurav',
#         'password': 'gaurav',
#     }
#
# }
#
# userid_mapping = {1: {
#         'id': 1,
#         'username': 'gaurav',
#         'password': 'gaurav',
#     }
#
# }
from user import User
from werkzeug.security import safe_str_cmp

users = [
    User(1, 'gaurav', 'gaurav')
]

username_mapping = {u.username: u for u in users}

userid_mapping = {u.id: u for u in users}


def authenticate(username, password):
    user = username_mapping.get(username, None)

    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)
