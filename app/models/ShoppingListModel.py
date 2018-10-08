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
__updated__ = '2018-10-05'

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
    storename = db.Column(db.String)

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
            "name": self.name,
            'date': self.date.isoformat() + 'Z',
            'storename': self.storename,
            'items': [item.export_data() for item in self.items],
            'id': self.id
            # TODO add a code to add the items
        }

    def import_data(self, data):
        """ Import the data for a shopping list item, we need to add more checks here for items"""
        try:
            self.name = data['name']
            self.storename = data['storename']
            self.date = datetime_parser.parse(datetime.now(
                timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'))
        except KeyError as e:
            raise ValidationError(
                'Invalid Shopping List: missing ' + e.args[0])
        return self

    def update_data(self, id, data):
        """ update the shopping list wiht new data, every time shopping list is updated the date filed will be updated as well"""
        try:
            lstname = data['name']
            print("bhushan"+lstname  + self.name)
            for lst in self.user.shoppinglists:
                if lst.name == lstname and lst.id != id:
                    raise ValidationError('Invalid Shopping List: shopping list with same name already exists with differnet ID')

            self.name = lstname
            if 'storename' in data:
                self.storename = data['storename']

            self.date = datetime_parser.parse(datetime.now(
                timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'))
        except KeyError as e:
            raise ValidationError(
                'Invalid Shopping List: missing ' + e.args[0])
        return self

    def get_item_by_id(self, id):
        """ Return the single item which matches the id else return None """
        for i in self.items:
            if i.id == id:
                return i
        v = ValidationError(
            'Invalid Items List: Item with specified ID is not found : ' + str(id))
        v.response_code = 404
        v.error = "not found"
        raise v

    def get_item_by_name(self, name):
        """ Return the single item which matches the name else return None """
        for i in self.items:
            if i.name == name:
                return i
        v = ValidationError(
            'Invalid Items List: Item with specified name is not found : ' + name)
        v.response_code = 404
        v.error = "not found"
        raise v

    def is_item_exists(self, data):
        """ check if the item exists with same name """
        try:
            itmname = data['name']
            for i in self.items:
                if i.name == itmname:
                    return True
        except KeyError as e:
            raise ValidationError('Invalid Item List: missing ' + e.args[0])
        return False
