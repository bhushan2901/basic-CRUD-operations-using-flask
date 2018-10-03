
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


from datetime import datetime
from flask import request
from . import api
from .. import db
from .. import json

@api.route('/items/', methods=['GET'])
@json
def get_item():
    """ sample API to make sure API the directory structure and package defination is working"""
    return {
        'self_url': 1,
        'order_url': 'tmp',
        'product_url': 'tmp1',
        'quantity': 3
    }
