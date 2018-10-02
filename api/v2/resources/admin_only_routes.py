"""
    Module defines admin specific endpoints
"""
from datetime import datetime

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
            "logged_in_admin": {
                "logged_in_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
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
        validate.abort_if_user_role_not_appropriate("admin")

        # if user_role confirmed ok

        query = """
        SELECT * FROM orders"""

        orders = database.select_from_db(query)

        if not orders:
            abort(make_response(jsonify(
                message="No orders found."), 404))

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
        validate.abort_order_not_found(order_id)

        formatted_order = configure_response(order)
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

        # Check that supplied status is valid
        order_status = validate.check_order_status_validity(data)

        # if user_role confirmed ok, and order_status is ok
        query = """
        SELECT * FROM orders
        WHERE orders.order_id = '{}'""".format(order_id)

        order = database.select_from_db(query)

        if not order:
            validate.abort_order_not_found(order_id)

        update_query = """
        UPDATE orders
        SET order_status = '{}' WHERE
        orders.order_id = '{}'""".format(order_status, order_id)

        database.query_db_no_return(update_query)

        updated_order = database.select_from_db(query)

        formatted_updated_order = configure_response(updated_order[0])

        response = make_response(jsonify({
            "message": "Order found.",
            "order": formatted_updated_order
        }), 200)

        return response

    @jwt_required
    def delete(self, order_id=None):
        """
            DELETE /orders/order_id and
            DELETE /orders endpoint
            : can only delete where status is 'Complete' or 'Cancelled'
        """
        validate.abort_if_user_role_not_appropriate("admin")
        # if user_role and order data confirmed ok

        if order_id:
         # see if order exists
            search_query = """
            SELECT * FROM orders WHERE orders.order_id = '{}'""".format(order_id)

            order = database.select_from_db(search_query)
            if not order:
                validate.abort_order_not_found(order_id)

            if order[0][3] not in ["Complete", "Cancelled"]:
                abort(make_response(jsonify(
                    message="Not deleted. Status is '{}'. \
Status must be 'Cancelled' or 'Complete' to delete".format(order[0][3])
                ), 401))

            # if order_status is 'Cancelled' or 'Complete'
            delete_single_order = """
            DELETE FROM orders
            WHERE orders.order_id = '{}'
            AND orders.order_status = 'Cancelled'
            OR orders.order_status = 'Complete' """.format(order_id)

            database.query_db_no_return(delete_single_order)

            # Confirm deletion by querying db for same item
            order = database.select_from_db(search_query)
            if order:
                # Means the deletion did not happen
                abort(make_response(jsonify(
                    message="Error. Not deleted for some reason"
                ), 500))
        else:
            delete_all_orders = """
            DELETE FROM orders WHERE orders.order_status = 'Complete'
            OR orders.order_status = 'Cancelled'"""

            database.query_db_no_return(delete_all_orders)

        response = make_response(jsonify(
            message="Delete successful."), 200)

        return response
