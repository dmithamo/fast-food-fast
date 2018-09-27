"""
    Module sets up UserRegistration, UserLogin as Resources
"""
import psycopg2

from flask import request, jsonify, abort, make_response
from flask_restful import Resource

# local imports
from api.v2.models import User
from api.v2.utils import validate
from api.v2.database import select_from_db


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
        email = registration_params['email']
        password = registration_params['password']

        # See if username or email is already in use
        validate.check_duplication({"username": username})
        validate.check_duplication({"email": email})

        # Register new user
        new_user = User(username, email, password)

        try:
            new_user.save_new_user_to_db()
            # See if new_user was added to db
            query = """
            SELECT user_id, username, email FROM users WHERE users.username = '{}';
            """.format(username)

            registered_user_data = select_from_db(query)

            registered_user = {
                "user_id": registered_user_data[0][0],  # first item is user_id
                "username": registered_user_data[0][1],  # second item is username
                "email": registered_user_data[0][2]  # third item is email
                }

            response = make_response(
                jsonify({
                    "message": "Registration successful",
                    "user": registered_user}), 201)

        except (Exception, psycopg2.DatabaseError) as error:
            response = make_response(jsonify({
                "message": "Server error : {}".format(error)
            }), 500)

        return response
