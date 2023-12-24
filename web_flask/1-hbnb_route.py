#!/usr/bin/python3
"""a module that starts a flask web application on 0.0.0.0 port 5000"""
from flask import Flask

app = Flask(__name__)


@app.route('/hbnb', strict_slashes=False)
def hbnb_route():
    """a route handler for the /hbnb"""
    return "HBNB"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
