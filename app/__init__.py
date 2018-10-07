#!/usr/bin/env python
# encoding: utf-8

'''
@author:     Bhushan Barhate
@contact:    bhushan2901@yahoo.co.in
'''

__all__ = []
__version__ = 1.0
__author__ = 'Bhushan Barhate'
__date__ = '2018-10-03'
__updated__ = '2018-10-07'

import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import functools
from flask import jsonify

""" create a SQLAlchemy object to be used through out the project """
db = SQLAlchemy()


def create_app(config_name):
    """ Create an application instance, initialize the DB, and return app object"""
    app = Flask(__name__)

    # apply configuration
    cfg = os.path.join(os.getcwd(), 'config', config_name + '.py')
    app.config.from_pyfile(cfg)

    # initialize extensions
    db.init_app(app)

    # register blueprints
    from .api_v1 import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    return app


def json(f):
    """Generate a JSON response from a database model or a Python
    dictionary."""
    # invoke the wrapped function
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        rv = f(*args, **kwargs)

        # the wrapped function can return the dictionary alone,
        # or can also include a status code and/or headers.
        # here we separate all these items
        status = None
        headers = None
        if isinstance(rv, tuple):
            rv, status, headers = rv + (None,) * (3 - len(rv))
        if isinstance(status, (dict, list)):
            headers, status = status, None

        # if the response was a database model, then convert it to a
        # dictionary

        if not isinstance(rv, dict) and not isinstance(rv, list):
            if hasattr(rv, "export_data"):
                rv = rv.export_data()

        if isinstance(rv, list):
            rv = [i.export_data() for i in rv]

        # generate the JSON response
        rv = jsonify(rv)
        if status is not None:
            rv.status_code = status
        if headers is not None:
            rv.headers.extend(headers)
        return rv
    return wrapped


class ValidationError(ValueError):
    """ Validation error for any type of user validation currently blank"""

    """ set response code for the validation"""
    response_code = 400
    error = "bad request"
    pass
