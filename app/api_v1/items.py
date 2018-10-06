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
__updated__='2018-10-04'

from flask import request
from . import api
from .. import db, json
from ..models.ItemModel import Item

@api.route('/items/<int:id>', methods=['GET'])
@json
def get_item(id):
    """ return the Item if found in database else return error code 404
    Parameters:
              arg1 (int) : Item
    Returns:
              Returns Json object for the Item details"""
    return Item.query.get_or_404(id).export_data()

@api.route('/items/', methods=['GET'])
@json
def get_shopping_list_items(id):
    return None
