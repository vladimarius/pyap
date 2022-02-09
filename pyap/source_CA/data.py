# -*- coding: utf-8 -*-

"""
    pyap.source_US.data
    ~~~~~~~~~~~~~~~~~~~~

    This module provides regular expression definitions required for
    detecting Canada addresses.

    The module is expected to always contain 'full_address' variable containing
    all address parsing definitions.

    :copyright: (c) 2015 by Vladimir Goncharov.
    :license: MIT, see LICENSE for more details.
"""

import re

''' Numerals from one to nine
Note: here and below we use syntax like '[Oo][Nn][Ee]'
instead of '(one)(?i)' to match 'One' or 'oNe' because
Python Regexps don't seem to support turning On/Off
case modes for subcapturing groups.
'''
zero_to_nine = r"""(?:
    [Zz][Ee][Rr][Oo]\ |[Oo][Nn][Ee]\ |[Tt][Ww][Oo]\ |
    [Tt][Hh][Rr][Ee][Ee]\ |[Ff][Oo][Uu][Rr]\ |
    [Ff][Ii][Vv][Ee]\ |[Ss][Ii][Xx]\ |
    [Ss][Ee][Vv][Ee][Nn]\ |[Ee][Ii][Gg][Hh][Tt]\ |
    [Nn][Ii][Nn][Ee]\ |[Tt][Ee][Nn]\ |
    [Ee][Ll][Ee][Vv][Ee][Nn]\ |
    [Tt][Ww][Ee][Ll][Vv][Ee]\ |
    [Tt][Hh][Ii][Rr][Tt][Ee][Ee][Nn]\ |
    [Ff][Oo][Uu][Rr][Tt][Ee][Ee][Nn]\ |
    [Ff][Ii][Ff][Tt][Ee][Ee][Nn]\ |
    [Ss][Ii][Xx][Tt][Ee][Ee][Nn]\ |
    [Ss][Ee][Vv][Ee][Nn][Tt][Ee][Ee][Nn]\ |
    [Ee][Ii][Gg][Hh][Tt][Ee][Ee][Nn]\ |
    [Nn][Ii][Nn][Ee][Tt][Ee][Ee][Nn]\ 
    )
"""

# Numerals - 10, 20, 30 ... 90
ten_to_ninety = r"""(?:
    [Tt][Ee][Nn]\ |[Tt][Ww][Ee][Nn][Tt][Yy]\ |
    [Tt][Hh][Ii][Rr][Tt][Yy]\ |
    [Ff][Oo][Rr][Tt][Yy]\ |
    [Ff][Oo][Uu][Rr][Tt][Yy]\ |
    [Ff][Ii][Ff][Tt][Yy]\ |[Ss][Ii][Xx][Tt][Yy]\ |
    [Ss][Ee][Vv][Ee][Nn][Tt][Yy]\ |
    [Ee][Ii][Gg][Hh][Tt][Yy]\ |
    [Nn][Ii][Nn][Ee][Tt][Yy]\ 
    )"""

# One hundred
hundred = r"""(?:
    [Hh][Uu][Nn][Dd][Rr][Ee][Dd]\ 
    )"""

# One thousand
thousand = r"""(?:
    [Tt][Hh][Oo][Uu][Ss][Aa][Nn][Dd]\ 
    )"""

'''
Regexp for matching street number.
Street number can be written 2 ways:
1) Using letters - "One thousand twenty two"
2) Using numbers
   a) - "1022"
   b) - "85-1190"
        "85 - 1190"
        "85th - 1190"
   c) - "85 1190"
'''
street_number = r"""(?<![\.0-9])(?P<street_number>
                        (?:
                            [Aa][Nn][Dd]\ 
                            |
                            {thousand}
                            |
                            {hundred}
                            |
                            {zero_to_nine}
                            |
                            {ten_to_ninety}
                        ){from_to}
                        |
                        # 85th - 1190
                        (?:\d{from_to}(?:th)?
                            (?:\ ?\-?\ ?\d{from_to}(?:th)?)?\ 
                        )
                        |
                        # 45
                        (?:\d{from_to}(?=[\ ,]))
                    )
                """.format(thousand=thousand,
                           hundred=hundred,
                           zero_to_nine=zero_to_nine,
                           ten_to_ninety=ten_to_ninety,
                           from_to='{1,5}')

'''
Regexp for matching street name.
In example below:
"Hoover Boulevard": "Hoover" is a street name
'''
street_name = r"""(?P<street_name>
                  \w[\w0-9\'\-\ \.]{0,30}?
                 )
              """

post_direction = r"""
                    (?P<post_direction>
                        (?:
                            # English
                            [Nn][Oo][Rr][Tt][Hh]{d}|
                            [Ss][Oo][Uu][Tt][Hh]{d}|
                            [Ee][Aa][Ss][Tt]{d}|
                            [Ww][Ee][Ss][Tt]{d}|
                            [Nn][Oo][Rr][Tt][Hh][Ee][Aa][Ss][Tt]{d}|
                            [Nn][Oo][Rr][Tt][Hh][Ww][Ee][Ss][Tt]{d}|
                            [Ss][Oo][Uu][Tt][Hh][Ee][Aa][Ss][Tt]{d}|
                            [Ss][Oo][Uu][Tt][Hh][Ww][Ee][Ss][Tt]{d}|
                            # French
                            [Ee][Ss][Tt]{d}|
                            [Nn][Oo][Rr][Dd]{d}|
                            [Nn][Oo][Rr][Dd]\-[Ee][Ss][Tt]{d}|
                            [Nn][Oo][Rr][Dd]\-[Oo][Uu][Ee][Ss][Tt]{d}|
                            [Ss][Uu][Dd]{d}|
                            [Ss][Uu][Dd]\-[Ee][Ss][Tt]{d}|
                            [Ss][Uu][Dd]\-[Oo][Uu][Ee][Ss][Tt]{d}|
                            [Oo][Uu][Ee][Ss][Tt]{d}
                        )
                        |
                        (?:
                            # English
                            NW{d}|NE{d}|SW{d}|SE{d}|
                            # French (missing above)
                            NO{d}|SO{d}
                        )
                        |
                        (?:
                            # English
                            N[\.\ ]|S[\.\ ]|E[\.\ ]|W[\.\ ]|
                            # French (missing above)
                            O[\.\ ]
                        )
                    )
                """.format(d='[\ ,]')

# Regexp for matching street type
# According to
# https://www.canadapost.ca/tools/pg/manual/PGaddress-e.asp#1385939
street_type = r"""
            (?P<street_type>
                [Aa][Bb][Bb][Ee][Yy]{div}|
                [Aa][Cc][Rr][Ee][Ss]{div}|
                [Aa][Ll][Ll][Éé][Ee]{div}|
                [Aa][Ll][Ll][Ee][Yy]{div}|
                [Aa][Uu][Tt][Oo][Rr][Oo][Uu][Tt][Ee]{div}|[Aa][Uu][Tt]{div}|
                [Aa][Vv][Ee][Nn][Uu][Ee]{div}|[Aa][Vv][Ee]?{div}|
                [Bb][Aa][Yy]{div}|
                [Bb][Ee][Aa][Cc][Hh]{div}|
                [Bb][Ee][Nn][Dd]{div}|
                [Bb][Oo][Uu][Ll][Ee][Vv][Aa][Er][Dd]{div}|[Bb][Ll][Vv][Dd]{div}|[Bb][Oo][Uu][Ll]{div}|
                # Broadway
                [Bb][Rr][Oo][Aa][Dd][Ww][Aa][Yy]{div}|
                [Bb][Yy]\-?[Pp][Aa][Ss][Ss]{div}|
                [Bb][Yy][Ww][Aa][Yy]{div}|
                [Cc][Aa][Mm][Pp][Uu][Ss]{div}|
                [Cc][Aa][Pp][Ee]{div}|
                [Cc][Aa][Rr][Rr][EéÉ]{div}|[Cc][Aa][Rr]{div}|
                [Cc][Aa][Rr][Rr][Ee][Ff][Oo][Uu][Rr]{div}|[Cc][Aa][Rr][Re][Ee][Ff]{div}|
                [Cc][Ee][Nn][Tt][Rr][Ee]{div}|[Cc][Tt][Rr]{div}|
                [Cc][Ee][Rr][Cc][Ll][Ee]{div}|
                [Cc][Hh][Aa][Ss][Ee]{div}|
                [Cc][Hh][Ee][Mm][Ii][Nn]{div}|[Cc][Hh]{div}|
                [Cc][Ii][Rr][Cc][Ll][Ee]{div}|[Cc][Ii][Rr]{div}|
                [Cc][Ii][Rr][Cc][Uu][Ii][Tt]{div}|[Cc][Ii][Rr][Cc][Tt]{div}|
                [Cc][Ll][Oo][Ss][Ee]{div}|
                [Cc][Oo][Mm][Mm][Oo][Nn]{div}|
                [Cc][Oo][Nn][Cc][Ee][Ss][Ss][Ii][Oo][Nn]{div}|[Cc][Oo][Nn][Cc]{div}|
                [Cc][Oo][Rr][Nn][Ee][Rr][Ss]{div}|
                [Cc][Ôô][Tt][Ee]{div}|
                [Cc][Oo][Uu][Rr][Ss]{div}|
                [Cc][Oo][Uu][Rr]{div}|
                [Cc][Oo][Uu][Rr][Tt]{div}|[Cc][Rr][Tt]{div}|
                [Cc][Oo][Vv][Ee]{div}|
                [Cc][Rr][Ee][Ss][Cc][Ee][Nn][Tt]{div}|[Cc][Rr][Ee][Ss]{div}|
                [Cc][Rr][Oo][Ii][Ss][Ss][Aa][Nn][Tt]{div}|[Cc][Rr][Oo][Ii][Ss]{div}|
                [Cc][Rr][Oo][Ss][Ss][Ii][Nn][Gg]{div}|[Cc][Rr][Oo][Ss][Ss]{div}|
                [Cc][Uu][Ll]\-[Dd][Ee]\-[Ss][Aa][Cc]{div}|[Cc][Dd][Ss]{div}|
                [Dd][Aa][Ll][Ee]{div}|
                [Dd][Ee][Ll][Ll]{div}|
                [Dd][Ii][Vv][Ee][Rr][Ss][Ii][Oo][Nn]{div}|[Dd][Ii][Vv][Ee][Rr][Ss]{div}|
                [Dd][Oo][Ww][Nn][Ss]{div}|
                [Dd][Rr][Ii][Vv][Ee]{div}|[Dd][Rr]{div}|
                [Ée][Cc][Hh][Aa][Nn][Gg][Ee][Uu][Rr]{div}|[Ée][Cc][Hh]{div}|
                [Ee][Nn][Dd]{div}|
                [Ee][Ss][Pp][Ll][Aa][Nn][Aa][Dd][Ee]{div}|[Ee][Ss][Pp][Ll]{div}|
                [Ee][Ss][Tt][Aa][Tt][Ee][Ss]?{div}|
                [Ee][Xx][Pp][Rr][Ee][Ss][Ss][Ww][Aa][Yy]{div}|[Ee][Xx][Pp][Yy]{div}|
                [Ee][Xx][Tt][Ee][Nn][Ss][Ii][Oo][Nn]{div}|[Ee][Xx][Tt][Ee][Nn]{div}|
                [Ff][Aa][Rr][Mm]{div}|
                [Ff][Ii][Ee][Ll][Dd]{div}|
                [Ff][Oo][Rr][Ee][Ss][Tt]{div}|
                [Ff][Rr][Ee][Ee][Ww][Aa][Yy]{div}|[Ff][Ww][Yy]{div}|
                [Ff][Rr][Oo][Nn][Tt]{div}|
                [Gg][Aa][Rr][Dd][Ee][Nn][Ss]{div}|[Gg][Dd][Nn][Ss]{div}|
                [Gg][Aa][Tt][Ee]{div}|
                [Gg][Ll][Aa][Dd][Ee]{div}|
                [Gg][Ll][Ee][Nn]{div}|
                [Gg][Rr][Ee][Ee][Nn]{div}|
                [Gg][Rr][Uo][Uu][Nn][Dd][Ss]{div}|[Gg][Rr][Nn][Dd][Ss]{div}|
                [Gg][Rr][Oo][Vv][Ee]{div}|
                [Hh][Aa][Rr][Bb][Oo][Uu][Rr]{div}|[Hh][Aa][Rr][Bb][Rr]{div}|
                [Hh][Ee][Aa][Tt][Hh]{div}|
                [Hh][Ee][Ii][Gg][Hh][Tt][Ss]{div}|[Hh][Tt][Ss]{div}|
                [Hh][Ii][Gg][Hh][Ll][Aa][Nn][Dd][Ss]{div}|[Hh][Gg][Hh][Ll][Dd][Sd]{div}|
                [Hh][Ii][Gg][Gh][Ww][Aa][Yy]{div}|[Hh][Ww][Yy]{div}|
                [Hh][Ii][Ll][Ll]{div}|
                [Hh][Oo][Ll][Ll][Oo][Ww]{div}|
                [Îi][Ll][Ee]{div}|
                [Ii][Mm][Pp][Aa][Ss][Ss][Ee]{div}|I[Mm][Pp]{div}|
                [Ii][Nn][Ll][Ee][Tt]{div}|
                [Ii][Ss][Ll][Aa][Nn][Dd]{div}|
                [Kk][Ee][Yy]{div}|
                [Kk][Nn][Oo][Ll][Ll]{div}|
                [Ll][Aa][Nn][Dd][Ii][Nn][Gg]{div}|[Ll][Aa][Nn][Dd][Nn][Gg]{div}|
                [Ll][Aa][Nn][Ee]{div}|
                [Ll][Ii][Mm][Ii][Tt][Ss]{div}|[Ll][Mm][Tt][Ss]{div}|
                [Ll][Ii][Nn][Ee]{div}|
                [Ll][Ii][Nn][Kk]{div}|
                [Ll][Oo][Oo][Kk][Oo][Uu][Tt]{div}|[Ll][Kk][Oo][Uu][Tt]{div}|
                [Mm][Aa][Ii][Nn][Ww][Aa][Yy]{div}|
                [Mm][Aa][Ll][Ll]{div}|
                [Mm][Aa][Nn][Oo][Rr]{div}|
                [Mm][Aa][Zz][Ee]{div}|
                [Mm][Ee][Aa][Dd][Oo][Ww]{div}|
                [Mm][Ee][Ww][Ss]{div}|
                [Mm][Oo][Nn][Tt][Éé][Ee]{div}|
                [Mm][Oo][Oo][Rr]{div}|
                [Mm][Oo][Uu][Nn][Tt][Aa][Ii][Nn]{div}|[Mm][Tt][Nn]{div}|
                [Mm][Oo][Uu][Nn][Tt]{div}|
                [Oo][Rr][Cc][Hh][Aa][Rr][Dd]{div}|[Oo][Rr][Cc][Hh]{div}|
                [Pp][Aa][Rr][Aa][Dd][Ee]{div}|
                [Pp][Aa][Rr][Cc]{div}|
                [Pp][Aa][Rr][Kk][Ww][Aa][Yy]{div}|[Pp][Kk][Yy]{div}|
                [Pp][Aa][Rr][Kk]{div}|[Pp][Kk]{div}|
                [Pp][Aa][Ss][Ss][Aa][Gg][Ee]{div}|[Pp][As][Ss][Ss]{div}|
                [Pp][Aa][Tt][Hh]{div}|
                [Pp][Aa][Tt][Hh][Ww][Aa][Yy]{div}|[Pp][Tt][Ww][Aa][Yy]{div}|
                [Pp][Ii][Nn][Ee][Ss]{div}|
                [Pp][Ll][Aa][Cc][Ee]{div}|[Pp][Ll]{div}|
                [Pp][Ll][Aa][Tt][Ee][Aa][Uu]{div}|[Pp][Ll][Aa][Tt]{div}|
                [Pp][Ll][Aa][Zz][Aa]{div}|
                [Pp][Oo][Ii][Nn][Tt][Ee]{div}|
                [Pp][Oo][Ii][Nn][Tt]{div}|[Pp][Tt]{div}|
                [Pp][Oo][Rr][Tt]{div}|
                [Pp][Rr][Ii][Vv][Aa][Tt][Ee]{div}|[Pp][Vv][Tt]{div}|
                [Pp][Rr][Oo][Mm][Ee][Nn][Aa][Dd][Ee]{div}|[Pp][Rr][Oo][Mm]{div}|
                [Qq][Uu][Aa][Ii]{div}|
                [Qq][Uu][Aa][Yy]{div}|
                [Rr][Aa][Mm][Pp]{div}|
                [Rr][Aa][Nn][Gg][Ee]{div}|[Rr][Gg]{div}|
                [Rr][Aa][Nn][Gg]{div}|
                [Rr][Ii][Dd][Gg][Ee]{div}|
                [Rr][Ii][Ss][Ee]{div}|
                [Rr][Oo][Aa][Dd]{div}|[Rr][Dd]{div}|
                [Rr][Oo][Nn][Dd]\-[Pp][Oo][Ii][Nn][Tt]{div}|[Rr][Dd][Pp][Tt]{div}|
                [Rr][Oo][Uu][Tt][Ee]{div}|[Rr][Tt][Ee]{div}|
                [Rr][Oo][Ww]{div}|
                [Rr][Uu][Ee][Ll][Ll][Ee]{div}|[Rr][Ll][Ee]{div}|
                [Rr][Uu][Ee]{div}|
                [Rr][Uu][Nn]{div}|
                [Ss][Ee][Nn][Tt][Ii][Ee][Rr]{div}|[Ss][Ee][Nn][Tt]{div}|
                # Street
                [Ss][Tt][Rr][Ee][Ee][Tt]{div}|[Ss][Tt](?![A-Za-z]){div}|
                # Square
                [Ss][Qq][Uu][Aa][Rr][Ee]{div}|[Ss][Qq]{div}|
                [Ss][Uu][Bb][Dd][Ii][Vv][Ii][Ss][Ii][Oo][Nn]{div}|[Ss][Uu][Bb][Dd][Ii][Vv]{div}|
                [Tt][Ee][Rr][Rr][Aa][Cc][Ee]{div}|[Tt][Ee][Re][Re]{div}|
                [Tt][Ee][Rr][Rr][Aa][Ss][Ss][Ee]{div}|[Tt][Ss][Ss][Es]{div}|
                [Tt][Hh][Ii][Cc][Kk][Ee][Tt]{div}|[Tt][Hh][Ii][Cc][Kk]{div}|
                [Tt][Oo][Ww][Ee][Rr][Ss]{div}|
                [Tt][Oo][Ww][Nn][Ll][Ii][Nn][Ee]{div}|[Tt][Ll][Ii][Nn][Ee]{div}|
                [Tt][Rr][Aa][Ii][Ll]{div}|
                [Tt][Uu][Rr][Nn][Aa][Bb][Oo][Uu][Tt]{div}|[Tt][Rr][Nn][Aa][Bb][Tt]{div}|
                [Vv][Aa][Ll][Ee]{div}|
                [Vv][Ii][Aa]{div}|
                [Vv][Ii][Ee][Ww]{div}|
                [Vv][Ii][Ll][Ll][Aa][Gg][Ee]{div}|[Vv][Ii][Ll][Ll][Gg][Ee]{div}|
                [Vv][Ii][Ll][Ll][Aa][Ss]{div}|
                [Vv][Ii][Ss][Tt][Aa]{div}|
                [Vv][Oo][Ii][Ee]{div}|
                [Ww][Aa][Ll][Lk]{div}|
                [Ww][Aa][Yy]{div}|
                [Ww][Hh][Aa][Rr][Ff]{div}|
                [Ww][Oo][Oo][Dd]{div}|
                [Ww][Yy][Nn][Dd]{div}
            )
            (?P<route_id>
                [\(\ \,]{route_symbols}
                [Rr][Oo][Uu][Tt][Ee]\ [A-Za-z0-9]+[\)\ \,]{route_symbols}
            )?
            """.format(div="[\.\ ,]{0,2}", route_symbols='{0,3}')

floor = r"""
            (?P<floor>
                (?:
                \d+[A-Za-z]{0,2}\.?\ [Ff][Ll][Oo][Oo][Rr]\ ?
                )
                |
                (?:
                    [Ff][Ll][Oo][Oo][Rr]\ \d+[A-Za-z]{0,2}\ ?
                )
            )
        """

building = r"""
            (?:
                (?:
                    (?:[Bb][Uu][Ii][Ll][Dd][Ii][Nn][Gg])
                    |
                    (?:[Bb][Ll][Dd][Gg])
                )
                \ \d{0,2}[A-Za-z]?
            )
            """

occupancy = r"""
            (?:
                (?:
                    (?:
                        #
                        # English
                        #
                        # Suite
                        [Ss][Uu][Ii][Tt][Ee]\ |[Ss][Tt][Ee]\.?\ 
                        |
                        # Apartment
                        [Aa][Pp][Tt]\.?\ |[Aa][Pp][Aa][Rr][Tt][Mm][Ee][Nn][Tt]\ 
                        |
                        # Room
                        [Rr][Oo][Oo][Mm]\ |[Rr][Mm]\.?\ 
                        |
                        # Unit
                        [Uu][Nn][Ii][Tt]\ 
                        |
                        #
                        # French
                        #
                        # Apartement
                        [Aa][Pp][Aa][Rr][Tt][Ee][Mm][Ee][Nn][Tt]\ |A[Pp][Pp]\ 
                        |
                        # Bureau
                        [Bb][Uu][Rr][Ee][Aa][Uu]\ 
                        |
                        # Unité
                        [Uu][Nn][Ii][Tt][Éé]\ 
                    )
                    (?:
                        [A-Za-z\#\&\-\d]{1,7}
                    )?
                )
                |
                (?:
                    \#[0-9]{,3}[A-Za-z]{1}
                )
            )\ ?
            """

po_box = r"""
            (?P<postal_box>
                # English - PO Box 123
                (?:[Pp]\.?\ ?[Oo]\.?\ [Bb][Oo][Xx]\ \d+)
                |
                # French - B.P. 123
                (?:[Bb]\.?\ [Pp]\.?\ \d+)
                |
                # C.P. 123
                (?:[Cc]\.?\ [Pp]\.?\ \d+)
                |
                # Case postale 123
                (?:[Cc]ase\ [Pp][Oo][Ss][Tt][Aa][Ll][Ee]\ \d+)
                |
                # C.P. 123
                (?:[Cc]\.[Pp]\.\ \d+)
            )
        """

'''Define detection rules for a second type of address format
   (the French one)
'''
street_number_b = re.sub('<([a-z\_]+)>', r'<\1_b>', street_number)
street_name_b = re.sub('<([a-z\_]+)>', r'<\1_b>', street_name)
street_type_b = re.sub('<([a-z\_]+)>', r'<\1_b>', street_type)
po_box_b = re.sub('<([a-z\_]+)>', r'<\1_b>', po_box)
post_direction_b = re.sub('<([a-z\_]+)>', r'<\1_b>', post_direction)

po_box_positive_lookahead = r"""
            (?=
                # English - PO Box 123
                (?:[Pp]\.?\ ?[Oo]\.?\ [Bb][Oo][Xx]\ \d+)
                |
                # French - B.P. 123
                (?:[Bb]\.?\ [Pp]\.?\ \d+)
                |
                # C.P. 123
                (?:[Cc]\.?\ [Pp]\.?\ \d+)
                |
                # Case postale 123
                (?:[Cc]ase\ [Pp][Oo][Ss][Tt][Aa][Ll][Ee]\ \d+)
                |
                # C.P. 123
                (?:[Cc]\.[Pp]\.\ \d+)
                |
                (?:[\ \,])
            )
        """

full_street = r"""
    (?:
        # Format commonly used in French
        (?P<full_street_b>

            {street_number_b}{div}
            {street_type_b}{div}
            ({street_name_b} {po_box_positive_lookahead})?\,?\ ?
            {post_direction_b}?\,?\ ?
            {po_box_b}?\,?\ ?
        )
        |
        # Format commonly used in English
        (?P<full_street>

            {street_number}\,?\ ?
            {street_name}?\,?\ ?
            (?:(?<=[\ \,]){street_type})\,?\ ?
            {post_direction}?\,?\ ?
            {floor}?\,?\ ?

            (?P<building_id>
                {building}
            )?\,?\ ?

            (?P<occupancy>
                {occupancy}
            )?\,?\ ?

            {po_box}?
        )
    )""".format(street_number=street_number,
                street_number_b=street_number_b,

                street_name=street_name,
                street_name_b=street_name_b,

                street_type=street_type,
                street_type_b=street_type_b,

                post_direction=post_direction,
                post_direction_b=post_direction_b,

                floor=floor,
                building=building,
                occupancy=occupancy,

                po_box=po_box,
                po_box_b=po_box_b,
                po_box_positive_lookahead=po_box_positive_lookahead,

                div='[\ ,]{1,2}',
                )

# region1 here is actually a "province"
region1 = r"""
        (?P<region1>
            (?:
                # province abbreviations (English)
                A\.?B\.?|B\.?C\.?|M\.?B\.?|N\.?B\.?|N\.?L\.?|
                N\.?T\.?|N\.?S\.?|N\.?U\.?|O\.?N\.?|P\.?E\.?|
                Q\.?C\.?|S\.?K\.?|Y\.?T\.?
            )
            |
            (?:
                # provinces full (English)
                [Aa][Ll][Bb][Ee][Rr][Tt][Aa]|
                [Bb][Rr][Ii][Tt][Ii][Ss][Hh]\ [Cc][Oo][Ll][Uu][Mm][Bb][Ii][Aa]|
                [Mm][Aa][Nn][Ii][Tt][Oo][Bb][Aa]|
                [Nn][Ee][Ww]\ [Bb][Rr][Uu][Nn][Ss][Ww][Ii][Cc][Kk]|
                [Nn][Ee][Ww][Ff][Oo][Uu][Nn][Dd][Ll][Aa][Nn][Dd]\ 
                [Aa][Nn][Dd]\ [Ll][Aa][Bb][Rr][Aa][Dd][Oo][Rr]|
                [Nn][Ee][Ww][Ff][Oo][Uu][Nn][Dd][Ll][Aa][Nn][Dd]\ 
                \&\ [Ll][Aa][Bb][Rr][Aa][Dd][Oo][Rr]|
                [Nn][Oo][Rr][Tt][Hh][Ww][Ee][Ss][Tt]\ 
                [Tt][Ee][Rr][Rr][Ii][Tt][Oo][Rr][Ii][Ee][Ss]|
                [Nn][Oo][Vv][Aa]\ [Ss][Cc][Oo][Tt][Ii][Aa]|
                [Nn][Uu][Nn][Aa][Vv][Uu][Tt]|
                [Oo][Nn][Tt][Aa][Rr][Ii][Oo]|
                [Pp][Rr][Ii][Nn][Cc][Ee]\ [Ee][Dd][Ww][Aa][Rr][Dd]\ 
                [Ii][Ss][Ll][Aa][Nn][Dd]|
                [Qq][Uu][Ee][Bb][Ee][Cc]|
                [Ss][Aa][Ss][Kk][Aa][Tt][Cc][Hh][Ee][Ww][Aa][Nn]|
                [Yy][Uu][Kk][Oo][Nn]|
                # provinces full (French)
                [Cc][Oo][Ll][Oo][Mm][Bb][Ii][Ee]\-
                [Bb][Rr][Ii][Tt][Aa][Nn]{1,2}[Ii][Qq][Eu][Ee]|
                [Nn][Oo][Uu][Vv][Ee][Aa][Uu]\-[Bb][Rr][Uu][Nn][Ss][Ww][Ii][Cc][Kk]|
                [Tt][Ee][Rr][Rr][Ee]\-[Nn][Ee][Uu][Vv][Ee]\-
                [Ee][Tt]\-[Ll][Aa][Bb][Rr][Aa][Dd][Oo][Rr]|
                [Tt][Ee][Rr][Rr][Ii][Tt][Oo][Ii][Rr][Ee][Ss]\ [Dd][Uu]\ 
                [Nn][Oo][Rr][Dd]\-[Oo][Uu][Ee][Ss][Tt]|
                [Nn][Oo][Uu][Vv][Ee][Ll][Ll][Ee]\-[ÉéEe][Cc][Oo][Ss][Ss][Ee]|
                [ÎîIi][Ll][Ee]\-[Dd][Uu]\-[Pp][Rr][Ii][Nn][Cc][Ee]\-
                [ÉéEe][Dd][Oo][Uu][Aa][Rr][Dd]|
                [Qq][Uu][Éé][Bb][Ee][Cc]
            )
        )
        """

city = r"""
        (?P<city>
            (?<=[\, ])[A-z]{1}(?![0-9]) # city second char should not be number
            [\w\ \-\'\.]{2,20}?(?=[\, ])
        )
        """

postal_code = r"""
            (?P<postal_code>
                (?:
                    [ABCEGHJKLMNPRSTVXY]\d[ABCEGHJKLMNPRSTVWXYZ]\ ?
                    \d[ABCEGHJKLMNPRSTVWXYZ]\d
                )
            )
            """

country = r"""
            (?:
                [Cc][Aa][Nn][Aa][Dd][Aa]
            )
            """

# define detection rules for postal code placed in different parts of address
postal_code_b = re.sub('<([a-z\_]+)>', r'<\1_b>', postal_code)
postal_code_c = re.sub('<([a-z\_]+)>', r'<\1_c>', postal_code)

full_address = r"""
                (?P<full_address>
                    {full_street} {div}
                    {city} {div}
                    (?:{postal_code_c} {div})?
                    \(?{region1}[\)\.]? {div}
                    (?:
                        (?:
                            {postal_code}? {div} {country}? 
                            (?:{div} {postal_code_b})?
                        )
                    )
                )
                """.format(
    full_street=full_street,
    div='[\, ]{,2}',
    city=city,
    region1=region1,

    country=country,
    country_b=country,

    postal_code=postal_code,
    postal_code_b=postal_code_b,
    postal_code_c=postal_code_c,
)
