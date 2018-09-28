"""
    Module contains tests for admin specific endpoints
"""
from api.tests.v2 import base_test_class


class TestEndpoints(base_test_class.TestClassBase):
    """
        Tests for admin specific endpoints
    """
    # GET /orders

    def test_unauthorized_admin_get_all(self):
        """
            1. Test that an unauthorised admin cannot get all orders
            by all users
        """
        response = self.client.get("{}/orders".format(
            self.base_url))

        response_json = base_test_class.helper_functions.response_as_json(
            response)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response_json["message"],
            "Forbidden. You must be logged in as admin")

    def test_get_all_orders_when_none_exist(self):
        """
            2. Test that logged in admin can access
            all orders from all users - when no orders exist
        """
        # Login admin
        token = self.login_test_admin()

        response = self.client.get("{}/orders".format(
            self.base_url), headers={
                "Content-Type": "application/json",
                "Authorization": token})

        response_json = base_test_class.helper_functions.response_as_json(
            response)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response_json["message"], "No orders exist as yet")

    def test_get_all_orders_when_orders_exist(self):
        """
            3. Test that logged in admin can get
            all orders  by all users - When at least one order exists
        """
        # Register and login user
        token = self.login_test_user()
        # Make POST requests
        self.logged_in_user_post_order(self.food, token)
        self.logged_in_user_post_order(self.food_2, token)

        # Login admin
        adm_token = self.login_test_admin()

        response = self.client.get("{}/orders".format(
            self.base_url), headers={
                "Content-Type": "application/json",
                "Authorization": adm_token})

        response_json = base_test_class.helper_functions.response_as_json(
            response)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response_json["message"], "Request successful")
        self.assertEqual(len(response_json["orders"]), 2)
        self.assertEqual(
            response_json["orders"][0]["order_id"], 1)
        self.assertEqual(
            response_json["orders"][1]["food_item_name"],
            self.food_2["food_item_name"])

    # GET /orders/order_id

    def test_unauthorized_admin_get_specific_order(self):
        """
            4. Test that an unauthorised admin cannot get specific order
        """
        # Register and login user
        token = self.login_test_user()
        # Make POST request
        self.logged_in_user_post_order(self.food, token)

        response = self.client.get("{}/orders".format(
            self.base_url), headers={
                "Content-Type": "application/json"})

        response_json = base_test_class.helper_functions.response_as_json(
            response)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response_json["message"],
            "Forbidden. You must be logged in as admin")

    def test_get_specific_order_when_not_exists(self):
        """
            5. Test that logged in admin cannot get
            a specific order When the order does not exist
        """
        # Login admin
        token = self.login_test_admin()

        response = self.client.get("{}/orders/10".format(
            self.base_url), headers={
                "Content-Type": "application/json",
                "Authorization": token})

        response_json = base_test_class.helper_functions.response_as_json(
            response)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response_json["message"], "Order with id 10 not found")

    def test_get_specific_order_when_order_exists(self):
        """
            6. Test that logged in admin can get
            specific order when the order exists
        """
        # Register and login user
        token = self.login_test_user()
        # Make POST request
        self.logged_in_user_post_order(self.food, token)

        # Login admin
        adm_token = self.login_test_admin()

        response = self.client.get("{}/orders/1".format(
            self.base_url), headers={
                "Content-Type": "application/json",
                "Authorization": adm_token})

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

    def test_put_order_when_order_does_not_exists(self):
        """
            7. Test that logged in admin cannot update
            order status when the order does not exists
        """
        # Login admin
        adm_token = self.login_test_admin()

        response = self.client.put("{}/orders/100".format(
            self.base_url), json={
                "order_status": "completed"
            }, headers={
                "Content-Type": "application/json",
                "Authorization": adm_token})

        response_json = base_test_class.helper_functions.response_as_json(
            response)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response_json["message"], "Order with id 100 not found")

    def test_put_order_when_order_exists(self):
        """
            8. Test that logged in admin can update
            order status when the order exists
        """
        # Register and login user
        token = self.login_test_user()
        # Make POST request
        self.logged_in_user_post_order(self.food_2, token)

        # Login admin
        adm_token = self.login_test_admin()

        response = self.client.put("{}/orders/1".format(
            self.base_url), json={
                "order_status": "completed"
            }, headers={
                "Content-Type": "application/json",
                "Authorization": adm_token})

        response_json = base_test_class.helper_functions.response_as_json(
            response)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response_json["message"], "Request successful")
        self.assertEqual(
            response_json["order"]["order_id"], 1)
        self.assertEqual(
            response_json["order"]["order_status"], "completed")

    def test_put_order_with_invalid_status(self):
        """
            9. Test that logged in admin cannot update
            order status with invalid status
        """
        # Register and login user
        token = self.login_test_user()
        # Make POST request
        self.logged_in_user_post_order(self.food_2, token)

        # Login admin
        adm_token = self.login_test_admin()

        response = self.client.put("{}/orders/1".format(
            self.base_url), json={
                "order_status": "what have you"
            }, headers={
                "Content-Type": "application/json",
                "Authorization": adm_token})

        response_json = base_test_class.helper_functions.response_as_json(
            response)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response_json["message"], "Error. Invalid order status")

    # GET /menu

    def test_get_menu_when_no_items(self):
        """
            10. Test that users can access
            the menu when menu is empty
        """
        response = self.client.get("{}/menu".format(
            self.base_url), headers={
                "Content-Type": "application/json"})

        response_json = base_test_class.helper_functions.response_as_json(
            response)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response_json["message"], "No items on the menu")

    def test_get_menu(self):
        """
            11. Test that admin and user can get
            all items on the menu
        """
        # Login admin
        adm_token = self.login_test_admin()
        # Make POST /menu request
        self.logged_in_admin_post_to_menu(self.new_food, adm_token)
        self.logged_in_admin_post_to_menu(self.food, adm_token)

        response = self.client.get("{}/menu".format(
            self.base_url), headers={
                "Content-Type": "application/json"})

        response_json = base_test_class.helper_functions.response_as_json(
            response)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response_json["message"], "Request successful")
        self.assertEqual(len(response_json["menu"]), 2)
        self.assertEqual(
            response_json["menu"][0]["food_item_id"], 1)
        self.assertEqual(
            response_json["menu"][1]["food_item_name"],
            self.food["food_item_name"])

    def test_post_menu(self):
        """
            12. Test that logged in admin can add
            items to the menu
        """
        # Login admin
        adm_token = self.login_test_admin()

        response = self.client.post("{}/menu".format(
            self.base_url), json=self.food, headers={
                "Content-Type": "application/json",
                "Authorization": adm_token})

        response_json = base_test_class.helper_functions.response_as_json(
            response)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response_json["message"], "Request successful")
        self.assertEqual(
            response_json["food_item"]["food_item_id"], 1)
        self.assertEqual(
            response_json["food_item"]["food_item_name"],
            self.food["food_item_name"])

    def test_post_menu_cannot_duplicate(self):
        """
            13. Test that logged in admin cannot
            add duplicate items on the menu
        """
        # Login admin
        adm_token = self.login_test_admin()
        # Make first POST
        self.logged_in_admin_post_to_menu(self.food, adm_token)

        # POST with same food item
        response = self.client.post("{}/menu".format(
            self.base_url), json=self.food, headers={
                "Content-Type": "application/json",
                "Authorization": adm_token})

        response_json = base_test_class.helper_functions.response_as_json(
            response)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response_json["message"], "Bad request. Food item already exists")

    def test_put_menu(self):
        """
            14. Test that logged in admin can modify
            params of items on the menu
        """
        # Login admin
        adm_token = self.login_test_admin()
        # POST food item
        self.logged_in_admin_post_to_menu(self.new_food, adm_token)

        response = self.client.put("{}/menu/1".format(
            self.base_url), json={
                "food_item_price": 10000
            }, headers={
                "Content-Type": "application/json",
                "Authorization": adm_token})

        response_json = base_test_class.helper_functions.response_as_json(
            response)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response_json["message"], "Request successful")
        self.assertEqual(
            response_json["food_item"]["food_item_id"], 1)
        self.assertEqual(
            response_json["food_item"]["food_item_price"], 10000)
        self.assertNotEqual(
            response_json["food_item"]["food_item_price"],
            self.new_food["food_itme_price"])
