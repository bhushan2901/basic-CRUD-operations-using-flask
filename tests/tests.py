#!/usr/bin/env python
# encoding: utf-8

'''
@author:     Bhushan Barhate
@contact:    bhushan2901@yahoo.co.in
Testing package
'''

__all__ = []
__version__ = 1.0
__author__ = 'Bhushan Barhate'
__date__ = '2018-10-07'
__updated__ = '2018-10-07'


import unittest
from werkzeug.exceptions import NotFound
from app import create_app, db
from app.models.UserModel import User
from app import ValidationError
from .test_client import TestClient

class TestAPI(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.drop_all()
        db.create_all()
        self.client = TestClient(self.app)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_users(self):
        # get list of users
        rv, json = self.client.get('/api/v1/users/')
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(json == [])

        # add a user
        rv, json = self.client.post('/api/v1/users/',
                                    data={'name': 'bhushan'})
        self.assertTrue(rv.status_code == 201)

        location = json['self_url']
        rv, json = self.client.get(location)
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(json['name'] == 'bhushan')
        rv, json = self.client.get('/api/v1/users/')
        self.assertTrue(rv.status_code == 200)

        # User update
        rv, json = self.client.put('/api/v1/users/1',
                                    data={'name': 'bhushan123'})
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(json['name'] == 'bhushan123')

        rv, json = self.client.post('/api/v1/users/',
                                    data={'name': 'bhushan123'})

        rv, json = self.client.delete('/api/v1/users/2')
        self.assertTrue(rv.status_code == 200)

        try:
            rv, json = self.client.post('/api/v1/users/',
                                    data={'name12': 'bhushan123'})
        except:
            print("error")


    def test_shopping_list(self):
        rv, json = self.client.get('/api/v1/shoppinglists/')
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(json == [])

        # add a user
        rv, json = self.client.post('/api/v1/users/',
                                    data={'name': 'bhushan'})
        self.assertTrue(rv.status_code == 201)


        rv, json = self.client.get('/api/v1/users/1/shoppinglists/')
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(json == [])

        rv, json = self.client.post('/api/v1/users/1/shoppinglists', data={"name": "list1","storename": "storename1"})
        self.assertTrue(rv.status_code == 201)

        rv, json = self.client.post('/api/v1/users/1/shoppinglists', data={"name": "list2","storename": "storename1"})
        rv, json = self.client.post('/api/v1/users/1/shoppinglists', data={"name": "list3shopping","storename": "storename2"})
        rv, json = self.client.post('/api/v1/users/1/shoppinglists', data={"name": "shoppinglist4","storename": "storename4"})
        rv, json = self.client.post('/api/v1/users/1/shoppinglists', data={"name": "list4","storename": "storename2"})
        rv, json = self.client.post('/api/v1/users/1/shoppinglists', data={"name": "list6","storename": "storename6"})
        rv, json = self.client.get('/api/v1/shoppinglists/sho')
        self.assertTrue(rv.status_code == 200)

        rv, json = self.client.get('/api/v1/users/1/shoppinglists/list4')
        self.assertTrue(rv.status_code == 200)
        try:
            rv, json = self.client.post('/api/v1/users/1/shoppinglists', data={"storename": "storename1"})
        except:
            print("error")

        try:
            rv, json = self.client.get('/api/v1/users/1/shoppinglists/list40')
        except:
            print("error")

        rv, json = self.client.get('/api/v1/users/1/shoppinglists/3')
        self.assertTrue(rv.status_code == 200)

        try:
            rv, json = self.client.get('/api/v1/users/1/shoppinglists/50')
        except:
            print("error")

        try:
            rv, json = self.client.post('/api/v1/users/1/shoppinglists', data={"name": "storename6"})
            self.assertRaises(ValidationError)
        except:
            print("error")

        rv, json = self.client.put('/api/v1/users/1/shoppinglists/1', data={"name": "list123"})
        self.assertTrue(rv.status_code == 200)

        try:
            rv, json = self.client.put('/api/v1/users/1/shoppinglists/1', data={"name": "list2","storename": "storename1"})
        except:
            print("error")

        try:
            rv, json = self.client.post('/api/v1/users/1/shoppinglists', data={"name": "list6","storename": "storename6"})
        except:
            print("error")

        try:
            rv, json = self.client.put('/api/v1/users/1/shoppinglists/1', data={"storename": "storename2"})
        except:
            print("error")

        rv, json = self.client.put('/api/v1/users/1/shoppinglists/1', data={"name": "list1","storename": "storename2"})
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(json['storename'] == 'storename2')

        rv, json = self.client.delete('/api/v1/users/1/shoppinglists/1')
        self.assertTrue(rv.status_code == 200)

    def test_items_list(self):
        rv, json = self.client.get('/api/v1/items/')
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(json == [])

        # add a user
        rv, json = self.client.post('/api/v1/users/', data={'name': 'bhushan'})
        rv, json = self.client.post('/api/v1/users/1/shoppinglists', data={"name": "list1","storename": "storename1"})
        rv, json = self.client.post('/api/v1/users/1/shoppinglists', data={"name": "list2","storename": "storename1"})
        rv, json = self.client.post('/api/v1/users/1/shoppinglists', data={"name": "list3shopping","storename": "storename2"})
        rv, json = self.client.post('/api/v1/users/1/shoppinglists', data={"name": "shoppinglist4","storename": "storename4"})

        #Add item
        rv, json = self.client.post('/api/v1/users/1/shoppinglists/1/items', data=[{"name": "item2","quantity": 2},{"name": "item3","quantity": 4}])
        self.assertTrue(rv.status_code == 201)

        rv, json = self.client.get('/api/v1/users/1/shoppinglists/1/items/1')
        self.assertTrue(rv.status_code == 200)

        rv, json = self.client.get('/api/v1/users/1/shoppinglists/items/item')
        self.assertTrue(rv.status_code == 200)

        rv, json = self.client.post('/api/v1/users/1/shoppinglists/1/items', data=[{"name": "item2","quantity": 2},{"name": "item3","quantity": 4}])
        self.assertTrue(rv.status_code == 201)

        rv, json = self.client.get('/api/v1/users/1/shoppinglists/1/items/item3')
        self.assertTrue(rv.status_code == 200)

        rv, json = self.client.delete('/api/v1/users/1/shoppinglists/1/items/1')
        self.assertTrue(rv.status_code == 200)

        try:
            rv, json = self.client.get('/api/v1/users/1/shoppinglists/1/items/item2')
            self.assertTrue(rv.status_code == 200)
        except:
            print("error")

        try:
            rv, json = self.client.post('/api/v1/users/1/shoppinglists/1/items', data=[{"quantity": 2}])
        except:
            print("error")

        try:
            rv, json = self.client.post('/api/v1/users/1/shoppinglists/1/items', data=[{"name": "item2","quantity": 2},{"name": "item2"}])
        except:
            print("error")
        try:
            rv, json = self.client.get('/api/v1/users/1/shoppinglists/1/items/10')
            print(json)
        except:
            print("error")

        try:
            rv, json = self.client.get('/api/v1/users/1/shoppinglists/1/items/item10')
            print(json)
        except:
            print("error")
