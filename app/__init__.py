#!/usr/bin/env python
# encoding: utf-8

'''
@author:     Bhushan Barhate
@contact:    bhushan2901@yahoo.co.in
'''

__all__ = []
__version__ = 1.0
__author__ = 'Bhushan Barhate'
__date__ = '2018-03-10'
__updated__='2018-03-10'

import os
from flask import Flask, jsonify, g
from flask_sqlalchemy import SQLAlchemy
import functools
from flask import jsonify

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, '../data-dev.sqlite')

IGNORE_AUTH = True
SECRET_KEY = 'SECRET_KEY'
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + db_path

db = SQLAlchemy()

def create_app(config_name):
    """ Create an application instance. and return app object"""
    print(__name__)
    app = Flask(__name__)

    # apply configuration
    cfg = os.path.join(os.getcwd(), 'config', config_name + '.py')
    app.config.from_pyfile(cfg)

    # register blueprints
    from .api_v1 import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    # initialize extensions
    db.init_app(app)
    return app


def json(f):
    """Generate a JSON response from a database model or a Python
    dictionary."""
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        # invoke the wrapped function
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
        if not isinstance(rv, dict):
            rv = rv.export_data()

        # generate the JSON response
        rv = jsonify(rv)
        if status is not None:
            rv.status_code = status
        if headers is not None:
            rv.headers.extend(headers)
        return rv
    return wrapped
