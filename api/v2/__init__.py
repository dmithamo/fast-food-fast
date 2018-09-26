"""
    Initialize flask app instance and configure
    as appropriate
"""

from flask import Flask

# local imports
from api.v2.config import CONFIGS

APP = Flask(__name__)
APP.config.from_object(CONFIGS['development_config'])
