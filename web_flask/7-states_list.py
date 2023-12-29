#!/usr/bin/python3
"""a module that starts a flask web application on 0.0.0.0 port 5000"""
from flask import Flask, render_template
from markupsafe import escape
import os
import subprocess

current_directory = os.getenv("PWD")
storage = None
executable_path = f"{current_directory}/dump_fix.sh"
storage_type = os.getenv("HBNB_TYPE_STORAGE")
app = Flask(__name__)
subprocess.run(['bash', 'dump_fix.sh', '7-dump.sql'])
if current_directory:
    import sys
    current_directory = current_directory.split('/')
    current_directory = current_directory[:-1]
    current_directory = '/'.join(current_directory)
    sys.path.append(current_directory)
    from models import storage

if storage:
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

    @app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
    def num_odd_even(n):
        """a route handler for the /number_odd_or_even/[slug]"""
        return render_template('6-number_odd_or_even.html', n=n)

    @app.route('/states_list')
    def handle_states_list():
        """this is the route handler for the /states_list endpoint"""
        all_states = storage.all('State')
        all_states = sorted(all_states.items(), key=lambda x: x[1].name)
        return render_template('7-states_list.html', states=all_states)

    def teardown_requests(exception=None):
        """this is the teardown function to be executed in the"""
        storage.close()

    app.teardown_appcontext(teardown_requests)

    if __name__ == "__main__":
        app.run(host='0.0.0.0', port=5000, debug=True)
