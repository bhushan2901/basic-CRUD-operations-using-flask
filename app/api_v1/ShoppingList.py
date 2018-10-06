
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
__updated__='2018-10-06'

from flask import request
from . import api
from .. import db, json
from ..models.ShoppingListModel import ShoppingList
from ..models.UserModel import User

@api.route('/shoppinglists/', methods=['GET'])
@json
def get_shopping_list():
    """ return the list of all shoppinglists available in database"""
    return ShoppingList.query.all()

@api.route('/users/<int:id>/shoppinglists/', methods=['GET'])
@json
def get_user_shoppinglist(id):
    """ return the shoppinglists for a user (ideally this should only be one shopping list per user) """
    user = User.query.get_or_404(id)
    return user.shoppinglists.all()

@api.route('/users/<int:id>/shoppinglists/<name>', methods=['POST'])
@json
def new_user_shoppinglists(id, name):
    """ add item to the shopping list"""
    user = User.query.get_or_404(id)
    slst = ShoppingList(user=user)
    slst.import_data(request.json, name)
    db.session.add(slst)
    db.session.commit()
    return slst.export_data, 201
