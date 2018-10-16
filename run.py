"""
    Serve entry page of app using Flask
"""

from flask import Flask, render_template
from flask_cors import CORS



APP = Flask(__name__)

CORS(APP)

@APP.route('/')
def serve_homepage():
    """
        Render homepage on visiting root url
    """
    return render_template("menu.html")

@APP.route('/register')
def serve_register_page():
    """
        Render resgister page on visiting register url
    """
    return render_template("auth/register.html")

@APP.route('/login')
def serve_admin_login_page():
    """
        Render admin_login page on visiting login url
    """
    return render_template("auth/login.html")

@APP.route('/admin_login')
def serve_login_page():
    """
        Render login page on visiting login url
    """
    return render_template("login.html")

@APP.route('/user/place_order')
def serve_place_order_page():
    """
        Render login page on visiting login url
    """
    return render_template("users/place_order.html")


if __name__ == '__main__':
    APP.run(debug=True)