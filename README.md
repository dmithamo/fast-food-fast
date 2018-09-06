# Fast-Food-Fast

This repo is a build out of the UI templates and API backend for an online food ordering platform.

## UI Features

The UI provides elements for :

1. User registration and login.

2. Page where users can place orders and review their order history.

3. Admin management portal, where admin can manage user orders, and modify list of items on offer.

UI preview : [dmithamo/fast-food-fast](https://dmithamo.github.io/fast-food-fast/index.html).

Code for UI tracked in the [gh-pages](https://github.com/dmithamo/fast-food-fast/tree/gh-pages) branch.

## API Features

The API contains the endpoints below:
  
| Endpoint                  | What it Does                     | Git Branch                             |
| :--------------------     | :-----------------------         | :--------------------------------      |
| `POST /orders`            | Place an order                   | [ft-api-post-order-160244252](https://github.com/dmithamo/fast-food-fast/tree/ft-api-post-order-160244252)                           |
| `GET /orders`             | Fetch all orders                 | [ft-api-get-orders-160244330](https://github.com/dmithamo/fast-food-fast/tree/ft-api-get-orders-160244330)                           |
| `GET /orders/id`          | Fetch specific order             | [ft-api-get-specific-order-160244412](https://github.com/dmithamo/fast-food-fast/tree/ft-api-get-specific-order-160244412)                   |
| `PUT /orders/id`          | Update order status              | [ft-api-update-order-status-160244454](https://github.com/dmithamo/fast-food-fast/tree/ft-api-update-order-status-160244454)                  |

## Manual testing of the API

To manually test these endpoints, configure and run the server as below:

1. `git checkout <branch-with-desired-endpoint>` [or `git checkout api-v1` for all the endpoints]

2. Create and activate a [Virtual Environment](https://virtualenv.pypa.io/en/stable/).

3. Run `pip install -r requirements.txt` to install dependencies

4. Run `export FLASK_APP=run.py`

5. Run `flask run` to start the server

Test the endpoints at `localhost:5000/fastfoodfast/api/v1/`.

Recommended testing tool : [Postman](https://www.getpostman.com/).

## Pytest-ing the API

To run the tests written for the API's endpoints:

1. Proceed as in steps `1 to 4` above.

2. Run `pytest` (or `pytest -v` for verbose output)

[Pytest documentation](http://pytest-flask.readthedocs.io/en/latest/).
