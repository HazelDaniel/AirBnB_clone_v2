#!/usr/bin/python3
# a module that starts a flask web application on 0.0.0.0 port 5000
from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index():
    """the index page for the root route"""
    return "Hello HBNB!"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
