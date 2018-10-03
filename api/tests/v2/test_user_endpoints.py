"""
    Module contains tests for other user specific endpoints
"""
from api.tests.v2 import base_test_class


class TestEndpoints(base_test_class.TestClassBase):
    """
        Tests for user specific endpoints
    """
    # POST users/orders

    def test_unauthorized_user_post(self):
        """
            1. Test that unauthorised user cannot place order
        """

        response = self.client.post("{}/users/orders".format(
            self.base_url), json={
                "food_item_id": 1,
                "quantity": 4
            }, headers={
                "Content-Type": "application/json"})

        response_json = base_test_class.helper_functions.response_as_json(
            response)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response_json["message"],
            "Forbidden. You must be logged in.")

    def test_post_an_order(self):
        """
            2. Test that authorised (logged in) user can place an order
        """
        # Login admin and post food item on menu
        adm_token = self.login_test_admin()
        self.logged_in_admin_post_to_menu({"food_item_name": "Guacamole", "food_item_price": 1000}, adm_token)

        # Register and login user
        token = self.login_test_user()
        food_item = {
            "food_item_id": 1,
            "quantity": 2
        }

        response = self.client.post("{}/users/orders".format(
            self.base_url), json=food_item, headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(token)
            })
        response_json = base_test_class.helper_functions.response_as_json(
            response)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response_json["message"], "Order posted successfully")
        self.assertEqual(
            response_json["order"]["total_order_cost"],
            self.food["food_item_price"] * food_item["quantity"])

    def test_user_cannot_order_non_existent_food(self):
        """
            3. Test that user cannot place order for an item not on the
            menu
        """
        token = self.login_test_user()
        response = self.client.post("{}/users/orders".format(
            self.base_url), json={
                "food_item_id": 11100,
                "quantity": 1
            }, headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(token)
            })

        response_json = base_test_class.helper_functions.response_as_json(
            response)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response_json["message"],
            "No 'food item with id '11100' ' found in menu")

    def test_incomplete_order_data(self):
        """
            4. Test that user cannot place order with incomplete data
        """
        token = self.login_test_user()
        response = self.client.post("{}/users/orders".format(
            self.base_url), json={
                "food_item_id": 1
            }, headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(token)
            })

        response_json = base_test_class.helper_functions.response_as_json(
            response)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response_json["message"],
            "Unsuccesful. Missing required param")

    # GET users/orders

    def test_unauthorized_user_get_all(self):
        """
            5. Test that an unauthorised user cannot get order history
        """
        response = self.client.get("{}/users/orders".format(
            self.base_url))

        response_json = base_test_class.helper_functions.response_as_json(
            response)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response_json,
            "Forbidden. You must be logged in.")

    def test_get_all_orders_when_none_exist(self):
        """
            6. Test that authorised (logged in) user can get order history
            When no orders exist
        """
        # Register and login user
        token = self.login_test_user()

        response = self.client.get("{}/users/orders".format(
            self.base_url), headers={
                "Content-Type": "application/json", 
                "Authorization": "Bearer {}".format(token)
            })

        response_json = base_test_class.helper_functions.response_as_json(
            response)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response_json["message"], "No 'orders' found for user 'dmithamo' ")

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
        food = {"food_item_id": 1, "quantity": 2}
        food_2 = {"food_item_id": 2, "quantity": 1}
        self.food_2["quantity"] = 1
        self.logged_in_user_post_order(food, token)
        self.logged_in_user_post_order(food_2, token)

        response = self.client.get("{}/users/orders".format(
            self.base_url), headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(token)
            })

        response_json = base_test_class.helper_functions.response_as_json(
            response)

        # self.assertEqual(response.status_code, 200)
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
        food = {"food_item_id": 1, "quantity": 2}
        food_2 = {"food_item_id": 2, "quantity": 1}
        self.logged_in_user_post_order(food, token)
        self.logged_in_user_post_order(food_2, token)

        response = self.client.get("{}/users/orders/1".format(
            self.base_url))

        response_json = base_test_class.helper_functions.response_as_json(
            response)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response_json, "Forbidden. You must be logged in.")

    def test_get_specific_orders_when_not_exists(self):
        """
            9. Test that authorised (logged in) user cannot get
            a specific order When the order does not exist
        """
        # Register and login user
        token = self.login_test_user()

        response = self.client.get("{}/users/orders/10".format(
            self.base_url), headers={
                "Content-Type": "application/json", 
                "Authorization": "Bearer {}".format(token)})

        response_json = base_test_class.helper_functions.response_as_json(
            response)

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
                "Content-Type": "application/json", 
                "Authorization": "Bearer {}".format(token)})

        response_json = base_test_class.helper_functions.response_as_json(
            response)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response_json["message"], "Request successful")
        self.assertEqual(
            response_json["order"]["order_id"], 1)
        self.assertEqual(
            response_json["order"]["food_item_name"],
            self.food["food_item_name"])