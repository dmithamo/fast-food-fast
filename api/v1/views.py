"""
  Define API endpoints as routes
"""
from flask_restful import Api


# local imports
from api.v1 import APP
from api.v1.resources.orders import Order, ShoppingCart


API = Api(APP)
API.add_resource(Order, '/v1/orders/<int:order_id>')
API.add_resource(ShoppingCart, '/v1/orders')
