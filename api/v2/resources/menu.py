"""
    Module models menu and defines routes to access menu
"""
import psycopg2
from flask_jwt_extended import (jwt_required, get_jwt_identity, get_raw_jwt)
from flask import request, abort, make_response, jsonify
from flask_restful import Resource

# local imports
from api.v2.utils import validate
from api.v2 import database
from api.v2.models import FoodItem


class Menu(Resource):
    """
        Define routes to menu
    """
    @jwt_required
    def post(self):
        """
            POST /menu endpoint
            Accessible by admin only
        """
        data = validate.check_request_validity(request)
        food_item = validate.check_food_item_params(data)
        # Save valid food to db
        new_food = FoodItem(food_item["food_item_name"], food_item["food_item_price"])
        new_food.save_food_item_to_menu()

        # Confirm save by querrying db for saved food item
        saved_food = new_food.retrieve_food_item_from_db(food_item["food_item_name"])

        response = make_response(jsonify({
            "message": "Food item added succesfully.",
            "food": str(saved_food)
        }), 201)

        return response

    def get(self):
        """
            Retrieve the menu
        """
        query = """
        SELECT * FROM menu"""
        menu = database.select_from_db(query)

        if not menu:
            # If menu is empty
            abort(make_response(jsonify(
                message="{} no food items found on the menu".format(menu),
            ), 404))

        response = make_response(jsonify({
            "message": "Request successful",
            "menu": str(menu)
        }), 200)

        return response
