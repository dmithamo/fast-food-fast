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

    @jwt_required
    def put(self, food_item_id):
        """
            PUT /menu<int:food_item_id> endpoint
            Accessible by admin only
        """
        data = validate.check_request_validity(request)
        # Check if user is admin
        validate.abort_if_user_role_not_appropriate("admin")

        query_search_for_item = """
        SELECT * FROM menu
        WHERE menu.food_item_id = '{}'""".format(food_item_id)

        food_item = database.select_from_db(query_search_for_item)

        if not food_item:
            # If no item in db with matching id
            validate.abort_not_found(
                "food_item with id {}".format(food_item_id), "menu")

        # Check if the item being updated is valid
        # Aborts for invalid param
        validate.check_if_param_updatable(data)

        # Detect if request represents a change
        validate.check_if_any_change(data, food_item)

        # If param being updated is food_item_name, check that the change
        # wont be a duplication of an existing name
        if "food_item_name" in data.keys():
            validate.check_duplication_b(data["food_item_name"], food_item_id)

        # Update if all checks pass
        for key, value in data.items():
            query_update = """
            UPDATE menu
            SET {} = '{}'
            WHERE menu.food_item_id = '{}'""".format(key, value, food_item_id)
            database.query_db_no_return(query_update)

        update_food_item = database.select_from_db(query_search_for_item)[0]

        response = make_response(jsonify({
            "message": "Food item modified succesfully.",
            "food": {
                "food_item_id": update_food_item[0],
                "food_item_name": update_food_item[1],
                "food_item_price": update_food_item[2]
            }
        }), 201)

        return response

    @jwt_required
    def delete(self, food_item_id):
        """
            DELETE /menu/<int:food_item_id> endpoint
            Accessible by admin only
        """
        # Check if user is admin
        validate.abort_if_user_role_not_appropriate("admin")

        query_search_for_item = """
        SELECT * FROM menu
        WHERE menu.food_item_id = '{}'""".format(food_item_id)

        food_item = database.select_from_db(query_search_for_item)

        if not food_item:
            # If no item in db with matching id
            validate.abort_not_found(
                "food_item with id {}".format(food_item_id), "menu")

        delete_query = """
        DELETE FROM menu
        WHERE menu.food_item_id = '{}'""".format(food_item_id)

        database.query_db_no_return(delete_query)

        # Confirm deletion by querying db for same item
        food_item = database.select_from_db(query_search_for_item)
        if food_item:
            # Means the deletion did not happen
            abort(make_response(jsonify(
                message="Error. Not deleted for some reason"
            ), 500))

        response = make_response(jsonify(
            message="Delete successful."), 200)

        return response

    def get(self):
        """
            Retrieve the menu
        """
        query = """
        SELECT * FROM menu ORDER BY menu.food_item_id"""
        menu = database.select_from_db(query)

        if not menu:
            # If menu is empty
            abort(make_response(jsonify(
                message="No food items on the menu yet",
            ), 200))

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
