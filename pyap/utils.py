# -*- coding: utf-8 -*-

"""
    pyap.utils
    ~~~~~~~~~~~~~~~~

    This module provides some utility functions.

    :copyright: (c) 2015 by Vladimir Goncharov.
    :license: MIT, see LICENSE for more details.
"""

import re
from typing import Any, List, Union

DEFAULT_FLAGS = re.VERBOSE | re.UNICODE


def match(
    regex: Union[str, re.Pattern[str]], string: str, flags: re.RegexFlag = DEFAULT_FLAGS
) -> Union[re.Match[str], None]:
    """Utility function for re.match"""
    return re.match(regex, string, flags=flags)


def findall(
    regex: Union[str, re.Pattern[str]], string: str, flags: re.RegexFlag = DEFAULT_FLAGS
) -> List[Any]:
    """Utility function for re.findall"""
    return re.findall(regex, string, flags=flags)


def finditer(
    regex: Union[str, re.Pattern[str]], string: str, flags: re.RegexFlag = DEFAULT_FLAGS
) -> List[re.Match[str]]:
    """Utility function for re.finditer"""
    return list(re.finditer(regex, string, flags=flags))


def unicode_str(string: str) -> str:
    """Return Unicode string"""
    return string
