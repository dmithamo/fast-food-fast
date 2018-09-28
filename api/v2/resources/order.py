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
from api.v2.models import User


class ShoppingCart(Resource):
    """
        Models a users's shopping cart with all user orders
    """
    def get(self):
        """
            GET users/orders endpoint
        """
        data = validate.check_request_validity(request)
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
            validate.abort_not_found(decoded_token, "orders")

        response = make_response(jsonify({
            "message": "Orders found.",
            "food": orders
        }), 200)

        return response