"""
  Initialize a Flask instance and configure as appropriate,
  Define API endpoints as routes
"""
from flask import Flask
from flask_restful import Api


# local imports
from api.v1.resources.orders import Order, ShoppingCart
from instance.config import DevelopmentConfig

APP = Flask(__name__)
APP.config.from_object(DevelopmentConfig)
API = Api(APP)

API.add_resource(Order, '/fastfoodfast/api/v1/orders/<int:order_id>')
API.add_resource(ShoppingCart, '/fastfoodfast/api/v1/orders')
