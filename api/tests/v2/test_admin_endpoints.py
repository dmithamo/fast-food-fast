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

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response_json["message"],
            "Unauthorized. Please login.")

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
                "Authorization": "Bearer {}".format(token)})

        response_json = base_test_class.helper_functions.response_as_json(
            response)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response_json["message"], "No orders yet.")

    def test_get_all_orders_when_orders_exist(self):
        """
            3. Test that logged in admin can get
            all orders  by all users - When at least one order exists
        """
        # Login admin and post food item on menu
        adm_token = self.login_test_admin()
        self.logged_in_admin_post_to_menu(
            {"food_item_name": "Watermelon",
             "food_item_price": 10,
             "food_item_img": "Watermelon"}, adm_token)
        self.logged_in_admin_post_to_menu(
            {"food_item_name": "Orange Juice",
             "food_item_price": 70,
             "food_item_img": "Juice"}, adm_token)

        # Register and login user
        token = self.login_test_user()
        # Make POST requests
        self.logged_in_user_post_order({"food_item_id": 1,
                                        "quantity": 3}, token)
        self.logged_in_user_post_order({"food_item_id": 2,
                                        "quantity": 5}, token)
        # Login admin
        adm_token = self.login_test_admin()

        response = self.client.get("{}/orders".format(
            self.base_url), headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(adm_token)})

        response_json = base_test_class.helper_functions.response_as_json(
            response)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response_json["message"], "Orders found.")
        self.assertEqual(len(response_json["orders"]), 2)
        self.assertEqual(
            response_json["orders"][0]["order_id"], 1)

        self.assertIn("Orange Juice",
                      response_json["orders"][1]["order_info"])

        self.assertIn("Watermelon",
                      response_json["orders"][0]["order_info"])

    # GET /orders/order_id

    def test_unauthorized_admin_get_specific_order(self):
        """
            4. Test that an unauthorised admin cannot get specific order
        """
        response = self.client.get("{}/orders".format(
            self.base_url), headers={
                "Content-Type": "application/json"})

        response_json = base_test_class.helper_functions.response_as_json(
            response)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response_json["message"],
            "Unauthorized. Please login.")

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
                "Authorization": "Bearer {}".format(token)})

        response_json = base_test_class.helper_functions.response_as_json(
            response)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response_json["message"], "Order with id '10' not found.")

    def test_get_specific_order_when_order_exists(self):
        """
            6. Test that logged in admin can get
            specific order when the order exists
        """
        # Login admin
        adm_token = self.login_test_admin()
        # Add item to menu
        adm_token = self.login_test_admin()
        self.logged_in_admin_post_to_menu(
            {"food_item_name": "Sembe Moto",
             "food_item_price": 70,
             "food_item_img": "Sembe"}, adm_token)

        # Register and login user
        token = self.login_test_user()
        # Make POST request
        self.logged_in_user_post_order({"food_item_id": 1,
                                        "quantity": 2}, token)

        # Login admin
        adm_token = self.login_test_admin()

        response = self.client.get("{}/orders/1".format(
            self.base_url), headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(adm_token)})

        response_json = base_test_class.helper_functions.response_as_json(
            response)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response_json["message"], "Order found.")
        self.assertEqual(
            response_json["order"]["order_id"], 1)
        self.assertEqual(
            response_json["order"]["order_info"], "2 x Sembe Moto @ Ksh. 70")

    def test_put_order_when_order_does_not_exists(self):
        """
            7. Test that logged in admin cannot update
            order status when the order does not exists
        """
        # Login admin
        adm_token = self.login_test_admin()

        response = self.client.put("{}/orders/100".format(
            self.base_url), json={
                "order_status": "Complete"
            }, headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(adm_token)})

        response_json = base_test_class.helper_functions.response_as_json(
            response)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response_json["message"], "Order with id '100' not found.")

    def test_put_order_when_order_exists(self):
        """
            8. Test that logged in admin can update
            order status when the order exists
        """
        # Login admin
        adm_token = self.login_test_admin()
        # Add item to menu
        self.logged_in_admin_post_to_menu(
            {"food_item_name": "Flowerey Things",
             "food_item_price": 2000,
             "food_item_img": "Things"}, adm_token)

        # Register and login user
        token = self.login_test_user()
        # Make POST request
        self.logged_in_user_post_order({"food_item_id": 1,
                                        "quantity": 2}, token)

        response = self.client.put("{}/orders/1".format(
            self.base_url), json={
                "order_status": "Complete"
            }, headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(adm_token)})

        response_json = base_test_class.helper_functions.response_as_json(
            response)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response_json["message"], "Order found.")
        self.assertEqual(
            response_json["order"]["order_id"], 1)
        self.assertEqual(
            response_json["order"]["order_status"], "Complete")

    def test_put_order_with_invalid_status(self):
        """
            9. Test that logged in admin cannot update
            order status with invalid status
        """
        # Login admin
        adm_token = self.login_test_admin()
        # Add item to menu
        self.logged_in_admin_post_to_menu(
            {"food_item_name": "Njugu Karanga",
             "food_item_price": 20,
             "food_item_img": "Njugu"}, adm_token)

        # Register and login user
        token = self.login_test_user()
        # Make POST request
        self.logged_in_user_post_order({"food_item_id": 1,
                                        "quantity": 2}, token)

        response = self.client.put("{}/orders/1".format(
            self.base_url), json={
                "order_status": "what have you"
            }, headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(adm_token)})

        response_json = base_test_class.helper_functions.response_as_json(
            response)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response_json["message"],
            "'what have you' is an invalid order status. \
Valid statuses: '['Processing', 'Cancelled', 'Complete']'")

    def test_put_order_when_order_was_already_cancelled(self):
        """
            10. Test that logged in admin cannot update
            order status when order has already been Cancelled
        """
        # Login admin
        adm_token = self.login_test_admin()
        # Add item to menu
        self.logged_in_admin_post_to_menu(
            {"food_item_name": "Njugu Karanga",
             "food_item_price": 20,
             "food_item_img": "Njugu"}, adm_token)

        # Register and login user
        token = self.login_test_user()
        # Make POST request
        self.logged_in_user_post_order({"food_item_id": 1,
                                        "quantity": 2}, token)

        self.client.put("{}/orders/1".format(
            self.base_url), json={
                "order_status": "Cancelled"
            }, headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(adm_token)})

        response = self.client.put("{}/orders/1".format(
            self.base_url), json={
                "order_status": "Cancelled"
            }, headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(adm_token)})

        response_json = base_test_class.helper_functions.response_as_json(
            response)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response_json["message"],
            "Not allowed. This order is already 'Cancelled'")

    def test_put_order_when_order_status_is_complete(self):
        """
            11. Test that logged in admin cannot update
            order status when order has already been marked Complete
        """
        # Login admin
        adm_token = self.login_test_admin()
        # Add item to menu
        self.logged_in_admin_post_to_menu(
            {"food_item_name": "Njugu Karanga",
             "food_item_price": 20,
             "food_item_img": "Njugu"}, adm_token)

        # Register and login user
        token = self.login_test_user()
        # Make POST request
        self.logged_in_user_post_order({"food_item_id": 1,
                                        "quantity": 2}, token)

        self.client.put("{}/orders/1".format(
            self.base_url), json={
                "order_status": "Complete"
            }, headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(adm_token)})

        response = self.client.put("{}/orders/1".format(
            self.base_url), json={
                "order_status": "Cancelled"
            }, headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(adm_token)})

        response_json = base_test_class.helper_functions.response_as_json(
            response)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response_json["message"],
            "Not allowed. This order is already 'Complete'")

    def test_put_order_when_order_was_already_deleted(self):
        """
            12. Test that logged in admin cannot update
            order status when order has already been Deleted
        """
        # Login admin
        adm_token = self.login_test_admin()
        # Add item to menu
        self.logged_in_admin_post_to_menu(
            {"food_item_name": "Njugu Karanga",
             "food_item_price": 20,
             "food_item_img": "Njugu"}, adm_token)

        # Register and login user
        token = self.login_test_user()
        # Make POST request
        self.logged_in_user_post_order({"food_item_id": 1,
                                        "quantity": 2}, token)

        # Change status to Cancelled to allow for Delete
        self.client.put("{}/orders/1".format(
            self.base_url), json={
                "order_status": "Cancelled"
            }, headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(adm_token)})

        # DELETE order
        self.client.delete("{}/orders/1".format(
            self.base_url), headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(adm_token)})

        # Try to Change status again to to Cancelled
        response = self.client.put("{}/orders/1".format(
            self.base_url), json={
                "order_status": "Cancelled"
            }, headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(adm_token)})

        response_json = base_test_class.helper_functions.response_as_json(
            response)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response_json["message"],
            "Not allowed. This order is already 'Deleted'")

    # GET /menu

    def test_get_menu_when_no_items(self):
        """
            13. Test that users can access
            the menu when menu is empty
        """
        response = self.client.get("{}/menu".format(
            self.base_url), headers={
                "Content-Type": "application/json"})

        response_json = base_test_class.helper_functions.response_as_json(
            response)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response_json["message"], "No food items on the menu yet")

    def test_get_menu(self):
        """
            14. Test that users can get items on the menu
            without needing authorization
        """
        # Login admin
        adm_token = self.login_test_admin()
        # Make POST /menu request
        food_a = {
            "food_item_name": "Vegetable Curry",
            "food_item_price": 550,
            "food_item_img": "Curry"
        }
        food_b = {
            "food_item_name": "Meat Balls",
            "food_item_price": 1550,
            "food_item_img": "Meat Balls"

        }
        self.logged_in_admin_post_to_menu(food_a, adm_token)
        self.logged_in_admin_post_to_menu(food_b, adm_token)

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
            response_json["menu"][1]["food_item_name"], "Meat Balls")
        self.assertEqual(
            response_json["menu"][0]["food_item_name"], "Vegetable Curry")

    def test_post_menu(self):
        """
            15. Test that logged in admin can add
            items to the menu
        """
        # Login admin
        adm_token = self.login_test_admin()

        response = self.client.post("{}/menu".format(
            self.base_url), json={
                "food_item_name": "Assorted Nuts",
                "food_item_price": 1400,
                "food_item_img": "Nuts"}, headers={
                    "Authorization": "Bearer {}".format(adm_token)})

        response_json = base_test_class.helper_functions.response_as_json(
            response)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response_json["message"], "Food item added succesfully.")
        self.assertEqual(
            response_json["food"]["food_item_id"], 1)
        self.assertEqual(
            response_json["food"]["food_item_name"], "Assorted Nuts")

    def test_post_menu_cannot_duplicate(self):
        """
            16. Test that logged in admin cannot
            add duplicate items on the menu
        """
        # Login admin
        adm_token = self.login_test_admin()
        # Make first POST
        food_item = {"food_item_name": "Mangoes",
                     "food_item_price": 400,
                     "food_item_img": "Mangoes"
                    }
        self.logged_in_admin_post_to_menu(food_item, adm_token)

        # POST with same food item
        response = self.client.post("{}/menu".format(
            self.base_url), json=food_item, headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(adm_token)})

        response_json = base_test_class.helper_functions.response_as_json(
            response)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response_json["message"],
            "Error. 'food_item_name' 'Mangoes' is already in use")

    def test_admin_can_modify_items_on_menu(self):
        """
            17. Test that logged in admin can modify
            items on menu
        """
        # Login admin
        adm_token = self.login_test_admin()
        # Add item to menu
        self.logged_in_admin_post_to_menu(
            {"food_item_name": "Maembe Kubwa",
             "food_item_price": 2000,
             "food_item_img": "Maembe"}, adm_token)

        # Update order status to "Complete"
        response = self.client.put("{}/menu/1".format(
            self.base_url), json={
                "food_item_price": 1200
            }, headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(adm_token)})

        response_json = base_test_class.helper_functions.response_as_json(
            response)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response_json["message"], "Food item modified succesfully.")

    def test_admin_cannot_modify_items_on_menu_if_no_change(self):
        """
            18. Test that logged in admin cannot modify
            items on menu if request contains no change
        """
        # Login admin
        adm_token = self.login_test_admin()
        # Add item to menu

        food_item = {
            "food_item_name": "Maembe Kubwa",
            "food_item_price": 10,
            "food_item_img": "Maembe"
        }
        self.logged_in_admin_post_to_menu(food_item, adm_token)

        # Update order status to "Complete"
        response = self.client.put("{}/menu/1".format(
            self.base_url), json={
                "food_item_name": "Maembe Kubwa"
            }, headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(adm_token)})

        response_json = base_test_class.helper_functions.response_as_json(
            response)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response_json["message"], "Not updated. No change detected")

    def test_admin_can_delete_items_on_menu(self):
        """
            19. Test that logged in admin can delete
            items on menu
        """
        # Login admin
        adm_token = self.login_test_admin()
        # Add item to menu
        self.logged_in_admin_post_to_menu(
            {"food_item_name": "Flowerey Things",
             "food_item_price": 2000,
             "food_item_img": "Things"}, adm_token)

        # Update order status to "Complete"
        response = self.client.delete("{}/menu/1".format(
            self.base_url), headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(adm_token)})

        response_json = base_test_class.helper_functions.response_as_json(
            response)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response_json["message"], "Delete successful.")

    def test_admin_cannot_delete_completed_orders(self):
        """
            20. Test that logged in admin cannot delete
            completed orders
        """
        # Login admin
        adm_token = self.login_test_admin()
        # Add item to menu
        self.logged_in_admin_post_to_menu(
            {"food_item_name": "Flowerey Things",
             "food_item_price": 2000,
             "food_item_img": "Things"}, adm_token)

        # Register and login user
        token = self.login_test_user()
        # Make POST request
        self.logged_in_user_post_order({"food_item_id": 1,
                                        "quantity": 2}, token)
        # Update order status to "Complete"
        self.client.put("{}/orders/1".format(
            self.base_url), json={
                "order_status": "Complete"
            }, headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(adm_token)})
        # Send DELETE request
        response = self.client.delete("{}/orders/1".format(
            self.base_url), headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(adm_token)})

        response_json = base_test_class.helper_functions.response_as_json(
            response)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response_json["message"], "Not deleted. Status is 'Complete'. \
Status must be 'Cancelled' to delete")

    def test_admin_can_delete_cancelled_orders(self):
        """
            21. Test that logged in admin can delete
            cancelled orders
        """
        # Login admin
        adm_token = self.login_test_admin()
        # Add item to menu
        self.logged_in_admin_post_to_menu(
            {"food_item_name": "Flowerey Things",
             "food_item_price": 2000,
             "food_item_img": "Things"}, adm_token)

        # Register and login user
        token = self.login_test_user()
        # Make POST request
        self.logged_in_user_post_order({"food_item_id": 1,
                                        "quantity": 2}, token)
        # Update order status to "Complete"
        self.client.put("{}/orders/1".format(
            self.base_url), json={
                "order_status": "Cancelled"
            }, headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(adm_token)})
        # Send DELETE request
        response = self.client.delete("{}/orders/1".format(
            self.base_url), headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(adm_token)})

        response_json = base_test_class.helper_functions.response_as_json(
            response)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response_json["message"], "Delete successful.")

    def test_admin_cannot_delete_new_order(self):
        """
            22. Test that logged in admin cannot delete
            orders whose status is 'New'
        """
        # Login admin
        adm_token = self.login_test_admin()
        # Add item to menu
        self.logged_in_admin_post_to_menu(
            {"food_item_name": "Flowerey Things",
             "food_item_price": 2000,
             "food_item_img": "Things"}, adm_token)

        # Register and login user
        token = self.login_test_user()
        # Make POST request
        self.logged_in_user_post_order({"food_item_id": 1,
                                        "quantity": 2}, token)

        # Send DELETE request
        response = self.client.delete("{}/orders/1".format(
            self.base_url), headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(adm_token)})

        response_json = base_test_class.helper_functions.response_as_json(
            response)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response_json["message"], "Not deleted. Status is 'New'. \
Status must be 'Cancelled' to delete")
