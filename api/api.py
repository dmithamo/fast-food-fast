"""
    Initialize a Flask instance and configure as appropriate,
"""


from flask import Flask
import config

API = Flask(__name__)
API.config.from_object(config.DevelopmentConfig)
