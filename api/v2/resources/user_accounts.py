"""
    Module sets up UserRegistration, UserLogin as Resources
"""
import datetime
import psycopg2

from flask_jwt_extended import create_access_token

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
        validate.check_duplication({"username": username}, "users")
        validate.check_duplication({"email": email}, "users")

        # Register new user
        new_user = User(username, email, password)

        new_user.save_new_user_to_db()
        # See if new_user was added to db successfully
        query = """
        SELECT user_id, username, email FROM users
        WHERE users.username = '{}';
        """.format(username)

        registered_user_data = select_from_db(query)
        if not registered_user_data:
            # This means recently registered user was not saved to db
            abort(make_response(jsonify(
                message="Server error. User not registered in db."), 500))

        registered_user = {
            "user_id": registered_user_data[0][0],
            "username": registered_user_data[0][1],
            "email": registered_user_data[0][2]
            }

        response = make_response(
            jsonify({
                "message": "Registration successful",
                "user": registered_user}), 201)

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
        data = validate.check_request_validity(request)
        user_data = validate.check_login_params(data)
        try:
            # Attempt to find user by email
            user = User.retrieve_user_from_db_by_email(user_data["username_or_email"])
            if not user:
                # Attempt to find user by username
                user = User.retrieve_user_from_db_by_username(user_data["username_or_email"])
                if not user:
                    # When both fail to find a user, abort
                    abort(make_response(jsonify(
                        message="User not found."), 404))

            # If user found
            user_id_from_db = user[0][0]
            username_from_db = user[0][1]
            email_from_db = user[0][2]
            password_hash_from_db = user[0][3]

            password_valid = User.check_password_at_login(
                password_hash_from_db, user_data["password"])

            # Check password
            if not password_valid:
                abort(make_response(jsonify(
                    message="Wrong password."), 403))

            # Generate token for logged in user
            token = create_access_token(
                identity=(username_from_db, "user"),
                expires_delta=datetime.timedelta(days=5))

            logged_in_user = {
                "user_id": user_id_from_db,  # first item is user_id
                "username": username_from_db,  # second item is username
                "email": email_from_db,  # third item is email
                "logged_in_at": datetime.datetime.utcnow().strftime(
                    "%Y-%m-%d %H:%M:%S"),
                "auth_token": token
                }

            # Return successful login response
            response = make_response(jsonify({
                "message": "Login successful.",
                "user": logged_in_user
            }), 200)

        except psycopg2.DatabaseError as error:
            abort(make_response(jsonify(
                message="Server error : {}".format(error)
            ), 500))

        return response
