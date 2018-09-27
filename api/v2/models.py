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
            Initialize user
        """
        self.username = username
        self.email = email
        self.password = password

    @classmethod
    def query_db_by_username(cls, username):
        """
            Searches db for username, returns user if found
        """
        query = """
        SELECT * FROM users;
        """
        users = {}
        rows = database.select_from_db(query)
        if rows:
            for row in rows:
                users["username"] = row
                users["user_email"] = row[1]
                users["user_password"] = row[2]
        return users
