"""
    Serve the api locally
"""
from api.v2.views import APP


if __name__ == '__main__':
    APP.run(debug=True)
