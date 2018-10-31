"""
    Serve entry page of app using Flask
"""

from flask import Flask, render_template
from flask_cors import CORS



APP = Flask(__name__)

CORS(APP)

@APP.route('/error_page')
def serve_errorpage():
    """
        Render custom error page
    """
    return render_template("error_page.html")

@APP.route('/')
@APP.route('/menu.html')
def serve_homepage():
    """
        Render homepage on visiting root url
    """
    return render_template("menu.html")

@APP.route('/auth/register', methods=['GET','POST'])
@APP.route('/auth/register.html', methods=['GET','POST'])
def serve_register_page():
    """
        Render resgister page on visiting register url
    """
    return render_template("auth/register.html")

@APP.route('/auth/login', methods=['GET','POST'])
@APP.route('/auth/login.html', methods=['GET','POST'])
def serve_admin_login_page():
    """
        Render login page on visiting login url
    """
    return render_template("auth/login.html")

@APP.route('/admin_login', methods=['GET','POST'])
@APP.route('/admin_login.html', methods=['GET','POST'])
@APP.route('/login', methods=['GET','POST'])
def serve_login_page():
    """
        Render admin_login page on visiting admin_login url
    """
    return render_template("admin_login.html")

@APP.route('/orders')
@APP.route('/orders.html')
def serve_admin_orders_history_page():
    """
        Render orders page on successful admin login
    """
    return render_template("orders.html")

@APP.route('/adm_menu')
@APP.route('/adm_menu.html')
def serve_admin_menu_page():
    """
        Render admin menu page on successful admin login
    """
    return render_template("adm_menu.html")

@APP.route('/users/place_order')
@APP.route('/users/place_order.html')
def serve_user_place_order_page():
    """
        Render login page on visiting login url
    """
    return render_template("users/place_order.html")

@APP.route('/users/view_orders')
@APP.route('/users/view_orders.html')
def serve_user_order_history_page():
    """
        Render user order history
    """
    return render_template("users/view_orders.html")


if __name__ == '__main__':
    APP.run(debug=True)