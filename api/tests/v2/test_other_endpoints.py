"""
    Module contains tests for other endpoints
"""
import unittest
import json

# local imports
from api.v2 import APP
from api.v2.config import CONFIGS
from api.v2.database import init_db


def response_as_json(resp):
    """
        Helper function
        Loads response as json for easier inspection
    """
    resp_json = json.loads(resp.data.decode('utf-8'))
    return resp_json


class TestEndpoints(unittest.TestCase):
    """
        Tests for user registration and Login
    """

    def setUp(self):
        """
            Configure params usable accross every test
        """
        self.app = APP
        self.app.config.from_object(CONFIGS['testing_config'])
        self.client = self.app.test_client()

        # Sample data for registration
        self.user = {
            "username": "dmithamo",
            "user_email": "dmithamo@andela.com",
            "password": "dmit-password"
        }

        # Sample data for login in
        self.user_logins = {
            "user_email": "dmithamo@andela.com",
            "password": "dmit-password"
        }

        # Sample order data for POST request
        self.food = {
            "food_item_name": "Guacamole and Marshmallows",
            "food_item_price": 200,
            "quantity": 2
        }

        # Define a base url, common to all endpoints
        self.base_url = "/api/v2"

        with self.app.app_context():
            # initialize db, create tables
            init_db()

    def tearDown(self):
        """
            Recreate the db connection and
            recreate all the tables, wiping all data
        """
        with self.app.app_context():
            init_db()

    def register_test_user(self):
        """
            Helper function
            Registers a user for use during testing
        """
        self.client.post("{}/auth/signup".format(
            self.base_url), json=self.user, headers={
                "Content-Type": "application/json"
            })

    def login_test_user(self):
        """
            Helper function
            Logs in the user registered above for use during testing
        """
        self.register_test_user()  # Register user
        # Login the user
        resp = self.client.post("{}/auth/login".format(
            self.base_url), json=self.user_logins, headers={
                "Content-Type": "application/json"
            })

        auth_token = response_as_json(resp)['Authorization']
        return auth_token


    def test_post_an_order(self):
        """
            1. Test that authorised (logged in) user place an order
        """
        # Register and login user
        token = self.login_test_user()

        response = self.client.post("{}/users/orders".format(
            self.base_url), json=self.food, headers={
                "Content-Type": "application/json", "Authorization": token
            })
        response_json = response_as_json(response)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response_json["message"], "Order posted successfully")
        self.assertEqual(
            response_json["order"]["total_order_cost"],
            self.food["food_item_price"] * self.food["quantity"])
        self.assertFalse(
            response_json["order"]["order_id"], None)

    def test_unauthorized_user_post(self):
        """
            3. Test that unauthorised user cannot place order
        """
        response = self.client.post("{}/users/orders".format(
            self.base_url), json=self.food, headers={
                "Content-Type": "application/json"})

        response_json = response_as_json(response)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response_json["message"], "Forbidden. You must be logged in")

    def test_user_cannot_order_non_existent_food(self):
        """
            4. Test that user cannot place order for an item not on the
            menu
        """
        token = self.login_test_user()
        response = self.client.post("{}/users/orders".format(
            self.base_url), json=self.food, headers={
                "Content-Type": "application/json", "Authorization": token
            })

        response_json = response_as_json(response)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response_json["message"], "Food item not found")

    def test_incomplete_order_data(self):
        """
            5. Test that user cannot place order with invalid data
            menu
        """
        token = self.login_test_user()
        response = self.client.post("{}/users/orders".format(
            self.base_url), json={
                "food_item_name": "Gucamole",
                "food_item_price": 200
            }, headers={
                "Content-Type": "application/json", "Authorization": token
            })

        response_json = response_as_json(response)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response_json["message"],
            "Bad request. Missing required order param")
        