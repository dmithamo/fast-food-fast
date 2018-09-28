"""
    Models User, FoodItem, Order as objects
"""
import os
import jwt

from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
# local imports
from api.v2 import database


class User:
    """
        Model of User
        Defines User params and methods callable on User
    """
    def __init__(self, username, email, password):
        """
            Initialize a user object
        """
        self.username = username
        self.email = email
        self.password = password
        self.encrypt_password_on_signup()

    def save_new_user_to_db(self):
        """
            Saves newly created user to db
        """
        query = """
        INSERT INTO users(username, email, password) VALUES(
            '{}', '{}', '{}'
        )""".format(self.username, self.email, self.password_hash)

        database.insert_into_db(query)

    @staticmethod
    def retrieve_user_from_db(email):
        """
            Queries db for user with given username
            Returns user object
        """
        # Query db for user with those params
        query = """
        SELECT user_id, username, email, password FROM users
        WHERE users.email = '{}'""".format(email)

        return database.select_from_db(query)

    @staticmethod
    def generate_auth_token(user_id):
        """
            Generate authentication token on signup/login
        """
        payload = {"user": user_id}

        token = jwt.encode(payload, os.getenv('SECRET_KEY'), algorithm='HS256')
        return token

    @staticmethod
    def decode_auth_token(token):
        """
            Decrypts token
        """
        resp = ''
        try:
            decoded_token = jwt.decode(token, os.getenv('SECRET_KEY'))["user"]
            resp = decoded_token
        except (Exception, jwt.InvalidTokenError) as error:
            resp = None

        return resp


    def encrypt_password_on_signup(self):
        """
            Encrypt password before saving to db
        """
        self.password_hash = generate_password_hash(self.password)

    @staticmethod
    def check_password_at_login(password_hash, password):
        """
            Encrypt password before saving to db
        """
        return check_password_hash(password_hash, password)
