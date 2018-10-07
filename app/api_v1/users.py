
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
__updated__ = '2018-10-07'

from flask import request
from . import api
from .. import db, json
from ..models.UserModel import User


@api.route('/users/', methods=['GET'])
@json
def get_users():
    return User.query.all()


@api.route('/users/<int:id>', methods=['GET'])
@json
def get_user(id):
    """ Return the user with specified ID """
    return User.query.get_or_404(id)


@api.route('/users/', methods=['POST'])
@json
def new_user():
    """ Add a new user to the list currently it will just keep adding the users with same name"""
    user = User()
    print("Bhushan: ", request)
    user.import_data(request.json)
    db.session.add(user)
    db.session.commit()
    return user.export_data(), 201


@api.route('/users/<int:id>', methods=['PUT'])
@json
def edit_user(id):
    """ udate a user in the system """
    user = User.query.get_or_404(id)
    user.import_data(request.json)
    db.session.add(user)
    db.session.commit()
    return user.export_data()


@api.route('/users/<int:id>', methods=['DELETE'])
@json
def delete_user(id):
    """ delete a user in the system """
    user = User.query.get_or_404(id)
    data = user.export_data()
    db.session.delete(user)
    db.session.commit()
    return data
