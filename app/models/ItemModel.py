#!/usr/bin/env python
# encoding: utf-8

'''
@author:     Bhushan Barhate
@contact:    bhushan2901@yahoo.co.in
'''

__all__ = []
__version__ = 1.0
__author__ = 'Bhushan Barhate'
__date__ = '2018-10-04'
__updated__ = '2018-10-05'

from flask import url_for, current_app
from .. import db


class Item(db.Model):
    """ DB model class for the Item """

    """ TableName where the data will be stored """
    __tablename__ = 'items'

    """ ID column for the items table """
    id = db.Column(db.Integer, primary_key=True)

    """ Name for item table """
    name = db.Column(db.String)

    """ Shopping list ID for the item """
    shopping_list_id = db.Column(
        db.Integer,  db.ForeignKey('shoppinglists.id'), index=True)

    """ Quantity for the item in shopping list """
    quantity = db.Column(db.Integer)

    def get_url(self):
        """ Return the API URL for this item to be retrived directly """
        return url_for('api.get_item', id=self.id, lstid=self.shoppinglist.id,
                       userid=self.shoppinglist.user.id, _external=True)

    def export_data(self):
        """ Export the item and all its attributes in json format"""
        return {
            'self_url': self.get_url(),
            'quantity': self.quantity,
            'id': self.id,
            'name': self.name
        }

    def import_data(self, data):
        """ import the item in database , is item exists for same user and same shoppinglist
            then add the quantity in the item"""
        try:
            name = data['name']
            self.name = name

            if self.quantity:
                self.quantity = self.quantity + int(data['quantity'])
            else:
                self.quantity = int(data['quantity'])
        except KeyError as e:
            raise ValidationError('Invalid order: missing ' + e.args[0])
        return self
