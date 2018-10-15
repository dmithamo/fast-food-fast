"""
    Module defines admin specific endpoints
"""
import datetime

from flask_jwt_extended import create_access_token, jwt_required
from flask import request, jsonify, make_response, abort
from flask_restful import Resource


# local imports
from api.v2.resources.orders import configure_response
from api.v2.utils import validate
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
            "admin": {
                "logged_in_at": datetime.datetime.utcnow().strftime(
                    "%Y-%m-%d %H:%M:%S"),
                "token": create_access_token(
                    identity=(data["email"], "admin"),
                    expires_delta=datetime.timedelta(days=5))
            }
        }), 200)
        return response


class AllOrders(Resource):
    """
        Defines routes to all orders in DB
    """
    @jwt_required
    def get(self):
        """
            GET /orders endpoint
        """
        validate.abort_if_user_role_not_appropriate("admin")

        # if user_role confirmed ok

        query = """
        SELECT * FROM orders ORDER BY orders.order_id"""

        orders = database.select_from_db(query)

        if not orders:
            abort(make_response(jsonify(
                message="No orders yet."), 200))

        formatted_orders = []
        for order in orders:
            formatted_order = configure_response(order)
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
        validate.abort_if_user_role_not_appropriate("admin")

        # if user_role confirmed ok
        query = """
        SELECT * FROM orders
        WHERE orders.order_id = '{}'""".format(order_id)

        order = database.select_from_db(query)
        # Abort if not order
        if not order:
            validate.abort_order_not_found(order_id)

        formatted_order = configure_response(order[0])
        response = make_response(jsonify({
            "message": "Order found.",
            "order": formatted_order
        }), 200)

        return response

    @jwt_required
    def put(self, order_id):
        """
            PUT /orders/order_id endpoint
        """
        validate.abort_if_user_role_not_appropriate("admin")
        data = validate.check_request_validity(request)

        # if user_role confirmed ok, and order_status is ok
        query = """
        SELECT * FROM orders
        WHERE orders.order_id = '{}'""".format(order_id)

        order = database.select_from_db(query)

        if not order:
            validate.abort_order_not_found(order_id)

        if order[0][3] in ["Complete", "Cancelled", "Deleted"]:
            # if order was already marked Complete, Cancelled or Deleted
            abort(make_response(
                jsonify(message="Not allowed. This order is already '{}'".format(order[0][3])), 401))

        # Check that supplied status is valid
        order_status = validate.check_order_status_validity(data)

        timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

        update_query = """
        UPDATE orders
        SET order_status = '{}',
            status_update_on = '{}' WHERE
        orders.order_id = '{}'""".format(order_status, timestamp, order_id)

        database.query_db_no_return(update_query)

        updated_order = database.select_from_db(query)

        formatted_updated_order = configure_response(updated_order[0])

        response = make_response(jsonify({
            "message": "Order found.",
            "order": formatted_updated_order
        }), 200)

        return response

    @jwt_required
    def delete(self, order_id):
        """
            DELETE /orders/order_id and
            : can only delete where status is 'Cancelled'
        """
        validate.abort_if_user_role_not_appropriate("admin")

        # if user_role and order data confirmed ok
        # see if order exists
        search_query = """
        SELECT * FROM orders
        WHERE orders.order_id = '{}'""".format(order_id)

        order = database.select_from_db(search_query)
        if not order:
            validate.abort_order_not_found(order_id)

        # if order_status not 'Cancelled'
        if order[0][3] != "Cancelled":
            abort(make_response(jsonify(
                message="Not deleted. Status is '{}'. \
Status must be 'Cancelled' to delete".format(order[0][3])
            ), 401))

        # if order_status already 'Deleted'
        if order[0][3] == "Deleted":
            abort(make_response(jsonify(
                message="Error. This was already deleted."
            ), 400))

        # Do a 'soft-delete',,,i.e, only change the status, 
        # don't remove order from DB
        timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        delete_single_order = """
        UPDATE orders
        SET order_status = 'Deleted',
            status_update_on = '{}'
        WHERE orders.order_id = '{}'
        """.format(timestamp, order_id)

        database.query_db_no_return(delete_single_order)

        response = make_response(jsonify(
            message="Delete successful."), 200)

        return response
