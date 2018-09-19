"""
    Tests for the API's endpoints.
"""

import json
import pytest

# local imports
from api.v1.views import APP
from api.v1.config import TestingConfig

# Base url common to all endpoints
BASE_URL = '/fastfoodfast/api/v1'
# Sample data for POST requests
ORDER = {
    'item_name' : 'Big Samosa',
    'item_price' : 'Ksh. 200'
}

ORDER_2 = {
    'item_name' : 'Pork Ribs',
    'item_price' : 'Ksh. 1080'
}

def response_as_json(resp):
    """
        Helper function
        Loads response as json for easier inspection
    """
    resp_json = json.loads(resp.data.decode('utf-8'))
    return resp_json

@pytest.fixture(scope='function')
def api_test_client():
    """
        Initialize a standard testing fixture on which all tests
        will be executed
    """
    # Configure api instance for testing
    APP.config.from_object(TestingConfig)
    # Yield test_client
    api_test_client = APP.test_client()
    yield api_test_client


def test_get_orders_endpoint(api_test_client):
    """
        1. Test GET /orders - when no orders exist
    """
    response = api_test_client.get('{}/orders'.format(BASE_URL))
    assert response.status_code == 404
    assert response_as_json(response)['message'] == 'No orders exist as yet'

def test_post_order_endpoint(api_test_client):
    """
        2. Test POST /orders - with proper data
    """
    response = api_test_client.post('{}/orders'.format(
        BASE_URL), json=ORDER, headers={'Content-Type':'application/json'})

    assert response.status_code == 201
    assert response_as_json(response)['item_name'] == 'Big Samosa'
    assert response_as_json(response)['item_price'] == 'Ksh. 200'

def test_post_order_endpoint_2(api_test_client):
    """
        3. Test POST /orders - when similar order already exists
    """
    response = api_test_client.post('{}/orders'.format(
        BASE_URL), json=ORDER, headers={'Content-Type':'application/json'})

    assert response.status_code == 201
    assert 'Big Samosa' in str(response.data)
    assert response_as_json(response)['quantity'] == 2
    assert response_as_json(response)['order_id'] == 1

def test_post_order_endpoint_3(api_test_client):
    """
        4. Test POST /orders - 2nd POST with proper data
    """
    response = api_test_client.post('{}/orders'.format(
        BASE_URL), json=ORDER_2, headers={'Content-Type':'application/json'})

    assert response.status_code == 201
    assert 'Pork Ribs' in str(response.data)
    assert response_as_json(response)['item_price'] == 'Ksh. 1080'
    assert response_as_json(response)['order_id'] == 2

def test_post_order_endpoint_4(api_test_client):
    """
        5. Test POST /orders - with some data missing
    """
    response = api_test_client.post('{}/orders'.format(
        BASE_URL), json={'item_name':'Watermelon'}, headers={'Content-Type':'application/json'})

    assert response.status_code == 400
    assert 'Bad request' in str(response.data)

def test_post_order_endpoint_5(api_test_client):
    """
        6. Test POST /orders - without any data
    """
    response = api_test_client.post('{}/orders'.format(
        BASE_URL), json={}, headers={'Content-Type':'application/json'})

    assert response.status_code == 400
    assert 'Bad request' in str(response.data)

def test_get_orders_endpoint_2(api_test_client):
    """
        7. Test GET /orders - when one or several orders exist
        Achieved after successful POSTs in Tests 1, 2, 3 above
    """
    response = api_test_client.get('{}/orders'.format(BASE_URL))
    assert response.status_code == 200
    assert 'Big Samosa' and 'Pork Ribs' in str(response.data)
    assert response_as_json(response)['orders'] is not None

def test_get_specific_order_endpoint(api_test_client):
    """
        8. Test GET /orders/id - when order with given id exists
    """
    response = api_test_client.get('{}/orders/1'.format(BASE_URL))
    assert response.status_code == 200
    assert response_as_json(response)['item_name'] == 'Big Samosa'

def test_get_specific_order_endpoint_2(api_test_client):
    """
        9. Test GET /orders/id - when order with given id does not exist
    """
    response = api_test_client.get('{}/orders/100'.format(BASE_URL))
    assert response.status_code == 404
    assert response_as_json(response)['message'] == 'Order with id 100 not found'

def test_update_order_status_endpoint(api_test_client):
    """
        10. Test PUT /orders/id - when order with given id exists
        and status is valid
    """
    response = api_test_client.put('{}/orders/1'.format(
        BASE_URL), json={'order_status':'confirmed'})

    assert response.status_code == 201
    assert response_as_json(response)['order_status'] == 'confirmed'
    assert 'status_updated_on' in str(response.data)

def test_update_order_status_endpoint_2(api_test_client):
    """
        11. Test PUT /orders/id - when order with given id exists
        but status is not valid
    """
    response = api_test_client.put('{}/orders/1'.format(
        BASE_URL), json={'order_status':'kenya'})

    assert response.status_code == 400
    assert response_as_json(response)['message'] == 'Bad request. Invalid order status'

def test_update_order_status_endpoint_3(api_test_client):
    """
        12. Test PUT /orders/id - when order with given id does not exist
    """
    response = api_test_client.put('{}/orders/1000'.format(
        BASE_URL), json={'order_status':'confirmed'})

    assert response.status_code == 404
    assert response_as_json(response)['message'] == 'Order with id 1000 not found'
