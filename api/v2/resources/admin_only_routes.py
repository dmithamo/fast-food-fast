"""
    Module defines admin specific endpoints
"""
import os
import datetime

from flask_jwt_extended import (create_access_token,
                                jwt_required)
from flask import request, jsonify, make_response, abort
from flask_restful import Resource


# local imports
from api.v2.utils import validate
from api.v2.models import User
from api.v2 import database


class AdminLogin(Resource):
    """
        Define admin specific methods
    """
    def post(self):
        """
            POST /login
        """
        data = validate.check_request_validity(request)
        # Check admin logins
        validate.check_admin_logins(data)

        # for valid admin logins
        response = make_response(jsonify({
            "message": "Admin logged in",
            "logged_in_admin": {
                "email": data["email"],
                "token": create_access_token(identity=(data["email"], "admin"))
            }
        }))
        return response


class AllOrders(Resource):
    """
        Defines routes to all orders in DB
    """
    @jwt_required
    def get(self):
        """
            GET users/orders endpoint
        """
        validate.abort_if_user_role_not_admin()

        # if user_role confirmed ok

        query = """
        SELECT * FROM orders"""

        orders = database.select_from_db(query)

        if not orders:
            abort(make_response(jsonify(
                message="No orders found."), 404))

        formatted_orders = []
        for order in orders:
            formatted_order = {
                "order_id": order[0],
                "ordered_by": order[1],
                "order_info": "{} {}s at {} each".format(
                    order[4], order[2], order[3]),
                "total_order_cost": order[5]
            }
            formatted_orders.append(formatted_order)

        response = make_response(jsonify({
            "message": "Orders found.",
            "orders": formatted_orders
        }), 200)

        return response

class Order(Resource):
    """
        Define routes targetted at a unique order in the DB
        Requires order_id
    """
    @jwt_required
    def get(self, order_id):
        """
            GET /orders/order_id endpoint
        """
        validate.abort_if_user_role_not_admin()

        # if user_role confirmed ok
        query = """
        SELECT * FROM orders 
        WHERE orders.order_id = '{}'""".format(order_id)

        order = database.select_from_db(query)

        if not order:
            abort(make_response(jsonify(
                message="Order with id '{}' not found.".format(order_id)), 404))

        formatted_order = {
            "order_id": order[0][0],
            "ordered_by": order[0][1],
            "order_info": "{} {}s at {} each".format(
                order[0][4], order[0][2], order[0][3]),
            "total_order_cost": order[0][5]
        }

        response = make_response(jsonify({
            "message": "Order found.",
            "order": formatted_order
        }), 200)

        return response
