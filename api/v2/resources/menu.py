"""
    Module models menu and defines routes to access menu
"""
import psycopg2
from flask import request, abort, make_response, jsonify
from flask_restful import Resource

# local imports
from api.v2.utils import validate
from api.v2 import database


class Menu(Resource):
    """
        Define routes to menu
    """
    def save_to_db(self, food_item):
        """
            Saves valid food item to db
        """
        try:
            query = """
            INSERT INTO menu (food_item_name, food_item_price) VALUES (
                '{}', '{}'
            )""".format(food_item["food_item_name"],
                        food_item["food_item_price"])
            database.insert_into_db(query)

            # Check is save was successful
            query_2 = """
            SELECT food_item_id, food_item_name, food_item_price FROM menu
            WHERE food_item_name = '{}'""".format(food_item["food_item_name"])

            new_food = database.select_from_db(query_2)

        except psycopg2.DatabaseError as error:
            abort(make_response(jsonify(
                message="Server error : {}".format(error)
            ), 500))

        return new_food

    def post(self):
        """
            POST /menu endpoint
            Accessible by admin only
        """
        try:
            request.headers['Authorization']
        except KeyError:
            validate.abort_access_unauthorized()

        data = validate.check_request_validity(request)
        food_item = validate.check_food_item_params(data)
        # Save valid food to db
        new_food = self.save_to_db(food_item)

        response = make_response(jsonify({
            "message": "Food added succesfully.",
            "food": new_food
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
                message="{}Not food items found on the menu".format(menu),
            ), 404))

        response = make_response(jsonify({
            "message": "Request successful",
            "menu": str(menu)
        }), 200)

        return response
