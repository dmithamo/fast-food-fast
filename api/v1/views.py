"""
  Initialize a Flask instance and configure as appropriate,
  Define API endpoints as routes
"""
from flask import Flask
from flask_restful import Api


# local imports
from api.v1.resources.orders import Order, ShoppingCart
from instance.config import CONFIGS

APP = Flask(__name__)
APP.config.from_object(CONFIGS['development_config'])
API = Api(APP)

API.add_resource(Order, '/v1/orders/<int:order_id>')
API.add_resource(ShoppingCart, '/v1/orders')
