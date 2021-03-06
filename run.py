"""
    Initialize flask app instance and configure
    as appropriate.
    Serve api endpoints
"""
from flask import Flask, make_response, jsonify, redirect
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS

# local imports
from api.v2.config import CONFIGS

# local imports
from api.v2.database import init_db


# import resources
from api.v2.resources.user_accounts import UserRegistration, UserLogin
from api.v2.resources.orders import ShoppingCart
from api.v2.resources.menu import Menu
from api.v2.resources.admin_only_routes import AdminLogin, AllOrders, Order


APP = Flask(__name__)
CORS(APP)
APP.config.from_object(CONFIGS['development_config'])

API = Api(APP)

with API.app.app_context():
    # Initialize db
    init_db(CONFIGS["db_url"])
    # Add auth
    jwt = JWTManager(APP)


@jwt.unauthorized_loader
def custom_error_response_unauthorised_user(callback):
    """
        Custom response to attempt to access protected routes without
        authorization header
    """
    response = make_response(jsonify(
        message="Unauthorized. Please login."), 401)
    return response


@jwt.expired_token_loader
def custom_error_response_expired_token():
    """
        Custom response for expired tokens
    """
    response = make_response(jsonify(
        message="Your token has expired. Please login again."), 401)
    return response


# Base url common to all endpoints
BASE_URL = '/api/v2'

# Access api docs at homepage of api
@APP.route('/')
def documentation():
    """
        Redirect to API docs on visiting root url
    """
    return redirect(
        "https://dmithamofastfoodfast.docs.apiary.io/#")


# Define routes
API.add_resource(UserRegistration, '{}/auth/signup'.format(BASE_URL))
API.add_resource(UserLogin, '{}/auth/login'.format(BASE_URL))
API.add_resource(ShoppingCart, '{}/users/orders'.format(BASE_URL))
API.add_resource(Menu, '{}/menu'.format(
    BASE_URL), '{}/menu/<int:food_item_id>'.format(BASE_URL))
API.add_resource(AdminLogin, '{}/login'.format(BASE_URL))
API.add_resource(AllOrders, '{}/orders'.format(BASE_URL))
API.add_resource(Order, '{}/orders/<int:order_id>'.format(BASE_URL))


if __name__ == '__main__':
    APP.run(debug=True)
