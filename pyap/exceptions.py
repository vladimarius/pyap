# -*- coding: utf-8 -*-

"""
    pyap.exceptions
    ~~~~~~~~~~~~~~~~

    This module contains address parser exceptions.

    :copyright: (c) 2015 by Vladimir Goncharov.
    :license: MIT, see LICENSE for more details.
"""


class AddressParserException(Exception):
    pass


class CountryDetectionMissing(AddressParserException):
    """Country-specific address detection rules were not found"""

    def __init__(self, message, errors):
        super(CountryDetectionMissing, self).__init__(message)
        self.errors = errors
