"""
    Serve the api locally
"""
from api.v1.routes import app

if __name__ == '__main__':
  app.run()
