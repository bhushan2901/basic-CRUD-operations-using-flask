
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

from flask import request, abort
from . import api
from .. import db, json
from ..models.ShoppingListModel import ShoppingList
from ..models.UserModel import User
from .. import ValidationError

@api.route('/shoppinglists/', methods=['GET'])
@json
def get_shopping_list():
    """ return the list of all shoppinglists available in database"""
    return ShoppingList.query.all()

@api.route('/shoppinglists/<pattern>', methods=['GET'])
@json
def get_shopping_list_using_pattern(pattern):
    """ return the list of all shoppinglists which contains the keyword int he requests"""
    return ShoppingList.query.filter(ShoppingList.name.like('%'+pattern+'%')).all()


@api.route('/users/<int:userid>/shoppinglists/', methods=['GET'])
@json
def get_user_shoppinglist(userid):
    """ return the shoppinglists for a user (ideally this should only be one shopping list per user) """
    user = User.query.get_or_404(userid)
    return user.shoppinglists.all()

@api.route('/users/<int:userid>/shoppinglists', methods=['POST'])
@json
def new_user_shoppinglists(userid):
    """ add item to the shopping list"""
    user = User.query.get_or_404(userid)
    if user.isshoppinglistexists(request.json):
        raise ValidationError('Invalid Shopping List: shopping list with same name already exists ')
    slst = ShoppingList(user=user)
    slst.import_data(request.json)
    db.session.add(slst)
    db.session.commit()
    return slst, 201

@api.route('/users/<int:userid>/shoppinglists/<name>', methods=['GET'])
@json
def get_user_shoppinglists_by_name(userid, name):
    """ return user to the shopping list which matches with the name """
    user = User.query.get_or_404(userid)
    lst=user.get_shoppinglists_by_name(name)
    return lst

@api.route('/users/<int:userid>/shoppinglists/<int:id>', methods=['GET'])
@json
def get_user_shoppinglists_by_id(userid, id):
    """ return user to the shopping list which matches with the id """
    user = User.query.get_or_404(userid)
    lst=user.get_shoppinglists_by_id(id)
    return lst

@api.route('/users/<int:userid>/shoppinglists/<int:id>', methods=['DELETE'])
@json
def delete_shoppinglists_by_id(userid,id):
    """ delete a shoppinglist for given user """
    user = User.query.get_or_404(userid)
    lst=user.get_shoppinglists_by_id(id)
    data=lst.export_data()
    db.session.delete(lst)
    db.session.commit()
    return data

@api.route('/users/<int:userid>/shoppinglists/<int:id>', methods=['PUT'])
@json
def update_shoppinglists_by_id(userid,id):
    """ udate a user in the system """
    user = User.query.get_or_404(userid)
    lst=user.get_shoppinglists_by_id(id)
    #TODO write a function to update the shopping lists
    lst.update_shopping_list(request.json)
    db.session.add(lst)
    db.session.commit()
    return user.export_data()
