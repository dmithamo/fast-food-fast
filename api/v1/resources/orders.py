"""
   Models Order and defines methods callable on an Order
"""
from flask import request, jsonify
from flask_restful import Resource
from datetime import datetime


all_orders = {} # Container for orders. Key = order_id, Value = order_params

class Order(Resource):
    """
        Model an Order params and define the order methods
    """
    def post(self):
        """
            Make order using order params from request object
            and save to all_orders dict
        """
        order_params = request.get_json()
        item_name = order_params['item_name']
        item_price = order_params['item_price']

        if item_name and item_price:
            # Respond to a valid POST/orders request
            new_order = {
                'item_id' : len(all_orders) + 1,
                'item_name' : item_name,
                'item_price' : item_price,
                'ordered_on' : datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            # Append new_order to dict of orders
            all_orders[new_order['item_id']] = new_order
            response = jsonify(new_order), 201
        else:
            # If request is missing required data
            response = jsonify({
                'message' : 'Bad request. Missing item_name or Item_price'
            }), 400
        return response
