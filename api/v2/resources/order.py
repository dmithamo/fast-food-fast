"""
    Models Order, ShoppingCart as a resource defining
    order endpoints
"""
import psycopg2
from flask import request, abort, make_response, jsonify
from flask_jwt_extended import (jwt_required, get_jwt_identity, get_raw_jwt)
from flask_restful import Resource

# local imports
from api.v2.utils import validate
from api.v2 import database
from api.v2.models import User, Order


class ShoppingCart(Resource):
    """
        Models a users's shopping cart with all user orders
    """
    @jwt_required
    def get(self):
        """
            GET users/orders endpoint
        """
        query = """
        SELECT * FROM orders;"""

        orders = database.select_from_db(query)

        if not orders:
            validate.abort_not_found("orders", "for user")

        response = make_response(jsonify({
            "message": "Orders found.",
            "food": str(orders)
        }), 200)

        return response

    @jwt_required
    def post(self):
        """
            POST users/orders
        """
        data = validate.check_request_validity(request)
        # Check token validity
        # token = request.header.get
        try:
            # Check if required params are present
            food_item = validate.check_food_item_params(data)

            # # Check whether food item on menu
            # query = """
            # SELECT food_item_name FROM menu
            # WHERE menu.food_item_name = '{}'""".format(data["food_item_name"])

            # food_item = database.select_from_db(query)
            # if not food_item:
            #     # Abort not found
            #     validate.abort_not_found(data["food_item_name"], "in menu")

            # Add quantity and ordered_by
            food_item['quantity'] = 5
            food_item['ordered_by'] = ""

            name = food_item["food_item_name"]
            price = food_item["food_item_price"]
            price = food_item["food_item_price"]
            quantity = food_item["quantity"]
            ordered_by = food_item["ordered_by"]

            new_order = Order(name, price, quantity, ordered_by)

            saved_order = new_order.save_order_to_db()

            if saved_order:
                response = make_response(jsonify({
                    "message": "Order posted successfully",
                    "order": str(new_order)
                }))
            else:
                abort(make_response(jsonify(
                    message="DB error : {}"), 500))

        except (psycopg2.DatabaseError) as error:
            abort(make_response(jsonify(
                message="Server hererrrr error : {}".format(error)
            ), 500))

        return response
