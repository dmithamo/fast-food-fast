"""
    Serve entry page of app using Flask
"""

from flask import Flask, url_for



APP = Flask(__name__)

@APP.route('/')
def serve_homepage():
    """
        Render homepage on visiting root url
    """
    return url_for("menu.html")


if __name__ == '__main__':
    APP.run(debug=True)