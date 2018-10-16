"""
    Serve entry page of app using Flask
"""

from flask import Flask, render_template



APP = Flask(__name__)

@APP.route('/')
def serve_homepage():
    """
        Render homepage on visiting root url
    """
    return render_template("menu.html")


if __name__ == '__main__':
    APP.run(debug=True)