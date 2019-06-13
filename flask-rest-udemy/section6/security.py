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
from models.user import UserModel
from werkzeug.security import safe_str_cmp

# users = [
#     User(1, 'gaurav', 'gaurav')
# ]

# username_mapping = {u.username: u for u in users}

# userid_mapping = {u.id: u for u in users}


def authenticate(username, password):
    user = UserModel.get_user_by_username(username)

    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    user_id = payload['identity']
    return UserModel.get_user_by_id(user_id)
