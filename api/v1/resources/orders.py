"""
   Models Order and defines methods callable on an Order
"""
from datetime import datetime
from flask import request, jsonify, abort, make_response
from flask_restful import Resource

CART = [] # Container for orders. List of dicts


def retrieve_order_from_list_by_id(order_id):
    """
        Helper method to fetch order from list of orders,
        given valid id
    """
    needed_order = None
    for order in CART:
        if order['order_id'] == order_id:
            needed_order = order
            break
    if not needed_order:
        abort_if_order_not_in_cart(order_id)

    return needed_order


def abort_if_order_not_in_cart(order_id):
    """
        Helper method to search for Order
        Abort if order not found and throw error
    """
    abort(make_response(
        jsonify(message="Order with id {} not found".format(order_id)), 404))


class Order(Resource):
    """
        Model and Order and define methods callable on an Order
    """

    def get(self, order_id):
        """
            GET /orders/<int:order_id>
            Return order with given order_id
        """
        order = retrieve_order_from_list_by_id(order_id)
        response = jsonify(order)
        response.status_code = 200

        return response

    def put(self, order_id):
        """
            PUT /orders/<int:order_id> endpoint
            Update the status of order with given order_id
        """
        order = retrieve_order_from_list_by_id(order_id)
        order_status = request.args.get('order_status')

        if order_status and order_status in ['confirmed', 'rejected']:
            # If order status is valid
            order['order_status'] = order_status
            order['status_updated_on'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Configure response
            response = jsonify(order)
            response.status_code = 201
        else:
            response = jsonify(message="Bad request. Invalid order status")
            response.status_code = 400
        return response


class ShoppingCart(Resource):
    """
        Models a container for orders, and defines the
        methods executable on the container
    """
    def get(self):
        """
            GET /orders endpoint
            Return all orders in CART, if any
        """
        if not CART:
            # If no orders as yet exist
            abort(make_response(
                jsonify(message="No orders exist as yet"), 404))
        else:
            # if at least one order exists
            response = jsonify({'orders' : CART})
            response.status_code = 200
        return response

    def post(self):
        """
            POST /orders endpoint
            Return created order
        """
        item_name = request.args.get('item_name')
        item_price = request.args.get('item_price')

        item_names_in_cart = [order['item_name'] for order in CART]


        if not item_name or not item_price:
            # If order is missing required item_name or item_price
            abort(make_response(
                jsonify(message="Bad request. Missing item_name or item_price"), 400))

        if item_name and item_price and item_name not in item_names_in_cart:
            # if order is a valid, and is not already in CART
            order_id = len(CART) + 1
            order = {
                'order_id' : order_id,
                'item_name' : item_name,
                'item_price' : item_price,
                'quantity' : 1,
                'ordered_on' : datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            # Save order
            CART.append(order)
            response = jsonify(order)
            response.status_code = 201

        elif item_name in item_names_in_cart:
            # if item has already been added to CART
            order = [order for order in CART if order['item_name'] == item_name][0]
            order['quantity'] += 1

            response = jsonify(order)
            response.status_code = 201

        return response
