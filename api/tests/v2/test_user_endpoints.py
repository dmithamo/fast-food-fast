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

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response_json["message"],
            "Unauthorized. Please login.")

    def test_post_an_order(self):
        """
            2. Test that authorised (logged in) user can place an order
        """
        # Login admin and post food item on menu
        adm_token = self.login_test_admin()
        self.logged_in_admin_post_to_menu(
            {"food_item_name": "Guacamole",
             "food_item_price": 1000}, adm_token)

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
            1000 * food_item["quantity"])

    def test_post_a_second_order(self):
        """
            3. Test that authorised (logged in) user can place
            another order for same meal
            And get correct order in rsponse message
        """
        # Login admin and post food item on menu
        adm_token = self.login_test_admin()
        self.logged_in_admin_post_to_menu(
            {"food_item_name": "Guacamole",
             "food_item_price": 1000}, adm_token)

        # Register and login user
        token = self.login_test_user()
        food_item = {
            "food_item_id": 1,
            "quantity": 2
        }

        # Post first Order
        self.client.post("{}/users/orders".format(
            self.base_url), json=food_item, headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(token)
            })

        # Admin marks first order 'Complete'
        self.client.put("{}/orders/1".format(
            self.base_url), json={
                "order_status": "Complete"
            }, headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(adm_token)})

        # Repost the Order (same food item, different quantity)
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
            response_json["order"]["order_status"],
            "New")

    def test_user_cannot_order_non_existent_food(self):
        """
            4. Test that user cannot place order for an item not on the
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
            5. Test that user cannot place order with incomplete data
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
            "Unsuccesful. Missing 'quantity', which is a required param")

    # GET users/orders

    def test_unauthorized_user_get_all(self):
        """
            6. Test that an unauthorised user cannot get order history
        """
        response = self.client.get("{}/users/orders".format(
            self.base_url))

        response_json = base_test_class.helper_functions.response_as_json(
            response)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response_json["message"],
            "Unauthorized. Please login.")

    def test_get_all_orders_when_none_exist(self):
        """
            7. Test that authorised (logged in) user can get order history
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

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response_json["message"], "No orders yet for user 'dmithamo'")

    def test_get_all_orders_when_orders_exist(self):
        """
            8. Test that authorised (logged in) user can get order history
            When at least one order exists
        """
        # Login admin and post food item on menu
        adm_token = self.login_test_admin()
        self.logged_in_admin_post_to_menu(
            {"food_item_name": "Cassava",
             "food_item_price": 120}, adm_token)
        self.logged_in_admin_post_to_menu(
            {"food_item_name": "Mango Shake",
             "food_item_price": 400}, adm_token)

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
            response_json["message"], "Orders found.")
        self.assertEqual(len(response_json["orders"]), 2)
        self.assertEqual(
            response_json["orders"][0]["order_id"], 1)
        self.assertEqual(
            response_json["orders"][1]["order_id"], 2)
