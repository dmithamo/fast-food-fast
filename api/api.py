"""
   Initialize a Flask instance and configure as appropriate,
   Define API endpoints as routes
"""


from flask import Flask, request, jsonify

from models.models import ShoppingCart
import config

API = Flask(__name__)
API.config.from_object(config.DevelopmentConfig)

BASE_URL = '/fastfoodfast/api/v1'
# Initialize a ShoppingCart object
MYCART = ShoppingCart()


@API.route('{}/orders'.format(BASE_URL), methods=['POST'])
def place_orders():
    """
        Respond to POST requests to /fastfoodfast/api/v1/orders endpoint
    """
    # Retrieve the order_params from the request object
    item_name = request.args.get('name')
    item_price = request.args.get('price')

    if item_name and item_price:
        # Place order if valid order_params
        order_params = {
            'item_name' : item_name,
            'item_price' : item_price
        }
        order = MYCART.place_order(order_params)

        # Configure a response
        response = jsonify({
            'item_id' : order.item_id,
            'item_name' : order.item_name,
            'item_price' : order.item_price,
            'ordered_on' : order.item_ordered_on,
            'quantity' : order.item_quantity
        })
        response.status_code = 201

    else:
        # Handle invalid order_params
        response = jsonify(
            message='Bad request. No order name or price'
        )
        response.status_code = 400
    return response

@API.route('{}/orders'.format(BASE_URL), methods=['GET'])
def get_orders():
    """
        Respond to GET requests to /fastfoodfast/api/v1/orders endpoint
    """
    all_orders = MYCART.get_orders()

    all_orders = [
        {
            'item_id' : order.item_id,
            'item_name' : order.item_name,
            'item_price' : order.item_price,
            'ordered_on' : order.item_ordered_on,
            'quantity' : order.item_quantity
        }
        for order in all_orders
    ]

    # Configure a response
    # If one or more orders exist in the cart
    if all_orders:
        response = jsonify({
            '{} Orders'.format(len(all_orders)) : all_orders
            })

    else:
        # if no orders yet
        response = jsonify(
            message='No orders as yet exist'
        )

    response.status_code = 200
    return response
