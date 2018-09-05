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
def orders():
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
            'ordered_item_id' : order.item_id,
            'ordered_item_name' : order.item_name,
            'ordered_item_price' : order.item_price,
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

