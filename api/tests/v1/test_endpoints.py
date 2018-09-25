"""
    Tests for the API's endpoints.
"""

import unittest
import json

# local imports
from api.v1.views import APP
from api.v1.config import CONFIGS


def response_as_json(resp):
    """
        Helper function
        Loads response as json for easier inspection
    """
    resp_json = json.loads(resp.data.decode('utf-8'))
    return resp_json


class TestEndpoints(unittest.TestCase):
    """
        Class with all the tests for the API endpoints
    """
    def setUp(self):
        """
            Instantiate the API for testing and configure
            as appropriate
        """
        APP.config.from_object(CONFIGS['testing_config'])
        self.api = APP
        self.api_context = self.api.app_context()
        self.api_context.push()
        self.api_test_client = APP.test_client()

        # Base url common to all endpoints
        self.BASE_URL = '/api/v1'
        # Sample data for POST requests
        self.ORDER = {
            'item_name': 'Big Samosa',
            'item_price': 200,
            'quantity': 1
        }

        self.ORDER_2 = {
            'item_name': 'Pork Ribs',
            'item_price': 1080,
            'quantity': 1
        }

    def tearDown(self):
        """
            Remove the app context after testing
        """
        self.api_context.pop()
        self.api_test_client = None

    def test_fetch_all_orders_when_none_exist(self):
        """
            1. Test GET /orders - when no orders exist
        """
        response = self.api_test_client.get('{}/orders'.format(self.BASE_URL))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_as_json(
            response)['message'], 'No orders exist as yet')

    def test_make_new_order(self):
        """
            2. Test POST /orders - with proper data
        """
        response = self.api_test_client.post('{}/orders'.format(
            self.BASE_URL), json=self.ORDER, headers={
                'Content-Type': 'application/json'})

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_as_json(
            response)['order']['item_name'], self.ORDER['item_name'])
        self.assertEqual(response_as_json(
            response)['order']['order_id'], 1)
        self.assertEqual(response_as_json(
            response)['order']['quantity'], 1)
        self.assertEqual(response_as_json(
            response)['order']['total_order_cost'], 200)

    def test_make_similar_order(self):
        """
            3. Test POST /orders - when similar order already exists
        """
        response = self.api_test_client.post('{}/orders'.format(
            self.BASE_URL), json=self.ORDER, headers={
                'Content-Type': 'application/json'})

        self.assertEqual(response.status_code, 201)
        print(response_as_json(
            response))
        self.assertEqual(response_as_json(
            response)['order']['item_name'], self.ORDER['item_name'])
        self.assertEqual(response_as_json(
            response)['order']['order_id'], 1)
        self.assertEqual(response_as_json(
            response)['order']['quantity'], 2)
        self.assertEqual(response_as_json(
            response)['order']['total_order_cost'], 400)

    def test_make_second_order(self):
        """
            4. Test POST /orders - 2nd POST with proper data
        """
        response = self.api_test_client.post('{}/orders'.format(
            self.BASE_URL), json=self.ORDER_2, headers={
                'Content-Type': 'application/json'})

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_as_json(
            response)['order']['item_name'], self.ORDER_2['item_name'])
        self.assertEqual(response_as_json(
            response)['order']['order_id'], 2)
        self.assertEqual(response_as_json(
            response)['order']['quantity'], 1)
        self.assertEqual(response_as_json(
            response)['order']['item_price'], 1080)

    def test_make_order_with_some_data_missing(self):
        """
            5. Test POST /orders - with some data missing
        """
        response = self.api_test_client.post('{}/orders'.format(
            self.BASE_URL), json={'item_name': 'Watermelon'}, headers={
                'Content-Type': 'application/json'})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_as_json(
            response)['message'], 'Bad request. Missing required param')

    def test_make_order_with_some_data_as_empty_str(self):
        """
            6. Test POST /orders - with some data as None
        """
        response = self.api_test_client.post('{}/orders'.format(
            self.BASE_URL), json={
                'item_name': 'Watermelon', 'item_price': 200, 'quantity': ''
                }, headers={'Content-Type': 'application/json'})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_as_json(
            response)['message'], 'Bad request. Missing required param')

    def test_make_order_without_any_request_data(self):
        """
            7. Test POST /orders - without any data
        """
        response = self.api_test_client.post('{}/orders'.format(
            self.BASE_URL), json={}, headers={
                'Content-Type': 'application/json'})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_as_json(
            response)['message'], 'Bad request. Missing required param')

    def test_make_order_with_non_json_data(self):
        """
            8. Test POST /orders - with non-json data in request
        """
        response = self.api_test_client.post('{}/orders'.format(
            self.BASE_URL), data='item_name=Guacamole&item_price=200')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_as_json(
            response)['message'],
                         'Bad request. Request data must be in json format')

    def test_retrieve_all_orders(self):
        """
            9. Test GET /orders - when one or several orders exist
            After successful POSTs in Tests 1, 2, 3 above
        """
        response = self.api_test_client.get('{}/orders'.format(self.BASE_URL))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_as_json(
            response)['orders'][0]['item_name'], self.ORDER['item_name'])
        self.assertEqual(response_as_json(
            response)['orders'][1]['item_name'], self.ORDER_2['item_name'])
        self.assertEqual(len(response_as_json(response)['orders']), 2)

    def test_retrieve_by_id(self):
        """
            10. Test GET /orders/id - when order with given id exists
        """
        response = self.api_test_client.get(
            '{}/orders/1'.format(self.BASE_URL))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_as_json(
            response)['item_name'], self.ORDER['item_name'])

    def test_fetch_specific_order_when_does_not_exist(self):
        """
            11. Test GET /orders/id - when order with given id does not exist
        """
        response = self.api_test_client.get(
            '{}/orders/100'.format(self.BASE_URL))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            'Order with id 100 not found', response_as_json(
                response)['message'])

    def test_update_order(self):
        """
            12. Test PUT /orders/id - when order with given id exists
            and status is valid
        """
        response = self.api_test_client.put('{}/orders/1'.format(
            self.BASE_URL), json={'order_status': 'accepted'})

        self.assertEqual(response.status_code, 201)
        self.assertTrue(
            response_as_json(response)['order']['status_updated_on'])
        self.assertEqual(
            response_as_json(response)['order']['order_status'], 'accepted')

    def test_update_order_with_invalid_status(self):
        """
            13. Test PUT /orders/id - when order with given id exists
            but status is not valid
        """
        response = self.api_test_client.put('{}/orders/1'.format(
            self.BASE_URL), json={'order_status': 'kenya'})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_as_json(
            response)['message'],
                         'Bad request. Invalid order status')

    def test_change_order_status_when_order_does_not_exist(self):
        """
            14. Test PUT /orders/id - when order with given id does not exist
        """
        response = self.api_test_client.put('{}/orders/1000'.format(
            self.BASE_URL), json={'order_status': 'accepted'})

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_as_json(
            response)['message'],
                         'Order with id 1000 not found')

    def test_update_order_with_no_status(self):
        """
            15. Test PUT /orders/id - when order with given id exists
            but status has not been provided
        """
        response = self.api_test_client.put('{}/orders/1'.format(
            self.BASE_URL), json={})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_as_json(
            response)['message'], 'Bad request. Missing required param')

    def test_update_order_with_non_json_data(self):
        """
            16. Test PUT /orders/id - when order with given id exists
            but status is provided in non-json format
        """
        response = self.api_test_client.put('{}/orders/1'.format(
            self.BASE_URL), data='order_status=rejected')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_as_json(
            response)['message'],
                         'Bad request. Request data must be in json format')


if __name__ == '__main__':
    unittest.main()
