#!/usr/bin/env python
# encoding: utf-8

'''
@author:     Bhushan Barhate
@contact:    bhushan2901@yahoo.co.in
'''

__all__ = []
__version__ = 1.0
__author__ = 'Bhushan Barhate'
__date__ = '2018-10-07'
__updated__ = '2018-10-07'

#!/usr/bin/env python
import coverage
COV = coverage.coverage(branch=True, include='app/*')
COV.start()

import unittest
from tests import suite
unittest.TextTestRunner(verbosity=2).run(suite)

COV.stop()
COV.report(show_missing=True)
