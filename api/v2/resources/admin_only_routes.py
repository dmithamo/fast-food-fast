"""
    Module defines admin specific endpoints
"""
import os
import datetime

from flask_jwt_extended import (create_access_token, jwt_required, get_jwt_identity)
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
        # extract user id from token
        user_role = get_jwt_identity()[1]
        if not user_role == "admin":
            abort(make_response(jsonify(
                message="Forbidden. You are not an admin"), 403))

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
