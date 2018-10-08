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
from .tests import TestAPI

suite = unittest.TestLoader().loadTestsFromTestCase(TestAPI)
