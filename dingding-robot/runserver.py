"""
This script runs the dingding_robot application using a development server.
"""

from os import environ
from dingding_robot import app,config
#app.config.from_object("config")

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', '0.0.0.0')
    try:
        PORT = int(environ.get('SERVER_PORT', '80'))
    except ValueError:
        PORT = 5000
    app.run(HOST, PORT,debug = True)
