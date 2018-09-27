"""
    Initialize flask app instance and configure
    as appropriate
"""

from flask import Flask

# local imports
from api.v2.config import CONFIGS
from api.v2.database import init_db

APP = Flask(__name__)
APP.config.from_object(CONFIGS['development_config'])

# Initialize db
db_url = CONFIGS["db_url"]
init_db(db_url)
