"""
  Define API endpoints as routes
"""
from flask_restful import Api


# local imports
from api.v2 import APP
from api.v2.resources import user


API = Api(APP)

# Base url common to all endpoints
BASE_URL = '/api/v2'

API.add_resource(user.UserRegistration, '{}/auth/signup'.format(BASE_URL))
