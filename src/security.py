from werkzeug.security import safe_str_cmp  # safe str compare (for python 2.7, different encodings, etc)

from src.models.user import UserModel


def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):  # using safe method to compare strings
        return user


def identity(payload):  # payload is a content of JWT
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)