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
            # Generate token for registered user
            auth_token = new_user.generate_auth_token(registered_user_data[0][0])

            registered_user = {
                "user_id": registered_user_data[0][0],  # first item is user_id
                "username": registered_user_data[0][1],  # second item is username
                "email": registered_user_data[0][2],  # third item is email
                "auth_token": User.decode_auth_token(auth_token)
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


class UserLogin(Resource):
    """
        Sets up UserLogin as a Resource
        Logs in user if params are valid
    """
    def post(self):
        """
            POST auth/login enpoint
        """
        try:
            # Get json from request object
            data = request.get_json()
        except:
            abort(make_response(jsonify(
                message="Bad request. Data must be json-formatted"
            ), 400))
        try:
            # extract params from json
            email = data["email"]
            password = data["password"]
        except KeyError:
            abort(make_response(jsonify(
                message="Bad request. Supply email AND password to login"
            ), 400))

        if not email or not password:
            abort(make_response(jsonify(
                message="Supply valid credentials to login."
            ), 400))
        try:
            user = User.retrieve_user_from_db(email)
            if not user:
                abort(make_response(jsonify(
                    message="User not found."), 404))

            user_id_from_db = user[0][0]
            username_from_db = user[0][1]
            email_from_db = user[0][2]
            password_hash_from_db = user[0][3]

            password_valid = User.check_password_at_login(
                password_hash_from_db, password)

            # Check password
            if not password_valid:
                abort(make_response(jsonify(
                    message="Wrong password."), 403))

            auth_token = User.generate_auth_token(user_id_from_db)

            logged_in_user = {
                "user_id": user_id_from_db,  # first item is user_id
                "username": username_from_db,  # second item is username
                "email": email_from_db,  # third item is email
                "auth_token": User.decode_auth_token(auth_token)
                }

            # Return successful login response
            response = make_response(jsonify({
                "message": "Login successful.",
                "user": logged_in_user
            }), 201)

        except psycopg2.DatabaseError as error:
            abort(make_response(jsonify(
                message="Server error : {}".format(error)
            ), 500))

        return response
