"""
    Models Order, ShoppingCart as a resource defining
    order endpoints
"""
import psycopg2
from flask import request, abort, make_response, jsonify
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from flask_restful import Resource

# local imports
from api.v2.utils import validate
from api.v2 import database
from api.v2.models import User, FoodItem, Order


class ShoppingCart(Resource):
    """
        Models a users's shopping cart with all user orders
    """
    @jwt_required
    def get(self):
        """
            GET users/orders endpoint
        """
        # extract user id from token
        username = get_jwt_identity()[0]
        query = """
        SELECT * FROM orders WHERE orders.ordered_by = '{}'""".format(username)

        orders = database.select_from_db(query)

        if not orders:
            validate.abort_not_found("orders", "for user '{}' ".format(username))

        formatted_orders = []
        total_expenditure = 0
        for order in orders:
            formatted_order = {
                "order_id": order[0],
                "ordered_by": order[1],
                "order_info": "{} {}s at {} each".format(
                    order[4], order[2], order[3]),
                "total_order_cost": order[5]
            }
            formatted_orders.append(formatted_order)
            total_expenditure += order[5]

        response = make_response(jsonify({
            "message": "Orders found.",
            "orders": formatted_orders,
            "total_expenditure": total_expenditure
        }), 200)

        return response

    @jwt_required
    def post(self):
        """
            POST users/orders
        """
        data = validate.check_request_validity(request)
        # extract user id from token
        username = get_jwt_identity()[0]

        # Check if required params are present
        food_item_params = validate.check_food_item_params_a(data)

        # Check whether food item on menu
        query = """
        SELECT * FROM menu
        WHERE menu.food_item_id = '{}'""".format(
            food_item_params["food_item_id"])

        food_item = database.select_from_db(query)

        if not food_item:
            validate.abort_not_found("food item with id '{}' ".format(
                food_item_params["food_item_id"]), "in menu")

        # If the food_item exists on the menu
        # Add ordered_by
        ordered_by = username
        food_item_name = food_item[0][1]
        food_item_price = food_item[0][2]
        quantity = food_item_params["quantity"]

        new_order = Order(
            ordered_by,
            food_item_name,
            food_item_price,
            quantity)

        new_order.save_order_to_db()
        # query db for saved order on success
        saved_order = new_order.retrieve_order_from_db(
            new_order.food_item_name)

        if not saved_order:
            validate.abort_not_found("Order with name '{}'".format(
                food_item_name), "in orders")
        # on success
        response = make_response(jsonify({
            "message": "Order posted successfully",
            "order": {
                "order_id": saved_order[0][0],
                "ordered_by": saved_order[0][1],
                "order_info": "{} {}s at {} each".format(
                    saved_order[0][4],
                    saved_order[0][2], saved_order[0][3]),
                "total_order_cost": saved_order[0][5]}
            }))

        return response
