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
        "email": "dmithamo@andela.com",
        "password": "dmit-password"
    }
    user_2 = {
        "username": "myname",
        "email": "myname@andela.com",
        "password": "my-password"
    }

    # Sample data for login in
    user_logins = {
        "email": "dmithamo@andela.com",
        "password": "dmit-password"
    }

    admin_logins = {
        "email": "admintest@admin.com",
        "password": "admin-pass-10s"
    }

    # Sample order data for POST request
    food = {
        "food_item_name": "Guacamole and Marshmallows",
        "food_item_price": 200,
    }
    food_2 = {
        "food_item_name": "Roast Meat",
        "food_item_price": 1000,
    }
    food_fake = {
        "food_item_name": "Njugu Karanga",
        "food_item_price": 50,
    }
    new_food = {
        "food_item_name": "Chicken Curry",
        "food_item_price": 500
    }

    return {
        "user": user,
        "user_2": user_2,
        "user_logins": user_logins,
        "admin_logins": admin_logins,
        "food": food,
        "food_2": food_2,
        "food_fake": food_fake,
        "new_food": new_food
    }

def response_as_json(resp):
    """
        Helper function
        Loads response as json for easier inspection
    """
    resp_json = json.loads(resp.data.decode('utf-8'))
    return resp_json
