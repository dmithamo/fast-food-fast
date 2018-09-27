"""
    Module contains tests for user registration and login
"""
import os
import unittest

# local imports
from api.v2.views import APP
from api.v2.config import CONFIGS
from api.v2.database import init_db
from api.tests.v2 import helper_functions


class TestUserRegistrationAndLogin(unittest.TestCase):
    """
        Tests for user registration and Login
    """

    def setUp(self):
        """
            Configure params usable accross every test
        """
        # Define a base url, common to all endpoints
        self.base_url = '/api/v2/auth'

        # Retrieve db_url from env
        self.db_url = os.getenv("DB_URL")
        # initialize db, create tables
        init_db(self.db_url)

        APP.config.from_object(CONFIGS['testing_config'])

        self.app = APP
        self.client = self.app.test_client()

        # Sample data for registration
        self.user = helper_functions.sample_params()["user"]
        self.user_2 = helper_functions.sample_params()["user_2"]

        # Sample data for login in
        self.user_logins = helper_functions.sample_params()["user_logins"]

        with self.app.app_context():
            # initialize db, create tables
            init_db(self.db_url)

    def tearDown(self):
        """
            Recreate the db connection and
            recreate all the tables, wiping all data
        """
        with self.app.app_context():
            init_db(self.db_url)

    def test_user_registration(self):
        """
           1. Test whether registration with valid data succeeds
        """
        response = self.client.post("{}/signup".format(
            self.base_url), json=self.user_2, headers={
                'Content-Type': 'application/json'})

        response_json = helper_functions.response_as_json(response)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_json['message'], "Registration successful")
        self.assertTrue(response_json['user']['auth_token'])

    def test_user_registration_missing_some_data(self):
        """
           2. Test that registration fails without all required data
        """
        response = self.client.post('{}/signup'.format(
            self.base_url), json=self.user_logins, headers={
                'Content-Type': 'application/json'})

        response_json = helper_functions.response_as_json(response)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response_json['message'], "Unsuccesful. Missing required param")

    def test_user_registration_without_any_data(self):
        """
           3. Test that registration fails without data
        """
        response = self.client.post("{}/signup".format(
            self.base_url), json={}, headers={
                'Content-Type': 'application/json'})

        response_json = helper_functions.response_as_json(response)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response_json['message'], "Unsuccesful. Missing required param")

    def test_duplicate_email_registration(self):
        """
           4. Test that registration with email already in use fails
        """
        self.client.post("{}/signup".format(
            self.base_url), json=self.user, headers={
                'Content-Type': 'application/json'})

        response = self.client.post("{}/signup".format(
            self.base_url), json={
                "username": "mithamod",
                "email": "dmithamo@andela.com",
                "password": "dmit-password"
            }, headers={
                'Content-Type': 'application/json'})

        response_json = helper_functions.response_as_json(response)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response_json['message'], "Error. email is already in use")

    def test_duplicate_user_name_registration(self):
        """
           5. Test that registration with username already in use fails
        """
        # Register a user
        self.client.post("{}/signup".format(
            self.base_url), json=self.user, headers={
                'Content-Type': 'application/json'})

        response = self.client.post("{}/signup".format(
            self.base_url), json={
                "username": "dmithamo",
                "email": "myemail@andela.com",
                "password": "dmit-weedpass"
            }, headers={
                'Content-Type': 'application/json'})

        response_json = helper_functions.response_as_json(response)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response_json['message'], "Error. username is already in use")

    def test_invalid_email_registration(self):
        """
           6. Test that registration with invalid email fails
        """
        response = self.client.post("{}/signup".format(
            self.base_url), json={
                "username": "dmithamo",
                "email": "myemail.andela.com",
                "password": "dmit-weedpass"
            }, headers={
                'Content-Type': 'application/json'})

        response_json = helper_functions.response_as_json(response)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response_json['message'],
            "Bad request. 'myemail.andela.com' is an invalid email")

    def test_user_registration_invalid_username(self):
        """
           7. Test that registration fails with invalid username
        """
        response = self.client.post('{}/signup'.format(
            self.base_url), json={
                "username": "d",
                "email": "dmithamo@andela.com",
                "password": "dmit-password"
            }, headers={
                'Content-Type': 'application/json'})

        response_json = helper_functions.response_as_json(response)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response_json['message'],
            "Bad request. 'd' is an invalid username")

    def test_user_registration_invalid_password(self):
        """
           8. Test that registration fails with invalid password
        """
        response = self.client.post('{}/signup'.format(
            self.base_url), json={
                "username": "dennisb",
                "email": "dmithamo@andela.com",
                "password": "dmit"
            }, headers={
                'Content-Type': 'application/json'})

        response_json = helper_functions.response_as_json(response)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response_json['message'],
            "Bad request. 'dmit' is an invalid password")

    def test_registered_user_login(self):
        """
            9. Test that a registered user can login
        """
        # Register a user
        self.client.post("{}/signup".format(
            self.base_url), json=self.user, headers={
                'Content-Type': 'application/json'})

        # Attempt login
        response = self.client.post("{}/login".format(
            self.base_url), json=self.user_logins, headers={
                'Content-Type': 'application/json'})

        response_json = helper_functions.response_as_json(response)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_json['message'], "Login successful.")
        self.assertTrue(response_json['user']['auth_token'])

    def test_unregistered_user_login(self):
        """
            10. Test that an unregistered user cannot login
        """

        response = self.client.post("{}/login".format(
            self.base_url), json={
                "email": "mary@kenya.co.ke",
                "password": "passwords-are-us"
            }, headers={
                'Content-Type': 'application/json'})

        response_json = helper_functions.response_as_json(response)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response_json['message'], "User not found.")

    def test_user_login_with_wrong_password(self):
        """
            11. Test that user cannot login with invalid credentials
        """
        # Register a user
        resp1 = self.client.post("{}/signup".format(
            self.base_url), json={
                "username": "dennismith",
                "email": "dennismith@andela.com",
                "password": "is-correct"}, headers={
                    'Content-Type': 'application/json'})

        self.assertEqual(resp1.status_code, 201)

        # Attempt login
        response = self.client.post("{}/login".format(
            self.base_url), json={
                "email": "dennismith@andela.com",
                "password": "is-not-correct"}, headers={
                    'Content-Type': 'application/json'})

        response_json = helper_functions.response_as_json(response)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response_json['message'], "Wrong password.")


if __name__ == '__main__':
    unittest.main()
