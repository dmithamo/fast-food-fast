# Fast-Food-Fast

This repo is a build out of the UI templates and API backend for an online food ordering platform.

## Continous Integration Badges

[![Build Status](https://travis-ci.org/dmithamo/fast-food-fast.svg?branch=develop)](https://travis-ci.org/dmithamo/fast-food-fast) [![Coverage Status](https://coveralls.io/repos/github/dmithamo/fast-food-fast/badge.svg?branch=develop)](https://coveralls.io/github/dmithamo/fast-food-fast?branch=develop) [![Maintainability](https://api.codeclimate.com/v1/badges/8450eb14df4a1833c544/maintainability)](https://codeclimate.com/github/dmithamo/fast-food-fast/maintainability)

## UI Features

The UI [(See dmithamo/fast-food-fast)](https://dmithamo.github.io/fast-food-fast/index.html) provides elements for :

1. User registration and login.

2. Page where users can place orders and review their order history.

3. Admin management portal, where admin can manage user orders, and modify list of items on offer.

## API Features

The API contains the endpoints below:
  
| Endpoint                  | What it Does                     | Comment                            |
| :--------------------     | :-----------------------         | :--------------------------------  |
| `POST /auth/signup`       | Signup a user                    |                                    |
| `POST /auth/login`        | Login a user                     |                                    |
| `POST /users/orders`      | Place an order                   | Needs Auth                         |
| `GET /users/orders`       | Fetch all user orders            | Needs Auth                         |
| `GET /menu`               | Fetch the menu                   |                                    |
| `PUT /menu/id`            | Update a food item on the menu   | Needs Auth - Admin Only Access     |
| `DELETE /menu`            | Remove a food item from the menu | Needs Auth - Admin Only Access     |
| `POST /menu`              | Add food item to the menu        | Needs Auth - Admin Only Access     |
| `GET /orders`             | Fetch all orders                 | Needs Auth - Admin Only Access     |
| `GET /orders/id`          | Fetch a single order             | Needs Auth - Admin Only Access     |
| `PUT /orders/id`          | Update order status              | Needs Auth - Admin Only Access     |
| `DELETE /orders/id`       | Delete an order                  | Needs Auth - Admin Only Access     |

## Manual testing of the API

To manually test these endpoints, configure and run the server as below:

1. `git checkout develop` for all the endpoints

2. Create and activate a [Virtual Environment](https://virtualenv.pypa.io/en/stable/).

3. Run `pip install -r requirements.txt` to install dependencies

4. Run `export FLASK_APP=run.py`

5. Run `export SECRET_KEY="a-secret-key"` 

6. Run `flask run` to start the server

Test the endpoints at `localhost:5000/api/v2`.

The API is hosted on [Heroku](https://dmithamo-fast-food-fast-api.herokuapp.com/).
To test from the Heroku server, send requests to [https://dmithamo-fast-food-fast-api.herokuapp.com/api/v2](https://dmithamo-fast-food-fast-api.herokuapp.com/api/v2)

[Postman](https://www.getpostman.com/) is the recommended testing tool.

## Pytest-ing the API

To run the tests written for the API's endpoints:

1. Proceed as in steps `1 to 3` above, checking out the `develop` branch.

2. Run `pytest` (or `pytest -v` for verbose output)

[Pytest documentation](http://pytest-flask.readthedocs.io/en/latest/).

### Languages

1. `Python 3.6.5`
