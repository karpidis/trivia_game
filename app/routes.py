from flask import Flask
"""
This module defines the routes for the Flask web application.

The routes.py file is essential in a Flask application as it defines the URL routes and their corresponding request handlers. 
In this example, the root URL ('/') is mapped to the hello_world function, which returns a simple 'Hello, World!' message. 
This file is crucial for organizing and managing the different endpoints of the web application.
"""


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)
