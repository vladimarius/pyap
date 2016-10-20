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

from . import exceptions as e
from . import address
from . import utils
from .packages import six


class AddressParser:

    def __init__(self, **args):
        '''Initialize with custom arguments'''
        for k, v in six.iteritems(args):
            # store country id in uppercase
            if k == 'country':
                v = v.upper()
            setattr(self, k, v)
        try:
            # import detection rules
            package = 'pyap' + '.source_' + self.country + \
                '.data'
            data = importlib.import_module(package)
            self.rules = data.full_address

        except AttributeError:
            raise e.NoCountrySelected(
                'No country specified during library initialization.',
                'Error 1')

        except ImportError:
            raise e.CountryDetectionMissing(
                'Detection rules for country "{country}" not found.'.
                format(country=self.country), 'Error 2'
            )

    def parse(self, text):
        '''Returns a list of addresses found in text
        together with parsed address parts
        '''
        results = []
        if isinstance(text, str):
            if six.PY2:
                text = unicode(text, 'utf-8')
        self.clean_text = self._normalize_string(text)

        # get addresses
        addresses = set(self._get_addresses(self.clean_text))
        if addresses:
            # append parsed address info
            results = list(map(self._parse_address, addresses))

        return results

    def _parse_address(self, address_string):
        '''Parses address into parts'''
        match = utils.match(self.rules, address_string, flags=re.VERBOSE | re.U)
        if match:
            match_as_dict = match.groupdict()
            match_as_dict.update({'country_id': self.country})
            # combine results
            cleaned_dict = self._combine_results(match_as_dict)
            # create object containing results
            return address.Address(**cleaned_dict)

        return False

    def _combine_results(self, match_as_dict):
            '''Combine results from different parsed parts:
            we look for non-empty results in values like
            'postal_code_b' or 'postal_code_c' and store
            them as main value.

            So 'postal_code_b':'123456'
                becomes:
               'postal_code'  :'123456'
            '''
            keys = []
            vals = []
            for k, v in six.iteritems(match_as_dict):
                if k[-2:] in '_a_b_c_d_e_f_g_h_i_j_k_l_m':
                    if v:
                        # strip last 2 chars: '..._b' -> '...'
                        keys.append(k[:-2])
                        vals.append(v)
                else:
                    if k not in keys:
                        keys.append(k)
                        vals.append(v)
            return dict(zip(keys, vals))

    def _normalize_string(self, text):
        '''Prepares incoming text for parsing:
        removes excessive spaces, tabs, newlines, etc.
        '''
        conversion = {
            # newlines
            '\r?\n': ' ',
            # replace excessive empty spaces
            '\s+': ' ',
            # convert all types of hyphens/dashes to a
            # simple old-school dash
            # from http://utf8-chartable.de/unicode-utf8-table.pl?
            # start=8192&number=128&utf8=string-literal
            '‐': '-',
            '‑': '-',
            '‒': '-',
            '–': '-',
            '—': '-',
            '―': '-',
        }
        for find, replace in six.iteritems(conversion):
            text = re.sub(find, replace, text, flags=re.UNICODE)
        return text

    def _get_addresses(self, text):
        '''Returns a list of addresses found in text'''
        # find addresses
        addresses = []
        matches = utils.findall(
            self.rules,
            text,
            flags=re.VERBOSE | re.U)

        if(matches):
            for match in matches:
                addresses.append(match[0].strip())
        return addresses
