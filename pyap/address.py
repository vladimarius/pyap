# -*- coding: utf-8 -*-

"""
    pyap.address
    ~~~~~~~~~~~~~~~~

    Contains class for constructing Address object which holds information
    about address and its components.

    :copyright: (c) 2015 by Vladimir Goncharov.
    :license: MIT, see LICENSE for more details.
"""

from dataclasses import dataclass
from typing import Union


@dataclass
class Address:
    match_end: int
    match_start: int

    country_id: str
    full_street: str
    full_address: str
    city: Union[str, None] = None
    floor: Union[str, None] = None
    region1: Union[str, None] = None
    country: Union[str, None] = None
    route_id: Union[str, None] = None
    occupancy: Union[str, None] = None
    street_type: Union[str, None] = None
    building_id: Union[str, None] = None
    postal_code: Union[str, None] = None
    single_street_name: Union[str, None] = None
    street_name: Union[str, None] = None
    street_number: Union[str, None] = None
    po_box: Union[str, None] = None
    post_direction: Union[str, None] = None
    phone_number: Union[str, None] = None

    def __post_init__(self):
        for s_field in self.__dataclass_fields__:
            field = getattr(self, s_field)
            if isinstance(field, str):
                setattr(self, s_field, field.strip(" ,;:"))
            elif isinstance(field, list) and field and isinstance(field[0], str):
                setattr(self, s_field, field[0].strip(" ,;:"))

    def __repr__(self) -> str:
        # Address object is represented as textual address
        address = ""
        try:
            address = self.full_address
        except AttributeError:
            pass
        return address
