#!/usr/bin/python3
"""a module that starts a flask web application on 0.0.0.0 port 5000"""
from flask import Flask
from markupsafe import escape

app = Flask(__name__)


@app.route('/c/<text>', strict_slashes=False)
def hbnb_route(text):
    """a route handler for the /c/[slug]"""
    return f"C {escape(text.replace('_', ' '))}"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
