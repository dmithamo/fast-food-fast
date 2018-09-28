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
from api.v2.models import User
from api.v2 import database


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
        # Model admin as user
        admin = User("admin", data["email"], data["password"])
        # save to db fro token verification later
        query = """
        INSERT INTO users (username, email, password)
        VALUES ('{}', '{}', '{}')""".format(admin.username, admin.email, admin.password)
        database.insert_into_db(query)

        # Generate token for admin
        response = make_response(jsonify({
            "message": "Admin succesfully authenticated",
            "admin": {
                "email": admin.email,
                "auth_token": str(self.generate_auth_token(admin.email.split("@")))
            }
        }), 201)

        return response
