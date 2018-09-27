"""
    Models User, FoodItem, Order as objects
    Models Users, Menu, ShoppingCart as containers for 
    each of the above, respectively
"""


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
