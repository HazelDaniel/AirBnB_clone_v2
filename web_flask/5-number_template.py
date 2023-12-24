#!/usr/bin/python3
"""a module that starts a flask web application on 0.0.0.0 port 5000"""
from flask import Flask, render_template
from markupsafe import escape

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index():
    """a route handler for the root route"""
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb_route():
    """a route handler for the /hbnb"""
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c_route(text):
    """a route handler for the /c/[slug]"""
    return f"C {escape(text.replace('_', ' '))}"


@app.route('/python/<text>', strict_slashes=False)
@app.route('/python/', defaults={'text': None}, strict_slashes=False)
def py_route(text):
    """a route handler for the /python/[slug]"""
    if text:
        return f"Python {escape(text.replace('_', ' '))}"
    return "Python is cool"


@app.route('/number/<int:n>', strict_slashes=False)
def num_route(n):
    """a route handler for the /number/[slug]"""
    return f"{escape(n)} is a number"


@app.route('/number_template/<int:n>', strict_slashes=False)
def num_template_route(n):
    """a route handler for the /number_template/[slug]"""
    return render_template('5-number.html', n=n)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
