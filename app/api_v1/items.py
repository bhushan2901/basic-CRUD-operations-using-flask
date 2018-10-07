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
from ..models.ShoppingListModel import ShoppingList
from ..models.UserModel import User

@api.route('/users/<int:userid>/shoppinglists/<int:lstid>/items/<int:id>', methods=['GET'])
@json
def get_item(userid, lstid, id):
    """ return the Item if found in database else return error code 404 """
    shoppinglst=User.query.get_or_404(userid).get_shoppinglists_by_id(lstid)
    item=shoppinglst.get_item_by_id(id)
    return item

@api.route('/items/', methods=['GET'])
@json
def get_items():
    """ return full list of items ( should use pages or this method dosent seems to be useful) """
    return Item.query.all()

@api.route('/users/<int:userid>/shoppinglists/<int:lstid>/items', methods=['POST'])
@json
def get_shopping_list_items(userid, lstid):
    shoppinglst=User.query.get_or_404(userid).get_shoppinglists_by_id(lstid)
    item = Item(shoppinglist=shoppinglst)
    item.import_data(request.json)
    db.session.add(item)
    db.session.commit()
    return item, 201
