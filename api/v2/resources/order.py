"""
    Models Order, ShoppingCart as a resource defining 
    order endpoints
"""
import psycopg2
from flask import request, abort, make_response, jsonify
from flask_restful import Resource

# local imports
from api.v2.utils import validate
from api.v2 import database
from api.v2.models import User, Order


class ShoppingCart(Resource):
    """
        Models a users's shopping cart with all user orders
    """
    def get(self):
        """
            GET users/orders endpoint
        """
        token = validate.check_token_present(request)

        # Check token validity bu searching for matching user
        decoded_token = User.decode_auth_token(token)
        if not decoded_token:
            # invalid token
            validate.abort_access_unauthorized()
        query = """
        SELECT * FROM orders WHERE orders.ordered_by = '{}'""".format(
            decoded_token
        )

        orders = database.select_from_db(query)

        if not orders:
            validate.abort_not_found("user", "orders")

        response = make_response(jsonify({
            "message": "Orders found.",
            "food": orders
        }), 200)

        return response

    def post(self):
        """
            POST users/orders
        """
        data = validate.check_request_validity(request)
        token = validate.check_token_present(request)

        # Check decoded token validity
        decoded_token = User.decode_auth_token(token)
        if not decoded_token:
            # invalid token
            validate.abort_access_unauthorized()

        try:
            # Check if required params are present
            food_item = validate.check_food_item_params(data)

            # Check whether food item on menu
            query = """
            SELECT food_item_name FROM menu
            WHERE menu.food_item_name = '{}'""".format(data["food_item_name"])

            food_item = database.select_from_db(query)
            if not food_item:
                # Abort not found
                validate.abort_not_found(data["food_item_name"], "menu")

        except (Exception, psycopg2.DatabaseError) as error:
            abort(make_response(jsonify(
                message="Server error : {}".format(error)
            ), 500))

            # Add quantity and ordered_by
            food_item['quantity'] = data['quantity']
            food_item['ordered_by'] = decoded_token

            name = food_item["food_item_name"]
            price = food_item["food_item_price"]
            price = food_item["food_item_price"]
            quantity = food_item["quantity"]
            ordered_by = food_item["ordered_by"]

            new_order = Order(name, price, quantity, ordered_by)
            new_order.save_order_to_db()

        return None
                