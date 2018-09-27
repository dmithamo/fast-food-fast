"""
    Models User, FoodItem, Order as objects
"""


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

    def save_new_user_to_db(self):
        """
            Saves newly created user to db
        """
        query = """
        INSERT INTO users(username, email, password) VALUES(
            '{}', '{}', '{}'
        )""".format(self.username, self.email, self.password)

        database.insert_into_db(query)
