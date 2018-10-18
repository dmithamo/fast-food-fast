"""
    Module contains re-usable helper functions
    Checks for validity of request data
    Aborts if data is in any way invalid
"""

from flask_jwt_extended import get_jwt_identity
from flask import abort, make_response, jsonify


# local imports
from api.v2.database import select_from_db


def abort_missing_required_param(required_params, data):
    """
        Checks whether all required params are present
        Aborts if any is missing or is None (e.g, 0 or "" )
    """
    for param in required_params:
        try:
            value = data["{}".format(param)]
        except KeyError:
            abort(make_response(jsonify(
                message="Unsuccesful. Missing '{}', which is a required param".format(param)), 400))


def abort_invalid_param(param, reason=""):
    """
        Checks whether all required params are present
        Aborts if any is missing or is None (e.g, 0 or "" )
    """
    for key, value in param.items():
        abort(make_response(jsonify(
            message="Unsuccessful. '{}' is an invalid {}. {}.".format(
                value, key, reason)), 400))


def abort_access_unauthorized():
    """
        Aborts if user is no authentication token
    """
    abort(make_response(jsonify(
        message="Unauthorised. No valid authentication token"), 403))


def abort_not_found(item, defn):
    """
        Aborts if no items found from db search
    """
    abort(make_response(jsonify(
        message="No '{}' found {}".format(item, defn)), 404))


def abort_order_not_found(order_id):
    """
        Aborts if order not in db
    """
    abort(make_response(jsonify(
        message="Order with id '{}' not found.".format(order_id)), 404))


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
                message="Error. '{}' '{}' \
is already in use".format(key, value)), 400))


def check_duplication_b(food_item_name, food_item_id):
    """
        Abort if new food_item_name would be a duplication
    """
    query = """
    SELECT * FROM menu WHERE menu.food_item_name = '{}'
    AND menu.food_item_id != '{}'""".format(food_item_name, food_item_id)

    food_item = select_from_db(query)
    if food_item:
        # Abort if it would be a duplication
        abort(make_response(jsonify(
            message="Error. {} is already in use".format(
                food_item_name)), 400))


def check_if_any_change(data, food_item):
    """
        See if the request represents a change in a food_item_param
    """
    formatted_food_item = {
        "food_item_name": food_item[0][1],
        "food_item_price": food_item[0][2]
    }
    name_not_changed = True
    price_not_changed = True

    for key, value in data.items():
        if key == "food_item_name" \
         and value != formatted_food_item["food_item_name"]:
            name_not_changed = False

        if key == "food_item_price" \
          and value != formatted_food_item["food_item_price"]:
            price_not_changed = False

    if name_not_changed and price_not_changed:
        # If neither param changed, abort
        abort(make_response(jsonify(
            message="Not updated. No change detected"), 400))


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
    required_params = ["username", "email", "password"]

    # if required param is missing, abort
    abort_missing_required_param(required_params, data)

    # check username
    username = data["username"]
    email = data["email"]
    password = data["password"]
    check_invalid_name("username", username)
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
        Carry out all checks necessary on login data
        Abort if any is invalid
    """
    username = data.get("username")
    if not username:
        email = data.get("email")
        if not email:
            abort(make_response(jsonify(
                message="Unsuccesful. Provide a 'username' or 'email', to login"), 400))
    try:
        password = data["password"]
    except KeyError:
        # If no username or email, or not password
        abort(make_response(jsonify(
            message="Unsuccesful. Missing 'password', which is required for login"), 400))
    
    # For valid params
    username_or_email = data.get("username") or data.get("email")
    password = data["password"]
    return {"username_or_email": username_or_email,
            "password": password}


def check_admin_logins(data):
    """
        Carry out all checks necessary on admin logins
        Abort if any is invalid
    """
    required_params = ["email", "password"]
    # if required param is missing, abort
    abort_missing_required_param(required_params, data)

    # Require specific email and password for admin
    email = data["email"]
    password = data["password"]
    if email != "admintest@admin.com":
        abort(make_response(jsonify(
            message="Unsuccessful. Incorrect admin email"), 400))
    if password != "admin-pass-10s":
        abort(make_response(jsonify(
            message="Wrong password"), 400))


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
        abort_invalid_param(
            {"email": email})
    if not user or not domain:
        abort_invalid_param(
            {"email": email})

    # Check that domain is valid
    # valid domain has valid part before and after '.'
    try:
        dom_1, dom_2 = domain.split(".")
    except ValueError:
        abort_invalid_param(
            {"email": email})
    if not dom_1 or not dom_2:
        abort_invalid_param(
            {"email": email})


def check_password_validity(password):
    """
        Checks for validity of provided password
    """
    if len(str(password)) < 8 \
      or " " in str(password):
        # If blank password or password too short
        abort_invalid_param(
            {"password": password},
            "Password must be at least an 8-char \
long alphanumeric without any spaces")


def check_food_item_params_a(data):
    """
        Check food params before placing to order
    """
    required_params = ["food_item_id", "quantity"]
    # abort if a required param is missing
    abort_missing_required_param(required_params, data)

    food_item_id = data["food_item_id"]
    quantity = data["quantity"]
    if not isinstance(food_item_id, int) or food_item_id <= 0:
        # Require that food_item_id be an int
        abort_invalid_param(
            {"food_item_id": food_item_id}, "'food_item_id' \
must be an int greater than 0")

    if not isinstance(quantity, int) or not quantity > 0:
        # Require that food_item_price be an int
        abort_invalid_param(
            {"quantity": quantity}, "'quantity' must be an \
int greater than 0")

    return {
        "food_item_id": food_item_id,
        "quantity": quantity
    }


def check_invalid_name(key, value):
    """
        Checks whether food_item_name or username are valid
    """
    if not isinstance(value, str) or not value.replace(
            " ", "").isalpha() \
     or not len(value.replace(" ", "")) > 3:
        # Require that food_item_name be a str
        abort_invalid_param(
            {"{}".format(key): value},
            "'{}' must be an alphabet-only str at least 4 chars long".format(
                key))


def check_food_item_params(data):
    """
        Check food params before adding to menu
    """
    required_params = ["food_item_name", "food_item_price"]
    # abort if missing a require param
    abort_missing_required_param(required_params, data)

    food_item_name = data["food_item_name"]
    food_item_price = data["food_item_price"]

    check_invalid_name("food_item_name", food_item_name)

    if not isinstance(food_item_price, int) or food_item_price <= 0:
        # Require that food_item_price be an int
        abort_invalid_param(
            {"food_item_price": food_item_price},
            "'food_item_price' must be an int greater than 0")

    check_duplication({"food_item_name": food_item_name}, "menu")

    food_item = {
        "food_item_name": food_item_name,
        "food_item_price": food_item_price}

    return food_item


def check_if_param_updatable(data):
    """
        Before PUT /menu/food_item_id, checks that param
        being updated is valid
    """
    for key, value in data.items():
        # if either is not a valid food_item_param
        if key not in ["food_item_name", "food_item_price"]:
            abort_not_food_item_param(key, "parameter")

        if key == "food_item_price" \
           and (not isinstance(value, int) or not value > 0):
            # If param being updated is food_item_price
            abort_not_food_item_param(value, "price")

        elif key == "food_item_name":
            check_invalid_name("food_item_name", value)


def abort_not_food_item_param(param_name, description):
    """
        Aborts if param is not a valid food_item_param
    """
    abort(make_response(
        jsonify(message="'{}' is an invalid food_item {}".format(
            param_name, description)), 400))


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
    required_params = ["order_status"]
    # abort if missing a required param
    abort_missing_required_param(required_params, data)

    order_status = data["order_status"]
    valid_statuses = ["Processing", "Cancelled", "Complete"]

    if not order_status.strip() in valid_statuses:
        # if status is invalid
        abort(make_response(
            jsonify(message="'{}' is an invalid order status. \
Valid statuses: '{}'".format(
    data["order_status"], valid_statuses)), 400))


    return order_status.strip()
