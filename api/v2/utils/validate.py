"""
    Module contains re-usable helper functions
    Checks for validity of request data
    Aborts if data is in any way invalid
"""
from flask import abort, make_response, jsonify


# local imports
from api.v2.database import select_from_db


def abort_missing_required_param():
    """
        Checks whether all required params are present
        Aborts if any is missing or is None (e.g, 0 or "" )
    """
    abort(make_response(jsonify(
        message="Unsuccesful. Missing required param"), 400))

def abort_invalid_param(param):
    """
        Checks whether all required params are present
        Aborts if any is missing or is None (e.g, 0 or "" )
    """
    for key, value in param.items():
        abort(make_response(jsonify(
            message="Bad request. '{}' is an invalid {}".format(value, key)), 400))

def abort_access_unauthorized():
    """
        Aborts if user is no authentication token
    """
    abort(make_response(jsonify(
        message="Unauthorised. You must be logged in"), 403))


def check_request_validity(request):
    """
        Checks if request data is in json format
        Aborts if request data is in non-json format
    """
    try:
        data = request.get_json()
    except:
        abort(make_response(jsonify(
            message="Bad request. Request data must be json formatted"), 400))

    return data


def check_admin_logins(data):
    """
        Carry out all checks necessary on admin logins
        Abort if any is invalid
    """
    try:
        email = data["email"]
        password = data["password"]
    except KeyError:
        # if required param is missing, abort
        abort_missing_required_param()
    # Check if email is valid
    check_email_validity(email)
    # check password length
    check_password_validity(password)

    # Require specific email and password for admin
    if not email == "admintest@admin.com" or not password == "admin-pass-10s":
        abort_access_unauthorized()
    return data

def check_registration_params(data):
    """
        Carry out all checks necessary on registration data
        Abort if any is invalid
    """
    try:
        username = data["username"]
        email = data["email"]
        password = data["password"]
    except KeyError:
        # if required param is missing, abort
        abort_missing_required_param()
    # check username
    check_username_validity(username)
    # check email
    check_email_validity(email)
    # check password
    check_password_validity(password)

    # For valid params
    return data

def check_email_validity(email):
    """
        Checks that provided email address is valid
    """
    # Check has user and domain components
    try:
        user, domain = email.split("@")
    except ValueError:
        abort_invalid_param({"email": email})

    # Check that domain is valid
    try:
        a, b = domain.split(".")
    except ValueError:
        abort_invalid_param({"email": email})

def check_username_validity(username):
    """
        Checks for validity of provided username
    """
    if len(username) < 4:
        # If blank username or too short
        abort_invalid_param({"username": username})

def check_password_validity(password):
    """
        Checks for validity of provided password
    """
    if len(password) < 8:
        # If blank password or password too short
        abort_invalid_param({"password": password})

def check_duplication(params, table_name):
    """
        Check if a param is already in use, abort if in use
    """
    for key, value in params.items():
        query = """
        SELECT {} from {} WHERE {}.{} = '{}'
        """.format(key, table_name, table_name, key, value)
        duplicated = select_from_db(query)
        if duplicated:
            # Abort if duplicated
            abort(make_response(jsonify(
                message="Error. {} is already in use".format(key)), 400))

def check_food_item_params(data):
    """
        Check food params before adding to menu
    """
    try:
        food_item_name = data["food_item_name"]
        food_item_price = data["food_item_price"]
    except KeyError:
        abort_missing_required_param()

    if not isinstance(food_item_name, str):
        # Require that food_item_name be a str
        abort_invalid_param({"food_item_name": food_item_name})

    if not isinstance(food_item_price, int):
        # Require that food_item_price be an int
        abort_invalid_param({"food_item_price": food_item_price})

    check_duplication({"food_item_name": food_item_name}, "menu")

    food_item = {
        "food_item_name": food_item_name,
        "food_item_price": food_item_price}

    return food_item
