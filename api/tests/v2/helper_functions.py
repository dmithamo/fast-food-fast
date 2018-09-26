"""
    Module contains helper fucntions common accross all
    the three test modules.
    Objective : To minimise repetition
"""
import json


def sample_params():
    """
        Helper method.
        Sets up sample params
    """

    # Sample data for registration
    user = {
        "username": "dmithamo",
        "user_email": "dmithamo@andela.com",
        "password": "dmit-password"
    }

    # Sample data for login in
    user_logins = {
        "user_email": "dmithamo@andela.com",
        "password": "dmit-password"
    }

    # Sample order data for POST request
    food = {
        "food_item_name": "Guacamole and Marshmallows",
        "food_item_price": 200,
        "quantity": 2
    }
    food_2 = {
        "food_item_name": "Roast Meat",
        "food_item_price": 1000,
        "quantity": 2,
    }
    food_fake = {
        "food_item_name": "Njugu Karanga",
        "food_item_price": 50,
        "quantity": 1,
    }

    return {
        "user": user,
        "user_logins": user_logins,
        "food": food,
        "food_2": food_2,
        "food_fake": food_fake
    }

def response_as_json(resp):
    """
        Helper function
        Loads response as json for easier inspection
    """
    resp_json = json.loads(resp.data.decode('utf-8'))
    return resp_json
