"""
  Initialize a Flask instance and configure as appropriate,
  Define API endpoints as routes
"""
from flask import Flask
from flask_restful import Api


# local imports
from api.v1.resources.orders import Order

app = Flask(__name__)
API = Api(app)

API.add_resource(Order, '/fastfoodfast/api/v1/orders')
