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

def abort_if_no_json_from_request(req_data):
    """
        Helper function.
        Aborts if a json could not be obtained from request data
    """
    if req_data is None:
        # If a json was not obtained from the request
        abort(make_response(
            jsonify(message="Bad request. Request data must be in json format"), 400))

def abort_if_missing_required_param():
    """
        Helper function.
        Aborts if request data is missing a required argument
    """
    abort(make_response(
        jsonify(message="Bad request. Missing required param"), 400))

def calculate_order_cost(order):
    """
        Helper function.
        Calculates the total cost of an order
    """
    order['total_order_cost'] = order['item_price'] * order['quantity']

def make_new_order(name, price, quantity):
    """
        Helper function
        Makes a new order, and prepares the response as a json

    """
    if name and price and quantity:
        # If all the required params are not None
        order_id = len(CART) + 1
        order = {
            'order_id' : order_id,
            'item_name' : name,
            'item_price' : price,
            'quantity' : quantity,
            'order_status' : 'pending',
            'ordered_on' : datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        # Calcute order cost
        calculate_order_cost(order)
        CART.append(order)
        response = jsonify(CART[-1])
        response.status_code = 201
    else:
        # if any of the required params is None
        abort_if_missing_required_param()
    return response

class Order(Resource):
    """
        Model and Order and define methods callable on an Order
    """

    def get(self, order_id):
        """
            GET /orders/<int:order_id>
        """
        order = retrieve_order_from_list_by_id(order_id)
        response = jsonify(order)
        response.status_code = 200

        return response

    def put(self, order_id):
        """
            PUT /orders/<int:order_id> endpoint
        """
        order = retrieve_order_from_list_by_id(order_id)
        data = request.get_json()
        abort_if_no_json_from_request(data)
        try:
            order_status = data['order_status']
            if order_status not in ['accepted', 'rejected', 'completed']:
                # If order status is not valid
                abort(make_response(
                    jsonify(message="Bad request. Invalid order status"), 400))
            # Valid order status
            order['order_status'] = order_status
            order['status_updated_on'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Configure response
            response = jsonify(order)
            response.status_code = 201
            return response

        except KeyError:
            # if order status is not provided in request
            abort_if_missing_required_param()


class ShoppingCart(Resource):
    """
        Models a container for orders, and defines the
        methods executable on the container
    """
    def get(self):
        """
            GET /orders endpoint
        """
        if not CART:
            # If no orders as yet exist
            abort(make_response(
                jsonify(message="No orders exist as yet"), 404))
        # if at least one order exists
        response = jsonify({'orders' : CART})
        response.status_code = 200
        return response

    def post(self):
        """
            POST /orders endpoint
        """
        data = request.get_json()
        abort_if_no_json_from_request(data)
        try:
            item_name = data['item_name']
            item_price = data['item_price']
            quantity = data['quantity']
        except KeyError:
            # If order is missing required item_name or item_price
            abort_if_missing_required_param()

        if CART:
            # If any orders have already been added to CART
            try:
                # See if an order with similar name is already in CART,
                # and has not been serviced yet
                unserviced_order = [
                    order for order in CART if order['item_name'] == item_name and
                    order['order_status'] == 'pending'][0]

                unserviced_order['quantity'] += quantity
                # Update order cost
                calculate_order_cost(unserviced_order)
                response = jsonify(unserviced_order)
                response.status_code = 201

            except IndexError:
                # if a similar order has not been added to CART, or
                # any that have been added have been marked
                # 'accepted', 'rejected' or 'completed'
                response = make_new_order(item_name, item_price, quantity)
        else:
            # if the CART is empty
            response = make_new_order(item_name, item_price, quantity)

        return response
