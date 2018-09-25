"""
    Tests for the API's endpoints.
"""

import unittest
import json

# local imports
from api.v1.views import APP
from api.v1.config import CONFIGS

# Base url common to all endpoints
BASE_URL = '/api/v1'
# Sample data for POST requests
ORDER = {
    'item_name' : 'Big Samosa',
    'item_price' : 200,
    'quantity' : 1
}

ORDER_2 = {
    'item_name' : 'Pork Ribs',
    'item_price' : 1080,
    'quantity' : 1
}

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

    def tearDown(self):
        """
            Remove the app context after testing
        """
        self.api_context.pop()

    def test_a_get_orders_with_no_orders(self):
        """
            1. Test GET /orders - when no orders exist
        """
        response = self.api_test_client.get('{}/orders'.format(BASE_URL))
        self.assertEqual(response.status_code, 404)
        self.assertIn(
            'No orders exist as yet', str(response.data))

    def test_b_post_order(self):
        """
            2. Test POST /orders - with proper data
        """
        response = self.api_test_client.post('{}/orders'.format(
            BASE_URL), json=ORDER, headers={'Content-Type':'application/json'})

        self.assertEqual(response.status_code, 201)
        self.assertIn('Big Samosa', str(response.data))
        self.assertEqual(response_as_json(response)['order_id'], 1)
        self.assertEqual(response_as_json(response)['quantity'], 1)
        self.assertEqual(response_as_json(response)['total_order_cost'], 200)

    def test_c_post_when_similar_order_exists(self):
        """
            3. Test POST /orders - when similar order already exists
        """
        response = self.api_test_client.post('{}/orders'.format(
            BASE_URL), json=ORDER, headers={'Content-Type':'application/json'})

        self.assertEqual(response.status_code, 201)
        self.assertIn('Big Samosa', str(response.data))
        self.assertEqual(response_as_json(response)['order_id'], 1)
        self.assertEqual(response_as_json(response)['quantity'], 2)
        self.assertEqual(response_as_json(response)['total_order_cost'], 400)

    def test_d_post_another_order(self):
        """
            4. Test POST /orders - 2nd POST with proper data
        """
        response = self.api_test_client.post('{}/orders'.format(
            BASE_URL), json=ORDER_2, headers={'Content-Type':'application/json'})

        self.assertEqual(response.status_code, 201)
        self.assertIn('Pork Ribs', str(response.data))
        self.assertEqual(response_as_json(response)['order_id'], 2)
        self.assertEqual(response_as_json(response)['quantity'], 1)
        self.assertEqual(response_as_json(response)['item_price'], 1080)

    def test_e_post_with_some_data_missing(self):
        """
            5. Test POST /orders - with some data missing
        """
        response = self.api_test_client.post('{}/orders'.format(
            BASE_URL), json={'item_name':'Watermelon'}, headers={'Content-Type':'application/json'})

        self.assertEqual(response.status_code, 400)
        self.assertIn('Bad request. Missing', str(response.data))

    def test_f_post_with_some_data_as_none(self):
        """
            6. Test POST /orders - with some data as None
        """
        response = self.api_test_client.post('{}/orders'.format(
            BASE_URL), json={
                'item_name':'Watermelon', 'item_price':200, 'quantity':''}, headers={
                    'Content-Type':'application/json'})

        self.assertEqual(response.status_code, 400)
        self.assertIn('Bad request. Missing', str(response.data))

    def test_g_post_order_without_any_data(self):
        """
            7. Test POST /orders - without any data
        """
        response = self.api_test_client.post('{}/orders'.format(
            BASE_URL), json={}, headers={'Content-Type':'application/json'})

        self.assertEqual(response.status_code, 400)
        self.assertIn('Bad request. Missing', str(response.data))

    def test_h_post_with_non_json_data(self):
        """
            8. Test POST /orders - with non-json data in request
        """
        response = self.api_test_client.post('{}/orders'.format(
            BASE_URL), data='item_name=Guacamole&item_price=200')

        self.assertEqual(response.status_code, 400)
        self.assertIn(
            'Bad request. Request data must be in json', str(response.data))

    def test_i_get_orders(self):
        """
            9. Test GET /orders - when one or several orders exist
            After successful POSTs in Tests 1, 2, 3 above
        """
        response = self.api_test_client.get('{}/orders'.format(BASE_URL))

        # self.assertEqual(response.status_code, 200)
        self.assertIn(
            'Big Samosa', str(response.data))
        self.assertIn(
            'Pork Ribs', str(response.data))
        self.assertEqual(len(response_as_json(response)['orders']), 2)

    def test_j_get_by_id_when_order_exists(self):
        """
            10. Test GET /orders/id - when order with given id exists
        """
        response = self.api_test_client.get('{}/orders/1'.format(BASE_URL))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_as_json(response)['item_name'], 'Big Samosa')

    def test_k_get_by_id_when_order_does_not_exist(self):
        """
            11. Test GET /orders/id - when order with given id does not exist
        """
        response = self.api_test_client.get('{}/orders/100'.format(BASE_URL))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            'Order with id 100 not found', response_as_json(response)['message'])

    def test_l_put_order(self):
        """
            12. Test PUT /orders/id - when order with given id exists
            and status is valid
        """
        response = self.api_test_client.put('{}/orders/1'.format(
            BASE_URL), json={'order_status':'accepted'})

        self.assertEqual(response.status_code, 201)
        self.assertIn(
            'status_updated_on', str(response.data))
        self.assertEqual(
            response_as_json(response)['order_status'], 'accepted')

    def test_m_put_order_with_invalid_status(self):
        """
            13. Test PUT /orders/id - when order with given id exists
            but status is not valid
        """
        response = self.api_test_client.put('{}/orders/1'.format(
            BASE_URL), json={'order_status':'kenya'})

        self.assertEqual(response.status_code, 400)
        self.assertIn(
            'Bad request. Invalid order status', str(response.data))

    def test_n_put_order_when_order_does_not_exist(self):
        """
            14. Test PUT /orders/id - when order with given id does not exist
        """
        response = self.api_test_client.put('{}/orders/1000'.format(
            BASE_URL), json={'order_status':'accepted'})

        self.assertEqual(response.status_code, 404)
        self.assertIn(
            'Order with id 1000 not found', str(response.data))

    def test_o_put_order_with_no_status(self):
        """
            15. Test PUT /orders/id - when order with given id exists
            but status has not been provided
        """
        response = self.api_test_client.put('{}/orders/1'.format(
            BASE_URL), json={})

        self.assertEqual(response.status_code, 400)
        self.assertIn(
            'Bad request. Missing required param', str(response.data))

    def test_p_put_order_with_non_json_data(self):
        """
            16. Test PUT /orders/id - when order with given id exists
            but status is provided in non-json format
        """
        response = self.api_test_client.put('{}/orders/1'.format(
            BASE_URL), data='order_status=rejected')

        self.assertEqual(response.status_code, 400)
        self.assertIn(
            'Bad request. Request data must be in json', str(response.data))

if __name__ == '__main__':
    unittest.main()
