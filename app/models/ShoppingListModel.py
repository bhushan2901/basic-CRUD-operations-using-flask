#!/usr/bin/env python
# encoding: utf-8

'''
@author:     Bhushan Barhate
@contact:    bhushan2901@yahoo.co.in
'''

__all__ = []
__version__ = 1.0
__author__ = 'Bhushan Barhate'
__date__ = '2018-10-05'
__updated__='2018-10-05'

from flask import url_for, current_app
from .. import db
from .. import ValidationError
from datetime import datetime, timezone
from dateutil import parser as datetime_parser
from dateutil.tz import tzutc

class ShoppingList(db.Model):
    """ DB model class for the Shopping List """

    """ Database table name"""
    __tablename__ = 'shoppinglists'

    "unique id for shoppinglists table"
    id = db.Column(db.Integer, primary_key=True)

    "Title for the shoppign lists"
    name = db.Column(db.String, unique=True)

    "store name for this shopping lists"
    storename=db.Column(db.String)

    """ userid which has this shohpping list object """
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                            index=True)

    """ Current date time at the time shopping list is created """
    date = db.Column(db.DateTime, default=datetime.now)

    """ List of items in the shopping list initially empty lists """
    items = db.relationship('Item', backref='shoppinglist', lazy='dynamic',
                            cascade='all, delete-orphan')

    def get_url(self):
        """ Return the url for shopping list object """
        return url_for('api.get_user_shoppinglists_by_id', userid=self.user_id, id=self.id, _external=True)

    def export_data(self):
        """ export the data in json format"""
        return {
            'self_url': self.get_url(),
            'user_url': self.user.get_url(),
            "name" : self.name,
            'date': self.date.isoformat() + 'Z',
            'storename' : self.storename,
            'id': self.id
            # TODO add a code to add the items
        }

    def import_data(self, data):
        """ Import the data for a shopping list item, we need to add more checks here for items"""
        # TODO add items to the list
        try:
            self.name = data['name']
            self.storename = data['storename']
            self.date = datetime_parser.parse(datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'))
        except KeyError as e:
            raise ValidationError('Invalid Shopping List: missing ' + e.args[0])
        return self


    def update_data(self, data, name):
        """ TODO """
        try:
            self.name = name
            self.date = datetime_parser.parse(datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'))
        except KeyError as e:
            raise ValidationError('Invalid Shopping List: missing ' + e.args[0])
        return self
