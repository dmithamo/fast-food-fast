"""
    Tests for the API's endpoints.
"""

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

@pytest.fixture
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

def test_post_endpoint(api_test_client):
    """
        1. Test POST /orders - with proper data
    """
    response = api_test_client.post('{}/orders?name={}&price={}'.format(
        BASE_URL, ORDER['name'], ORDER['price']
    ))
    assert response.status_code == 201
    assert 'ordered_on' in str(response.data)

def test_post_endpoint_2(api_test_client):
    """
        2. Test POST /orders - with some data missing
    """
    response = api_test_client.post('{}/orders?name={}&price='.format(
        BASE_URL, ORDER['name']
    ))
    assert response.status_code == 400
    assert 'Bad request' in str(response.data)

def test_post_endpoint_3(api_test_client):
    """
        3. Test POST /orders - without any data
    """
    response = api_test_client.post('{}/orders'.format(
        BASE_URL
    ))
    assert response.status_code == 400
    assert 'Bad request' in str(response.data)
