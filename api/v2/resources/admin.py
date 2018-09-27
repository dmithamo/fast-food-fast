"""
    Module defines admin specific endpoints
"""
import os
import jwt
import datetime

from flask import request, jsonify, make_response, abort
from flask_restful import Resource



# local imports
from api.v2.utils import validate


class AdminLogin(Resource):
    """
        Define admin specific methods
    """

    @staticmethod
    def generate_auth_token(name):
        """
            Generate authentication token on login
        """
        payload = {"admin": name}

        token = jwt.encode(payload, os.getenv('SECRET_KEY'), algorithm='HS256')
        return token

    def post(self):
        """
            POST /login
        """
        data = validate.check_request_validity(request)
        # Generate token for admin
        response = make_response(jsonify({
            "message": "Admin succesfully authenticated",
            "admin": {
                "email": data["email"],
                "auth_token": str(self.generate_auth_token(data["email"].split("@")))
            }
        }), 201)

        return response
