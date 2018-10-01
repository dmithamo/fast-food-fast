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

        # Check if user is admin
        validate.abort_if_user_role_not_appropriate("admin")
        # Save valid food to db
        new_food = FoodItem(
            food_item["food_item_name"], food_item["food_item_price"])
        new_food.save_food_item_to_menu()

        # Confirm save by querrying db for saved food item
        saved_food = new_food.retrieve_food_item_from_db(
            food_item["food_item_name"])
        if not saved_food:
            abort(make_response(jsonify(
                message="Server / DB error ..."
            ), 500))

        response = make_response(jsonify({
            "message": "Food item added succesfully.",
            "food": {
                "food_item_id": saved_food[0][0],
                "food_item_name": saved_food[0][1],
                "food_item_price": saved_food[0][2]
            }
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
                message="No food items found on the menu",
            ), 404))

        formatted_menu = []
        for item in menu:
            formatted_item = {
                "food_item_id": item[0],
                "food_item_name": item[1],
                "food_item_price": item[2]
            }

            formatted_menu.append(formatted_item)

        response = make_response(jsonify({
            "message": "Request successful",
            "menu": formatted_menu
        }), 200)

        return response
