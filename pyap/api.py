# -*- coding: utf-8 -*-

"""
    pyap.api
    ~~~~~~~~~~~~~~~~

    This module contains address parser API functions.

    :copyright: (c) 2015 by Vladimir Goncharov.
    :license: MIT, see LICENSE for more details.
"""

from typing import Literal, List

from . import parser
from . import address


def parse(some_text: str, country: Literal["US", "GB", "CA"]) -> List[address.Address]:
    """Creates request to AddressParser
    and returns list of Address objects
    """
    ap = parser.AddressParser(country)
    return ap.parse(some_text)


def parse_single_street(
    some_text: str, country: Literal["US", "GB", "CA"]
) -> List[address.Address]:
    ap = parser.AddressParser(country)
    return ap.parse_single_street(some_text)
