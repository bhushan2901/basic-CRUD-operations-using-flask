#!/usr/bin/env python
# encoding: utf-8

'''
@author:     Bhushan Barhate
@contact:    bhushan2901@yahoo.co.in
'''

__all__ = []
__version__ = 1.0
__author__ = 'Bhushan Barhate'
__date__ = '2018-03-11'
__updated__='2018-03-11'

from flask import url_for, current_app
from .. import db

class Item(db.Model):
    """ DB model class for the Item """

    """ TableName where the data will be stored """
    __tablename__ = 'items'

    """ ID column for the items table """
    id = db.Column(db.Integer, primary_key=True)

    """ Shopping list ID for the item """
    shopping_list_id = db.Column(db.Integer)

    """ Quantity for the item in shopping list """
    quantity = db.Column(db.Integer)

    def get_url(self):
        """ Return the API URL for this item to be retrived directly """
        return url_for('api.get_item', id=self.id, _external=True)

    def export_data(self):
        """ Export the item and all its attributes in json format"""
        return {
            'self_url': self.get_url(),
            'quantity': self.quantity
        }
