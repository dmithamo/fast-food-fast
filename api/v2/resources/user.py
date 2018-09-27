"""
    Module sets up UserRegistration, UserLogin as Resources
"""

from flask import request, jsonify, abort, make_response
from flask_restful import Resource

# local imports
from api.v2.models import User
from api.v2.utils import validate

class UserRegistration(Resource):
    """
        Set up UserRegistration resource
        Registers a user if request data is valid
    """
    def post(self):
        """
            POST /auth/signup endpoint
        """
        # Check whether request is valid
        data = validate.check_request_validity(request)

        # Check validity of registration params
        registration_params = validate.check_registration_params(data)

        # Register user
        username = registration_params['username']
        user_email = registration_params['user_email']
        password = registration_params['password']

        # See if username or email is already in use
        validate.check_duplication({"username": username})
        validate.check_duplication({"user_email": user_email})
        # User(username, user_email, password)
        # new_user = User.create_new_user()
        response = make_response(jsonify(
            message="No duplicates"
        ), 201)

        return response
