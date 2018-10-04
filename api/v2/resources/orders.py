"""
    Models Order, ShoppingCart as a resource defining
    order endpoints
"""
from flask import request, make_response, jsonify
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from flask_restful import Resource

# local imports
from api.v2.utils import validate
from api.v2 import database
from api.v2.models import Order


# Helper functions
def configure_response(order):
    """
        Configure appropriate
    """
    formatted_order = {
        "order_id": order[0],
        "ordered_by": order[1],
        "ordered_on": order[2],
        "order_status": order[3],
        "order_info": "{} {}s at {} each".format(
            order[6], order[4], order[5]),
        "total_order_cost": order[7]
    }
    return formatted_order


class ShoppingCart(Resource):
    """
        Models a users's shopping cart with all user orders
    """
    @jwt_required
    def get(self):
        """
            GET users/orders endpoint
        """
        # Abort if role not 'user'
        validate.abort_if_user_role_not_appropriate("user")
        # extract user id from token
        username = get_jwt_identity()[0]
        query = """
        SELECT * FROM orders
        WHERE orders.ordered_by = '{}'""".format(username)

        orders = database.select_from_db(query)

        if not orders:
            validate.abort_not_found(
                "orders", "for user '{}' ".format(username))

        formatted_orders = []
        total_expenditure = 0
        for order in orders:
            formatted_order = configure_response(order)
            formatted_orders.append(formatted_order)
            total_expenditure += order[7]

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
        # Abort if role not 'user'
        validate.abort_if_user_role_not_appropriate("user")
        # extract user id from token
        username = get_jwt_identity()[0]

        # Check if required params are present
        food_item_params = validate.check_food_item_params_a(data)

        # Check that user is 'user' (not admin)
        validate.abort_if_user_role_not_appropriate("user")

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
        # Check if a similar unfulfilled order exists
        search_query = """
        SELECT * FROM orders WHERE
        orders.ordered_by = '{}' AND
        orders.food_item_name = '{}' AND orders.order_status IN ('New', 'Processing')
        """.format(username, food_item[0][1])

        order_exists = database.select_from_db(search_query)
        print("\n\n\n{}\n\n\n".format(order_exists))
        if order_exists:
            formated_ord = configure_response(order_exists[0])
            # if a similar order has been placed which has not been serviced
            validate.abort_similar_order_exists(formated_ord)

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
            new_order.food_item_name, new_order.ordered_by)

        if not saved_order:
            validate.abort_not_found("Order with name '{}'".format(
                food_item_name), "in orders")
        # on success
        response = make_response(jsonify({
            "message": "Order posted successfully",
            "order": configure_response(saved_order[0])
            }), 201)

        return response
