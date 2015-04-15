# -*- coding: utf-8 -*-

"""
    pyap.api
    ~~~~~~~~~~~~~~~~

    This module contains address parser API functions.

    :copyright: (c) 2015 by Vladimir Goncharov.
    :license: MIT, see LICENSE for more details.
"""

from . import parser


def parse(some_text, **kwargs):
    """Creates request to AddressParser
    and returns list of Address objects
    """
    ap = parser.AddressParser(**kwargs)
    return ap.parse(some_text)
