"""
    Module contains tests for other user specific endpoints
"""
import unittest

# local imports
from api.v2 import APP
from api.v2.config import CONFIGS
from api.v2.database import init_db
from api.tests.v2 import helper_functions


class TestEndpoints(unittest.TestCase):
    """
        Tests for user specific endpoints
    """

    def setUp(self):
        """
            Configure params usable accross every test
        """
        self.app = APP
        self.app.config.from_object(CONFIGS['testing_config'])
        self.client = self.app.test_client()

        # Define a base url, common to all endpoints
        self.base_url = "/api/v2"

        # Set up sample params, extract for use within tests
        sample_params = helper_functions.sample_params()

        self.user = sample_params["user"]
        self.user_logins = sample_params["user_logins"]
        self.admin_logins = sample_params["admin_logins"]
        self.food = sample_params["food"]
        self.food_2 = sample_params["food_2"]
        self.food_fake = sample_params["food_fake"]

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
        # Register user
        self.register_test_user()
        # Login the user
        resp = self.client.post("{}/auth/login".format(
            self.base_url), json=self.user_logins, headers={
                "Content-Type": "application/json"
            })

        auth_token = helper_functions.response_as_json(resp)['Authorization']
        return auth_token

    def logged_in_user_post_order(self, food_params, token):
        """
            Helper function
            Posts an order with logged in user
        """
        # Make POST request
        self.client.post("{}/users/orders".format(
            self.base_url), json=food_params, headers={
                "Content-Type": "application/json", "Authorization": token
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

        auth_token = helper_functions.response_as_json(resp)['Authorization']
        return auth_token

    def logged_in_admin_post_to_menu(self, food_params, token):
        """
            Helper function
            Posts a new food item to menu with admin logged in
            Makes food items available for order
        """
        # Make POST request
        self.client.post("{}/menu".format(
            self.base_url), json=food_params, headers={
                "Content-Type": "application/json", "Authorization": token
            })

    # POST users/orders

    def test_unauthorized_user_post(self):
        """
            1. Test that unauthorised user cannot place order
        """
        # Login admin and post food item on menu
        adm_token = self.login_test_admin()
        self.logged_in_admin_post_to_menu(self.food, adm_token)

        # Add quantity to food itema and attempt to place order
        self.food["quantity"] = 2

        response = self.client.post("{}/users/orders".format(
            self.base_url), json=self.food, headers={
                "Content-Type": "application/json"})

        response_json = helper_functions.response_as_json(response)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response_json["message"], "Forbidden. You must be logged in")

    def test_post_an_order(self):
        """
            2. Test that authorised (logged in) user can place an order
        """
        # Login admin and post food item on menu
        adm_token = self.login_test_admin()
        self.logged_in_admin_post_to_menu(self.food, adm_token)

        # Add quantity to food itema and attempt to place order
        self.food["quantity"] = 1

        # Register and login user
        token = self.login_test_user()

        response = self.client.post("{}/users/orders".format(
            self.base_url), json=self.food, headers={
                "Content-Type": "application/json", "Authorization": token
            })
        response_json = helper_functions.response_as_json(response)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response_json["message"], "Order posted successfully")
        self.assertEqual(
            response_json["order"]["total_order_cost"],
            self.food["food_item_price"] * self.food["quantity"])
        self.assertFalse(
            response_json["order"]["food_item_price"],
            self.food["food_item_name"])

    def test_user_cannot_order_non_existent_food(self):
        """
            3. Test that user cannot place order for an item not on the
            menu
        """
        token = self.login_test_user()
        response = self.client.post("{}/users/orders".format(
            self.base_url), json=self.food_fake, headers={
                "Content-Type": "application/json", "Authorization": token
            })

        response_json = helper_functions.response_as_json(response)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response_json["message"], "Food item not found")

    def test_incomplete_order_data(self):
        """
            4. Test that user cannot place order with incomplete data
        """
        token = self.login_test_user()
        response = self.client.post("{}/users/orders".format(
            self.base_url), json={
                "food_item_name": "Gucamole",
                "food_item_price": 200
            }, headers={
                "Content-Type": "application/json", "Authorization": token
            })

        response_json = helper_functions.response_as_json(response)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response_json["message"],
            "Bad request. Missing required order param")

    # GET users/orders

    def test_unauthorized_user_get_all(self):
        """
            5. Test that an unauthorised user cannot get order history
        """
        response = self.client.get("{}/users/orders".format(
            self.base_url))

        response_json = helper_functions.response_as_json(response)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response_json["message"], "Forbidden. You must be logged in")

    def test_get_all_orders_when_none_exist(self):
        """
            6. Test that authorised (logged in) user can get order history
            When no orders exist
        """
        # Register and login user
        token = self.login_test_user()

        response = self.client.get("{}/users/orders".format(
            self.base_url), headers={
                "Content-Type": "application/json", "Authorization": token})

        response_json = helper_functions.response_as_json(response)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response_json["message"], "No orders exist as yet")

    def test_get_all_orders_when_orders_exist(self):
        """
            7. Test that authorised (logged in) user can get order history
            When at least one order exists
        """
        # Login admin and post food item on menu
        adm_token = self.login_test_admin()
        self.logged_in_admin_post_to_menu(self.food, adm_token)
        self.logged_in_admin_post_to_menu(self.food_2, adm_token)

        # Register and login user
        token = self.login_test_user()
        # Make some POST request
        self.food["quantity"] = 3
        self.food_2["quantity"] = 1
        self.logged_in_user_post_order(self.food, token)
        self.logged_in_user_post_order(self.food_2, token)

        response = self.client.get("{}/users/orders".format(
            self.base_url), headers={
                "Content-Type": "application/json", "Authorization": token})

        response_json = helper_functions.response_as_json(response)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response_json["message"], "Request successful")
        self.assertEqual(len(response_json["orders"]), 2)
        self.assertEqual(
            response_json["orders"][0]["order_id"], 1)
        self.assertEqual(
            response_json["orders"][1]["order_id"], 2)

    # GET users/orders/order_id

    def test_unauthorized_user_get_specific_order(self):
        """
            8. Test that an unauthorised user cannot get specific order
        """
        # Login admin and post food item on menu
        adm_token = self.login_test_admin()
        self.logged_in_admin_post_to_menu(self.food, adm_token)

        # Register and login user
        token = self.login_test_user()
        # Make some POST request
        self.food["quantity"] = 3
        self.food_2["quantity"] = 1
        self.logged_in_user_post_order(self.food, token)
        self.logged_in_user_post_order(self.food_2, token)

        response = self.client.get("{}/users/orders/1".format(
            self.base_url))

        response_json = helper_functions.response_as_json(response)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response_json["message"], "Forbidden. You must be logged in")

    def test_get_specific_orders_when_not_exists(self):
        """
            9. Test that authorised (logged in) user cannot get
            a specific order When the order does not exist
        """
        # Register and login user
        token = self.login_test_user()

        response = self.client.get("{}/users/orders/10".format(
            self.base_url), headers={
                "Content-Type": "application/json", "Authorization": token})

        response_json = helper_functions.response_as_json(response)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response_json["message"], "Order with id 10 not found")

    def test_get_specific_order_when_order_exists(self):
        """
            10. Test that authorised (logged in) user can get
            specific order when the order exists
        """
        # Login admin and post food item on menu
        adm_token = self.login_test_admin()
        self.logged_in_admin_post_to_menu(self.food, adm_token)

        # Register and login user
        token = self.login_test_user()
        # Make some POST request
        self.food["quantity"] = 3
        self.food_2["quantity"] = 1
        self.logged_in_user_post_order(self.food, token)
        self.logged_in_user_post_order(self.food_2, token)

        # Make POST request
        self.logged_in_user_post_order(self.food, token)

        response = self.client.get("{}/users/orders/1".format(
            self.base_url), headers={
                "Content-Type": "application/json", "Authorization": token})

        response_json = helper_functions.response_as_json(response)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response_json["message"], "Request successful")
        self.assertEqual(
            response_json["order"]["order_id"], 1)
        self.assertEqual(
            response_json["order"]["food_item_name"],
            self.food["food_item_name"])


if __name__ == '__main__':
    unittest.main()
