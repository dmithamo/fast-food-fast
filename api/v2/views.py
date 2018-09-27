"""
  Define API endpoints as routes
"""
from flask_restful import Api


# local imports
from api.v2 import APP


API = Api(APP)
