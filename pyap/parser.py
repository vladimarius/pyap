# -*- coding: utf-8 -*-

"""
    pyap.parser
    ~~~~~~~~~~~~~~~~

    This module contains AddressParser class which connects all the
    functionality of the package in one place.

    :copyright: (c) 2015 by Vladimir Goncharov.
    :license: MIT, see LICENSE for more details.
"""

import re
import importlib
from typing import Any, Dict, List, Literal

from . import exceptions as e
from . import address
from . import utils


class AddressParser:
    def __init__(self, country: Literal["US", "CA", "GB"]):
        """Initialize with custom arguments"""
        self.country = country.upper()

        try:
            # import detection rules
            package = "pyap" + ".source_" + self.country + ".data"
            data = importlib.import_module(package)
            self.rules = data.full_address
            self.single_street_rules = data.full_street

        except ImportError:
            raise e.CountryDetectionMissing(
                'Detection rules for country "{country}" not found.'.format(
                    country=self.country
                ),
                "Error 2",
            )

    def parse(self, text: str) -> List[address.Address]:
        """Returns a list of addresses found in text
        together with parsed address parts
        """
        return self._parse(self.rules, text)

    def parse_single_street(self, text: str) -> List[address.Address]:
        return self._parse(self.single_street_rules, text)

    def _parse(self, rules: str, text: str) -> List[address.Address]:
        results = []
        self.clean_text = self._normalize_string(text)

        # get addresses
        address_matches = utils.finditer(rules, self.clean_text)
        if address_matches:
            # append parsed address info
            results = list(map(self._parse_address, address_matches))

        return results

    def _parse_address(self, match: re.Match[str]) -> address.Address:
        """Parses address into parts"""
        match_as_dict = match.groupdict()
        match_as_dict.update({"country_id": self.country})
        # combine results
        cleaned_dict = self._combine_results(match_as_dict)
        cleaned_dict["match_start"] = match.start()
        cleaned_dict["match_end"] = match.end()

        # if only parsing a single street the full address is the full street
        if "full_address" not in cleaned_dict:
            cleaned_dict["full_address"] = cleaned_dict["full_street"]

        # create object containing results
        return address.Address(**cleaned_dict)

    @staticmethod
    def _combine_results(match_as_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Combine results from different parsed parts:
        we look for non-empty results in values like
        'postal_code_b' or 'postal_code_c' and store
        them as main value.

        So 'postal_code_b':'123456'
            becomes:
           'postal_code'  :'123456'
        """
        keys = []
        vals = []
        for k, v in match_as_dict.items():
            if k[-2:] in "_a_b_c_d_e_f_g_h_i_j_k_l_m":
                if v:
                    # strip last 2 chars: '..._b' -> '...'
                    keys.append(k[:-2])
                    vals.append(v)
            else:
                if k not in keys:
                    keys.append(k)
                    vals.append(v)
        return dict(zip(keys, vals))

    @staticmethod
    def _normalize_string(text: str) -> str:
        """Prepares incoming text for parsing:
        removes excessive spaces, tabs, etc.
        We should keep the newlines as they are
        good indicators for limits of elements.
        """
        conversion = {
            r"[\ \t]*(\,[\ \t]*)+": ", ",
            # replace excessive empty spaces
            r"\ +": " ",
            # convert all types of hyphens/dashes to a
            # simple old-school dash
            # from http://utf8-chartable.de/unicode-utf8-table.pl?
            # start=8192&number=128&utf8=string-literal
            "‐": "-",
            "‑": "-",
            "‒": "-",
            "–": "-",
            "—": "-",
            "―": "-",
        }
        for find, replace in conversion.items():
            text = re.sub(find, replace, text, flags=re.UNICODE)
        return text
