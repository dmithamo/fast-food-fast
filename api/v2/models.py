"""
    Models User, FoodItem, Order as objects
"""
import os

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
        self.password = self.encrypt_password_on_signup(password)

    def save_new_user_to_db(self):
        """
            Saves newly created user to db
        """
        query = """
        INSERT INTO users(username, email, password) VALUES(
            '{}', '{}', '{}'
        )""".format(self.username, self.email, self.password)

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

    def encrypt_password_on_signup(self, password):
        """
            Encrypt password before saving to db
        """
        password_hash = generate_password_hash(str(password))
        return password_hash

    @staticmethod
    def check_password_at_login(password_hash, password):
        """
            Encrypt password before saving to db
        """
        return check_password_hash(password_hash, str(password))


class Order:
    """
        Model an order
    """
    def __init__(self, food_item_name, food_item_price, quantity, ordered_by):
        """"
            Initilize an order, given params
        """
        self.food_item_name = food_item_name
        self.food_item_price = food_item_price
        self.quantity = quantity
        self.ordered_by = ordered_by
        self.timestamp = datetime.now()

    def save_order_to_db(self):
        """
            Add order with valid params to db
        """
        query = """
        INSERT INTO orders(food_item_name, food_item_price, quantity) VALUES(
            '{}', '{}', '{}', '{}'
        )""".format(self.food_item_name,
                    self.food_item_price, self.quantity, self.timestamp)

        database.insert_into_db(query)

        order = None
        query_to_check = """
        SELECT * FROM orders WHERE orders.food_item_name = '{}'""".format(self.food_item_name)

        order = database.select_from_db(query_to_check)

        return order
        
