"""
    Module contains re-usable helper functions
    Checks for validity of request data
    Aborts if data is in any way invalid
"""

from flask_jwt_extended import get_jwt_identity
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
            message="Bad request. '{}' is an invalid {}".format(
                value, key)), 400))


def abort_access_unauthorized():
    """
        Aborts if user is no authentication token
    """
    abort(make_response(jsonify(
        message="Unauthorised. No valid authentication token"), 403))


def abort_not_found(item, defn):
    """
        Aborts if user is no items found from db search
    """
    abort(make_response(jsonify(
        message="No '{}' found {}".format(item, defn)), 404))


def abort_order_not_found(order_id):
    """
        Aborts if order not in db
    """
    abort(make_response(jsonify(
        message="Order with id '{}' not found.".format(order_id)), 404))


def check_request_validity(request):
    """
        Checks if request data is in json format
        Aborts if request data is in non-json format
    """
    data = request.get_json() or None
    if not data:
        abort(make_response(jsonify(
            message="Bad request. Request data must be json formatted"), 400))

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
    return {"username": username,
            "email": email,
            "password": password}


def check_login_params(data):
    """
        Carry out all checks necessary on registration data
        Abort if any is invalid
    """
    try:
        # extract params from json
        email = data["email"]
        password = data["password"]
    except KeyError:
        abort_missing_required_param()

    # For valid params
    return {"email": email,
            "password": password}


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

    # Require specific email and password for admin
    if not email == "admintest@admin.com" or not password == "admin-pass-10s":
        abort(make_response(jsonify(
            message="Unsuccessful. Invalid admin credentials"), 400))


def check_email_validity(email):
    """
        Checks that provided email address is valid
    """
    # prevent user from registering with admin email
    if email == "admintest@admin.com":
        abort(make_response(jsonify(
            message="Email already in use"), 400))
    # Check has valid user and domain components
    try:
        user, domain = str(email).split("@")
    except ValueError:
        abort_invalid_param({"email": email})
    if not user or not domain:
        abort_invalid_param({"email": email})

    # Check that domain is valid
    # valid domain has valid part before and after '.'
    try:
        dom_1, dom_2 = domain.split(".")
    except ValueError:
        abort_invalid_param({"email": email})
    if not dom_1 or not dom_2:
        abort_invalid_param({"email": email})


def check_username_validity(username):
    """
        Checks for validity of provided username
    """
    if len(str(username)) < 4:
        # If blank username or too short
        abort_invalid_param({"username": username})


def check_password_validity(password):
    """
        Checks for validity of provided password
    """
    if len(str(password)) < 8:
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
                message="Error. {} is already in use".format(value)), 400))


def check_food_item_params_a(data):
    """
        Check food params before placing to order
    """
    try:
        food_item_id = data["food_item_id"]
        quantity = data["quantity"]
    except KeyError:
        abort_missing_required_param()

    if not isinstance(food_item_id, int):
        # Require that food_item_id be an int
        abort_invalid_param({"food_item_id": food_item_id})

    if not isinstance(quantity, int):
        # Require that food_item_price be an int
        abort_invalid_param({"quantity": quantity})

    return {
        "food_item_id": food_item_id,
        "quantity": quantity
    }


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


def abort_if_user_role_not_appropriate(allowed_role):
    """
        For admin specific endpoints, aborts if role extracted from
        identity is not 'admin'
    """
    # extract user id from token
    user_role = get_jwt_identity()[1]
    if not user_role == allowed_role:
        abort(make_response(jsonify(
            message="Forbidden. '{}' not allowed to access this route".format(
                user_role)), 403))


def check_order_status_validity(data):
    """
        Check whether the status supplied when updating order
        is valid
    """
    try:
        order_status = data["order_status"]
    except KeyError:
        abort_missing_required_param()

    if not data["order_status"] in ["New",
                                    "Processing",
                                    "Cancelled", "Complete"]:
        # if status is invalid
        abort(make_response(
            jsonify(message="'{}' is an invalid order status".format(
                data["order_status"])), 400))
    return order_status
