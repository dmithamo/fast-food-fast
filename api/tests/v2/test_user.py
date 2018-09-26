"""
    Module contains tests for user registration and login
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


class TestUserRegistrationAndLogin(unittest.TestCase):
    """
        Tests for user registration and Login
    """

    def setUp(self):
        """
            Configure params usable accross every test
        """
        self.app = APP
        self.app.config.from_object(CONFIGS['testing_config'])
        self.api_testing_client = self.app.test_client()

        # Sample data for registration
        self.test_user_data = {
            "username": "dmithamo",
            "user_email": "dmithamo@andela.com",
            "password": "dmit-password"
        }

        # Sample data for login in
        self.partial_user_data = {
            "user_email": "dmithamo@andela.com",
            "password": "dmit-password"
        }

        # Define a base url, common to all endpoints
        self.base_url = "/auth/api/v2"

        with self.app.app_context():
            # initialize db, create tables
            init_db()
            print("\n\n\nDB Connection successful\n\n\n")

    def tearDown(self):
        """
            Recreate the db connection and
            recreate all the tables, wiping all data
        """
        with self.app.app_context():
            init_db()

    def test_user_registration(self):
        """
           1. Test whether registration with valid data succeeds
        """
        response = self.api_testing_client.post("{}/signup".format(
            self.base_url), json=self.test_user_data, headers={
                'Content-Type': 'application/json'})

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response_as_json(response)['message'], "Registration succesful")

    def test_user_registration_missing_some_data(self):
        """
           2. Test that registration fails without all required data
        """
        response = self.api_testing_client.post("{}/signup".format(
            self.base_url), json=self.partial_user_data, headers={
                'Content-Type': 'application/json'})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_as_json(
            response)['message'], "Unsuccesful. Missing required param")

    def test_user_registration_without_any_data(self):
        """
           3. Test that registration fails without data
        """
        response = self.api_testing_client.post("{}/signup".format(
            self.base_url), json={}, headers={
                'Content-Type': 'application/json'})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_as_json(
            response)['message'], "Unsuccesful. Missing required param")

    def test_duplicate_user_email_registration(self):
        """
           4. Test that registration with email already in use fails
        """
        self.api_testing_client.post("{}/signup".format(
            self.base_url), json=self.test_user_data, headers={
                'Content-Type': 'application/json'})

        response = self.api_testing_client.post("{}/signup".format(
            self.base_url), json={
                "username": "mithamod",
                "user_email": "dmithamo@andela.com",
                "password": "dmit-password"
            }, headers={
                'Content-Type': 'application/json'})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_as_json(
            response)['message'], "Unsuccesful. Email already in use")

    def test_duplicate_user_name_registration(self):
        """
           5. Test that registration with email already in use fails
        """
        # Register a user
        self.api_testing_client.post("{}/signup".format(
            self.base_url), json=self.test_user_data, headers={
                'Content-Type': 'application/json'})

        response = self.api_testing_client.post("{}/signup".format(
            self.base_url), json={
                "username": "dmithamo",
                "user_email": "myemail@andela.com",
                "password": "dmit-weedpass"
            }, headers={
                'Content-Type': 'application/json'})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_as_json(
            response)['message'], "Unsuccesful. Username already in use")

    def test_invalid_user_email_registration(self):
        """
           6. Test that registration with email already in use fails
        """
        response = self.api_testing_client.post("{}/signup".format(
            self.base_url), json={
                "username": "dmithamo",
                "user_email": "myemail.andela.com",
                "password": "dmit-weedpass"
            }, headers={
                'Content-Type': 'application/json'})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_as_json(
            response)['message'], "Unsuccesful. Username already in use")

    def test_registered_user_login(self):
        """
            7. Test that a registered user can login
        """
        # Register a user
        self.api_testing_client.post("{}/signup".format(
            self.base_url), json=self.test_user_data, headers={
                'Content-Type': 'application/json'})

        response = self.api_testing_client.post("{}/login".format(
            self.base_url), json=self.partial_user_data, headers={
                'Content-Type': 'application/json'})
        # Attempt login
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_as_json(
            response)['message'], "Login successful.")

    def test_unregistered_user_login(self):
        """
            8. Test that an unregistered user cannot login
        """

        response = self.api_testing_client.post("{}/login".format(
            self.base_url), json=self.partial_user_data, headers={
                'Content-Type': 'application/json'})

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_as_json(
            response)['message'], "Unsuccessful. User unknown.")

    def test_user_login_with_wrong_password(self):
        """
            9. Test that user cannot login with invalid credentials
        """
        # Register a user
        self.api_testing_client.post("{}/auth/signup".format(
            self.base_url), json=self.test_user_data)
        # Attempt login
        response = self.api_testing_client.post("{}/login".format(
            self.base_url), json={
                "user_email": "dmithamo@andela.com",
                "password": "not-correct"}, headers={
                    'Content-Type': 'application/json'})

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response_as_json(
            response)['message'], "Unsuccessful. Invalid credentials.")
