"""
    Models a base test class from which other
    test classes are defined
"""
import os
import unittest

# local imports
from run import APP
from api.v2.config import CONFIGS
from api.v2.database import init_db
from api.tests.v2 import helper_functions


class TestClassBase(unittest.TestCase):
    """
        Base test class
    """
    def setUp(self):
        """
            Configure params usable accross every test
        """
        self.app = APP
        testing_config = CONFIGS['testing_config']
        self.app.config.from_object(testing_config)
        self.client = self.app.test_client()

        # Define a base url, common to all endpoints
        self.base_url = "/api/v2"

        # Set up sample params, extract for use within tests
        sample_params = helper_functions.sample_params()

        self.admin_logins = sample_params["admin_logins"]
        self.user = sample_params["user"]
        self.user_2 = sample_params["user_2"]
        self.user_logins = sample_params["user_logins"]
        self.food = sample_params["food"]
        self.food_2 = sample_params["food_2"]
        self.new_food = sample_params["new_food"]
        self.food_fake = sample_params["food_fake"]

        with self.app.app_context():
            # Retrieve test_db url from env
            self.db_url = CONFIGS['test_db_url']
            # initialize db, create tables
            init_db(self.db_url)

    def tearDown(self):
        """
            Recreate the db connection and
            recreate all the tables, wiping all data
        """
        with self.app.app_context():
            init_db(self.db_url)

    def register_test_user(self):
        """
            Helper function
            Registers a user for use during testing
        """
        resp = self.client.post("{}/auth/signup".format(
            self.base_url), json=self.user, headers={
                "Content-Type": "application/json"
            })

        auth_token = helper_functions.response_as_json(
            resp)['user']['auth_token']

        return auth_token


    def login_test_user(self):
        """
            Helper function
            Logs in the user registered above for use during testing
        """
        # Register user
        self.register_test_user()
        # Login the user
        resp = self.client.post("{}/auth/login".format(
            self.base_url), json=self.user_logins, headers={
                "Content-Type": "application/json"
            })

        auth_token = helper_functions.response_as_json(
            resp)['user']['auth_token']

        return auth_token

    def logged_in_user_post_order(self, food_item, token):
        """
            Helper function
            Posts an order with logged in user
        """
        # Make POST request
        self.client.post("{}/users/orders".format(
            self.base_url), json=food_item, headers={
                "Content-Type": "application/json", "Authorization": "Bearer {}".format(token)
            })

    def login_test_admin(self):
        """
            Helper function
            Logs in the admin
        """
        # Login the admin
        resp = self.client.post("{}/login".format(
            self.base_url), json=self.admin_logins, headers={
                "Content-Type": "application/json"
            })

        auth_token = helper_functions.response_as_json(
            resp)['admin']['token']
        return auth_token

    def logged_in_admin_post_to_menu(self, food_item, token):
        """
            Helper function
            Posts a new food item to menu with admin logged in
        """
        # Make POST request
        self.client.post("{}/menu".format(
            self.base_url), json=food_item, headers={
                "Content-Type": "application/json", "Authorization": "Bearer {}".format(token)
            })


if __name__ == '__main__':
    unittest.main()
