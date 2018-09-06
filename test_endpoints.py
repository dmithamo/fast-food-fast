"""
    Tests for the API's endpoints.
"""

import json
import pytest
import config
from api.api import API

# Base url common to all endpoints
BASE_URL = '/fastfoodfast/api/v1'
# Sample data for POST requests
ORDER = {
    'name' : 'Big Samosa',
    'price' : 'Ksh. 200'
}

ORDER_2 = {
    'name' : 'Pork Ribs',
    'price' : 'Ksh. 1080'
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
    API.config.from_object(config.TestingConfig)
    # Yield test_client
    api_test_client = API.test_client()
    yield api_test_client


def test_get_orders_endpoint(api_test_client):
    """
        1. Test GET /orders - when no orders exist
    """
    response = api_test_client.get('{}/orders'.format(BASE_URL))
    assert response.status_code == 200
    assert 'No orders as yet exist' in str(response.data)

def test_post_order_endpoint(api_test_client):
    """
        2. Test POST /orders - with proper data
    """
    response = api_test_client.post('{}/orders?name={}&price={}'.format(
        BASE_URL, ORDER['name'], ORDER['price']
    ))
    assert response.status_code == 201
    assert 'Big Samosa' in str(response.data)
    assert 'ordered_on' in str(response.data)

def test_post_order_endpoint_2(api_test_client):
    """
        3. Test POST /orders - when similar order already exists
    """
    response = api_test_client.post('{}/orders?name={}&price={}'.format(
        BASE_URL, ORDER['name'], ORDER['price']
    ))
    assert response.status_code == 201
    assert 'Big Samosa' in str(response.data)
    assert response_as_json(response)['quantity'] == 2
    assert response_as_json(response)['item_id'] == 1

def test_post_order_endpoint_3(api_test_client):
    """
        4. Test POST /orders - 2nd POST with proper data
    """
    response = api_test_client.post('{}/orders?name={}&price={}'.format(
        BASE_URL, ORDER_2['name'], ORDER_2['price']
    ))
    assert response.status_code == 201
    assert 'Pork Ribs' in str(response.data)
    assert response_as_json(response)['item_price'] == 'Ksh. 1080'
    assert response_as_json(response)['item_id'] == 2

def test_post_order_endpoint_4(api_test_client):
    """
        5. Test POST /orders - with some data missing
    """
    response = api_test_client.post('{}/orders?name={}&price='.format(
        BASE_URL, ORDER['name']
    ))
    assert response.status_code == 400
    assert 'Bad request' in str(response.data)

def test_post_order_endpoint_5(api_test_client):
    """
        6. Test POST /orders - without any data
    """
    response = api_test_client.post('{}/orders'.format(
        BASE_URL
    ))
    assert response.status_code == 400
    assert 'Bad request' in str(response.data)

def test_get_orders_endpoint_2(api_test_client):
    """
        7. Test GET /orders - when one or several orders exist
        Achieved after successful POSTs in Tests 1, 2, 3 above
    """
    response = api_test_client.get('{}/orders'.format(BASE_URL))
    assert response.status_code == 200
    assert 'orders' in str(response.data)
    assert 'Big Samosa' and 'Pork Ribs' in str(response.data)
    assert len(response_as_json(response)['orders']) == 2
    assert isinstance(response_as_json(response)['orders'], list)

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
    assert response_as_json(response)['message'] == 'Error. Order not found'

def test_update_order_status_endpoint(api_test_client):
    """
        10. Test PUT /orders/id - when order with given id exists
        and status is valid
    """
    response = api_test_client.put('{}/orders/1?status=confirmed'.format(
        BASE_URL
        ))
    assert response.status_code == 201
    assert response_as_json(response)['status'] == 'confirmed'
    assert 'status_updated_on' in str(response.data)

def test_update_order_status_endpoint_2(api_test_client):
    """
        11. Test PUT /orders/id - when order with given id exists
        but status is not valid
    """
    response = api_test_client.put('{}/orders/1?status=kenya'.format(
        BASE_URL
        ))
    assert response.status_code == 400
    assert 'Bad request. Provide a valid order status.' in str(response.data)

def test_update_order_status_endpoint_3(api_test_client):
    """
        12. Test PUT /orders/id - when order with given id does not exist
    """
    response = api_test_client.put('{}/orders/100?status=rejected'.format(
        BASE_URL
        ))
    assert response.status_code == 404
    assert 'Order not found' in str(response.data)
