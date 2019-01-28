# -*- coding: utf-8 -*-

"""
    pyap.utils
    ~~~~~~~~~~~~~~~~

    This module provides some utility functions.

    :copyright: (c) 2015 by Vladimir Goncharov.
    :license: MIT, see LICENSE for more details.
"""

import re
from .packages import six


if six.PY2:

    def match(regex, string, flags=0):
        '''Utility function for re.match '''
        if isinstance(string, str):
            string = unicode(string, 'utf-8')
        return re.match(
            unicode(regex, 'utf-8'),
            string,
            flags=flags
        )

    def findall(regex, string, flags=0):
        '''Utility function for re.findall '''
        if isinstance(string, str):
            string = unicode(string, 'utf-8')
        return re.findall(
            unicode(regex, 'utf-8'),
            string,
            flags=flags
        )

    def unicode_str(string):
        '''Return Unicode string'''
        return unicode(string, 'utf-8')

elif six.PY3:

    def match(regex, string, flags=0):
        '''Utility function for re.match '''
        return re.match(regex, string, flags=flags)

    def findall(regex, string, flags=0):
        '''Utility function for re.findall '''
        return re.findall(regex, string, flags=flags)

    def unicode_str(string):
        '''Return Unicode string'''
        return string
