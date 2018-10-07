#!/usr/bin/env python
# encoding: utf-8

'''
@author:     Bhushan Barhate
@contact:    bhushan2901@yahoo.co.in
'''

__all__ = []
__version__ = 1.0
__author__ = 'Bhushan Barhate'
__date__ = '2018-10-06'
__updated__ = '2018-10-07'

from flask import request, jsonify
from . import api
from .. import db, json
from .. import ValidationError


@api.errorhandler(ValidationError)
def bad_request(e):
    print(e.response_code)
    """ error handler for the bad request"""
    response = jsonify({'status': e.response_code, 'error': e.error,
                        'message': e.args[0]})
    response.status_code = e.response_code
    return response


@api.app_errorhandler(404)  # this has to be an app-wide handler
def not_found(e):
    print(e.description)
    ermsg = 'invalid resource URI'
    if e:
        ermsg = e.description
    response = jsonify({'status': 404, 'error': 'not found',
                        'message': ermsg})
    response.status_code = 404
    return response


@api.app_errorhandler(405)
def method_not_supported(e):
    response = jsonify({'status': 405, 'error': 'method not supported',
                        'message': 'the method is not supported'})
    response.status_code = 405
    return response


@api.app_errorhandler(500)  # this has to be an app-wide handler
def internal_server_error(e):
    response = jsonify({'status': 500, 'error': 'internal server error',
                        'message': e.args[0]})
    response.status_code = 500
    return response
