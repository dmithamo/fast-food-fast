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
        # extract user id from token
        user = get_jwt_identity()
        query = """
        SELECT * FROM orders WHERE orders.ordered_by = '{}'""".format(user)


        orders = database.select_from_db(query)

        if not orders:
            validate.abort_not_found("orders", "for user '{}' ".format(user))

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
        try:
            # extract user id from token
            user = get_jwt_identity()
            # Check if required params are present
            food_item = validate.check_food_item_params(data)

            # Check whether food item on menu
            # query = """
            # SELECT food_item_name FROM menu
            # WHERE menu.food_item_name = '{}'""".format(
            #     food_item["food_item_name"])

            # food_item = database.select_from_db(query)
            # if not food_item:
            #     # Abort not found
            #     validate.abort_not_found(food_item["food_item_name"], "in menu")

            # Add ordered_by
            food_item["ordered_by"] = user

            ordered_by = food_item["ordered_by"]
            food_item_name = food_item["food_item_name"]
            food_item_price = food_item["food_item_price"]
            quantity = food_item["quantity"]

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

        except (Exception, psycopg2.Error) as error:
            abort(make_response(jsonify(
                message="Server error : {}".format(error)
            ), 500))

        return response
