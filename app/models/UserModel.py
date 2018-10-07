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
__updated__='2018-10-07'

from flask import url_for, current_app
from .. import db
from .. import ValidationError
from datetime import datetime
from dateutil import parser as datetime_parser
from dateutil.tz import tzutc


class User(db.Model):
    """ User model to store the users """

    """ Table name to store users """
    __tablename__ = 'users'

    """ User ID """
    id = db.Column(db.Integer, primary_key=True)

    """ User Name"""
    name = db.Column(db.String(64), index=True)

    """ Shoppinglists for a user ( ideally this should be only 1 shopping list per user) """
    shoppinglists = db.relationship('ShoppingList', backref='user', lazy='dynamic')

    def get_url(self):
        """ return self URL"""
        return url_for('api.get_user', id=self.id, _external=True)

    def export_data(self):
        """ export user data from the database """
        return {
            'self_url': self.get_url(),
            'id': self.id,
            'name': self.name,
            'shoppinglist_url': url_for('api.get_user_shoppinglist', userid=self.id,
                                  _external=True)
        }

    def get_shoppinglists_by_name(self, name):
        """ Return the single list which matches the name else return None """
        for i in self.shoppinglists:
            if i.name == name:
                return i
        v = ValidationError('Invalid Shopping List: shoppinglist with specified name is not found : ' + name)
        v.response_code = 404
        v.error="not found"
        raise v

    def get_shoppinglists_by_id(self, id):
        """ Return the single list which matches the id else return None """
        for i in self.shoppinglists:
            if i.id == id:
                return i
        v = ValidationError('Invalid Shopping List: shoppinglist with specified ID is not found : ' + str(id))
        v.response_code = 404
        v.error="not found"
        raise v

    def is_shopping_list_exists(self, data):
        """ check if the shopping lists exists with same name """
        try:
            lstname = data['name']
            for i in self.shoppinglists:
                if i.name == lstname:
                    return True
        except KeyError as e:
            raise ValidationError('Invalid Shopping List: missing ' + e.args[0])
        return False

    def import_data(self, data):
        """ Import users """
        try:
            self.name = data['name']
        except KeyError as e:
            raise ValidationError('Invalid customer: missing ' + e.args[0])
        return self
