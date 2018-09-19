"""
    Serve the api locally
"""
from api.v1.routes import APP

if __name__ == '__main__':
    APP.run(debug=True)
