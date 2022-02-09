# -*- coding: utf-8 -*-

"""
    pyap.source_US.data
    ~~~~~~~~~~~~~~~~~~~~

    This module provides regular expression definitions required for
    detecting US addresses.

    The module is expected to always contain 'full_address' variable containing
    all address parsing definitions.

    :copyright: (c) 2015 by Vladimir Goncharov.
    :license: MIT, see LICENSE for more details.
"""

import string


'''Numerals from one to nine
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
    )"""

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
   c) - "85 1190"
'''
street_number = r"""(?P<street_number>
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
                        (?:\d{from_to}
                            (?:\ ?\-?\ ?\d{from_to})?\ 
                        )
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
                  [a-zA-Z0-9\ \.]{3,31}  # Seems like the longest US street is
                                         # 'Northeast Kentucky Industrial Parkway'
                                         # https://atkinsbookshelf.wordpress.com/tag/longest-street-name-in-us/
                 )
              """

post_direction = r"""
                    (?P<post_direction>
                        (?:
                            [Nn][Oo][Rr][Tt][Hh]\ |
                            [Ss][Oo][Uu][Tt][Hh]\ |
                            [Ee][Aa][Ss][Tt]\ |
                            [Ww][Ee][Ss][Tt]\ 
                        )
                        |
                        (?:
                            NW\ |NE\ |SW\ |SE\ 
                        )
                        |
                        (?:
                            N\.?\ |S\.?\ |E\.?\ |W\.?\ 
                        )
                    )
                """

# This list was taken from: https://pe.usps.com/text/pub28/28apc_002.htm
# Broadway and Lp (abbreviation for Loop) were added to the list
street_type_list = [
    'Allee', 'Alley', 'Ally', 'Aly', 'Anex', 'Annex',
    'Annx', 'Anx', 'Arc', 'Arcade', 'Av', 'Ave',
    'Aven', 'Avenu', 'Avenue', 'Avn', 'Avnue', 'Bayoo',
    'Bayou', 'Bch', 'Beach', 'Bend', 'Bg', 'Bgs',
    'Blf', 'Blfs', 'Bluf', 'Bluff', 'Bluffs', 'Blvd',
    'Bnd', 'Bot', 'Bottm', 'Bottom', 'Boul', 'Boulevard',
    'Boulv', 'Br', 'Branch', 'Brdge', 'Brg', 'Bridge',
    'Brk', 'Brks', 'Brnch', 'Broadway', 'Brook', 'Brooks',
    'Btm', 'Burg', 'Burgs', 'Byp', 'Bypa', 'Bypas',
    'Bypass', 'Byps', 'Byu', 'Camp', 'Canyn', 'Canyon',
    'Cape', 'Causeway', 'Causwa', 'Cen', 'Cent', 'Center',
    'Centers', 'Centr', 'Centre', 'Cir', 'Circ', 'Circl',
    'Circle', 'Circles', 'Cirs', 'Clb', 'Clf', 'Clfs',
    'Cliff', 'Cliffs', 'Club', 'Cmn', 'Cmns', 'Cmp',
    'Cnter', 'Cntr', 'Cnyn', 'Common', 'Commons', 'Cor',
    'Corner', 'Corners', 'Cors', 'Course', 'Court', 'Courts',
    'Cove', 'Coves', 'Cp', 'Cpe', 'Crcl', 'Crcle',
    'Creek', 'Cres', 'Crescent', 'Crest', 'Crk', 'Crossing',
    'Crossroad', 'Crossroads', 'Crse', 'Crsent', 'Crsnt', 'Crssng',
    'Crst', 'Cswy', 'Ct', 'Ctr', 'Ctrs', 'Cts',
    'Curv', 'Curve', 'Cv', 'Cvs', 'Cyn', 'Dale',
    'Dam', 'Div', 'Divide', 'Dl', 'Dm', 'Dr',
    'Driv', 'Drive', 'Drives', 'Drs', 'Drv', 'Dv',
    'Dvd', 'Est', 'Estate', 'Estates', 'Ests', 'Exp',
    'Expr', 'Express', 'Expressway', 'Expw', 'Expy', 'Ext',
    'Extension', 'Extensions', 'Extn', 'Extnsn', 'Exts', 'Fall',
    'Falls', 'Ferry', 'Field', 'Fields', 'Flat', 'Flats',
    'Fld', 'Flds', 'Fls', 'Flt', 'Flts', 'Ford',
    'Fords', 'Forest', 'Forests', 'Forg', 'Forge', 'Forges',
    'Fork', 'Forks', 'Fort', 'Frd', 'Frds', 'Freeway',
    'Freewy', 'Frg', 'Frgs', 'Frk', 'Frks', 'Frry',
    'Frst', 'Frt', 'Frway', 'Frwy', 'Fry', 'Ft',
    'Fwy', 'Garden', 'Gardens', 'Gardn', 'Gateway', 'Gatewy',
    'Gatway', 'Gdn', 'Gdns', 'Glen', 'Glens', 'Gln',
    'Glns', 'Grden', 'Grdn', 'Grdns', 'Green', 'Greens',
    'Grn', 'Grns', 'Grov', 'Grove', 'Groves', 'Grv',
    'Grvs', 'Gtway', 'Gtwy', 'Harb', 'Harbor', 'Harbors',
    'Harbr', 'Haven', 'Hbr', 'Hbrs', 'Heights', 'Highway',
    'Highwy', 'Hill', 'Hills', 'Hiway', 'Hiwy', 'Hl',
    'Hllw', 'Hls', 'Hollow', 'Hollows', 'Holw', 'Holws',
    'Hrbor', 'Ht', 'Hts', 'Hvn', 'Hway', 'Hwy',
    'Inlet', 'Inlt', 'Is', 'Island', 'Islands', 'Isle',
    'Isles', 'Islnd', 'Islnds', 'Iss', 'Jct', 'Jction',
    'Jctn', 'Jctns', 'Jcts', 'Junction', 'Junctions', 'Junctn',
    'Juncton', 'Key', 'Keys', 'Knl', 'Knls', 'Knol',
    'Knoll', 'Knolls', 'Ky', 'Kys', 'Lake', 'Lakes',
    'Land', 'Landing', 'Lane', 'Lck', 'Lcks', 'Ldg',
    'Ldge', 'Lf', 'Lgt', 'Lgts', 'Light', 'Lights',
    'Lk', 'Lks', 'Ln', 'Lndg', 'Lndng', 'Loaf',
    'Lock', 'Locks', 'Lodg', 'Lodge', 'Loop', 'Loops',
    'Lp', 'Mall', 'Manor', 'Manors', 'Mdw', 'Mdws',
    'Meadow', 'Meadows', 'Medows', 'Mews', 'Mill', 'Mills',
    'Mission', 'Missn', 'Ml', 'Mls', 'Mnr', 'Mnrs',
    'Mnt', 'Mntain', 'Mntn', 'Mntns', 'Motorway', 'Mount',
    'Mountain', 'Mountains', 'Mountin', 'Msn', 'Mssn', 'Mt',
    'Mtin', 'Mtn', 'Mtns', 'Mtwy', 'Nck', 'Neck',
    'Opas', 'Orch', 'Orchard', 'Orchrd', 'Oval', 'Overpass',
    'Ovl', 'Park', 'Parks', 'Parkway', 'Parkways', 'Parkwy',
    'Pass', 'Passage', 'Path', 'Paths', 'Pike', 'Pikes',
    'Pine', 'Pines', 'Pkway', 'Pkwy', 'Pkwys', 'Pky',
    'Pl', 'Place', 'Plain', 'Plains', 'Plaza', 'Pln',
    'Plns', 'Plz', 'Plza', 'Pne', 'Pnes', 'Point',
    'Points', 'Port', 'Ports', 'Pr', 'Prairie', 'Prk',
    'Prr', 'Prt', 'Prts', 'Psge', 'Pt', 'Pts',
    'Rad', 'Radial', 'Radiel', 'Radl', 'Ramp', 'Ranch',
    'Ranches', 'Rapid', 'Rapids', 'Rd', 'Rdg', 'Rdge',
    'Rdgs', 'Rds', 'Rest', 'Ridge', 'Ridges', 'Riv',
    'River', 'Rivr', 'Rnch', 'Rnchs', 'Road', 'Roads',
    'Route', 'Row', 'Rpd', 'Rpds', 'Rst', 'Rte',
    'Rue', 'Run', 'Rvr', 'Shl', 'Shls', 'Shoal',
    'Shoals', 'Shoar', 'Shoars', 'Shore', 'Shores', 'Shr',
    'Shrs', 'Skwy', 'Skyway', 'Smt', 'Spg', 'Spgs',
    'Spng', 'Spngs', 'Spring', 'Springs', 'Sprng', 'Sprngs',
    'Spur', 'Spurs', 'Sq', 'Sqr', 'Sqre', 'Sqrs',
    'Sqs', 'Squ', 'Square', 'Squares', 'St', 'Sta',
    'Station', 'Statn', 'Stn', 'Str', 'Stra', 'Strav',
    'Straven', 'Stravenue', 'Stravn', 'Stream', 'Street', 'Streets',
    'Streme', 'Strm', 'Strt', 'Strvn', 'Strvnue', 'Sts',
    'Sumit', 'Sumitt', 'Summit', 'Ter', 'Terr', 'Terrace',
    'Throughway', 'Tpke', 'Trace', 'Traces', 'Track', 'Tracks',
    'Trafficway', 'Trail', 'Trailer', 'Trails', 'Trak', 'Trce',
    'Trfy', 'Trk', 'Trks', 'Trl', 'Trlr', 'Trlrs',
    'Trls', 'Trnpk', 'Trwy', 'Tunel', 'Tunl', 'Tunls',
    'Tunnel', 'Tunnels', 'Tunnl', 'Turnpike', 'Turnpk', 'Un',
    'Underpass', 'Union', 'Unions', 'Uns', 'Upas', 'Valley',
    'Valleys', 'Vally', 'Vdct', 'Via', 'Viadct', 'Viaduct',
    'View', 'Views', 'Vill', 'Villag', 'Village', 'Villages',
    'Ville', 'Villg', 'Villiage', 'Vis', 'Vist', 'Vista',
    'Vl', 'Vlg', 'Vlgs', 'Vlly', 'Vly', 'Vlys',
    'Vst', 'Vsta', 'Vw', 'Vws', 'Walk', 'Walks',
    'Wall', 'Way', 'Ways', 'Well', 'Wells', 'Wl',
    'Wls', 'Wy', 'Xing', 'Xrd', 'Xrds',
]


def street_type_list_to_regex(street_type_list):
    """Converts a list of street types into a regex"""
    street_types = '|'.join(set(street_type_list)).lower()
    for letter in string.ascii_lowercase:
        street_types = street_types.replace(letter, '[{upper}{lower}]'.format(upper=letter.upper(), lower=letter))

    # Use \b to check that there are word boundaries before and after the street type
    # Optionally match zero to two of " ", ",", or "." after the street name
    street_types = street_types.replace('|', r'\b{div}|\b')
    street_types = r'\b' + street_types + r'\b{div}'
    return street_types.format(
        div=r'[\.\ ,]{0,2}',
    )


# Regexp for matching street type
street_type = r"""
            (?:
                (?P<street_type>
                    {street_types}
                )
                (?P<route_id>
                    [\(\ \,]{route_symbols}
                    [Rr][Oo][Uu][Tt][Ee]\ [A-Za-z0-9]+[\)\ \,]{route_symbols}
                )?
            )
""".format(
    route_symbols='{0,3}',
    street_types=street_type_list_to_regex(street_type_list),
)

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
            (?P<building_id>
                (?:
                    (?:[Bb][Uu][Ii][Ll][Dd][Ii][Nn][Gg])
                    |
                    (?:[Bb][Ll][Dd][Gg])
                )
                \ 
                (?:
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
                    ){{1,5}}
                    |
                    \d{{0,4}}[A-Za-z]?
                )
                \ ?
            )
            """.format(thousand=thousand,
                       hundred=hundred,
                       zero_to_nine=zero_to_nine,
                       ten_to_ninety=ten_to_ninety,
                       )

occupancy = r"""
            (?P<occupancy>
                (?:
                    (?:
                        (?:
                            # Suite
                            [Ss][Uu][Ii][Tt][Ee]\ |[Ss][Tt][Ee]\.?\ 
                            |
                            # Apartment
                            [Aa][Pp][Tt]\.?\ |[Aa][Pp][Aa][Rr][Tt][Mm][Ee][Nn][Tt]\ 
                            |
                            # Room
                            [Rr][Oo][Oo][Mm]\ |[Rr][Mm]\.?\ 
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
            )
            """

po_box = r"""
            (?:
                [Pp]\.?\ ?[Oo]\.?\ [Bb][Oo][Xx]\ \d+
            )
        """

full_street = r"""
    (?:
        (?P<full_street>
            {street_number}
            {street_name}?\,?\ ?
            (?:[\ \,]{street_type})\,?\ ?
            {post_direction}?\,?\ ?
            {floor}?\,?\ ?
            {building}?\,?\ ?
            {occupancy}?\,?\ ?
            {po_box}?
        )
    )""".format(street_number=street_number,
                street_name=street_name,
                street_type=street_type,
                post_direction=post_direction,
                floor=floor,
                building=building,
                occupancy=occupancy,
                po_box=po_box,
                )

# region1 is actually a "state"
region1 = r"""
        (?P<region1>
            (?:
                # states abbreviations
                AL|AK|AZ|AR|CA|CO|CT|DE|DC|FL|GA|HI|ID|IL|IN|IA|KS|KY|LA|ME|MD|MA|MI|
                MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|OH|OK|OR|PA|RI|SC|SD|TN|TX|UT|VT|
                VA|WA|WV|WI|WY|
                # unincorporated & commonwealth territories
                AS|GU|MP|PR|VI
            )
            |
            (?:
                # states full
                [Aa][Ll][Aa][Bb][Aa][Mm][Aa]|
                [Aa][Ll][Aa][Ss][Kk][Aa]|
                [Aa][Rr][Ii][Zz][Oo][Nn][Aa]|
                [Aa][Rr][Kk][Aa][Nn][Ss][Aa][Ss]|
                [Cc][Aa][Ll][Ii][Ff][Oo][Rr][Nn][Ii][Aa]|
                [Cc][Oo][Ll][Oo][Rr][Aa][Dd][Oo]|
                [Cc][Oo][Nn][Nn][Ee][Cc][Tt][Ii][Cc][Uu][Tt]|
                [Dd][Ee][Ll][Aa][Ww][Aa][Rr][Ee]|
                [Dd][Ii][Ss][Tt][Rr][Ii][Cc][Tt]\ [Oo][Ff]\ 
                [Cc][Oo][Ll][Uu][Mm][Bb][Ii][Aa]|
                [Ff][Ll][Oo][Rr][Ii][Dd][Aa]|
                [Gg][Ee][Oo][Rr][Gg][Ii][Aa]|
                [Hh][Aa][Ww][Aa][Ii][Ii]|
                [Ii][Dd][Aa][Hh][Oo]|
                [Ii][Ll][Ll][Ii][Nn][Oo][Ii][Ss]|
                [Ii][Nn][Dd][Ii][Aa][Nn][Aa]|
                [Ii][Oo][Ww][Aa]|
                [Kk][Aa][Nn][Ss][Aa][Ss]|
                [Kk][Ee][Nn][Tt][Uu][Cc][Kk][Yy]|
                [Ll][Oo][Uu][Ii][Ss][Ii][Aa][Nn][Aa]|
                [Mm][Aa][Ii][Nn][Ee]|
                [Mm][Aa][Rr][Yy][Ll][Aa][Nn][Dd]|
                [Mm][Aa][Ss][Ss][Aa][Cc][Hh][Uu][Ss][Ee][Tt][Tt][Ss]|
                [Mm][Ii][Cc][Hh][Ii][Gg][Aa][Nn]|
                [Mm][Ii][Nn][Nn][Ee][Ss][Oo][Tt][Aa]|
                [Mm][Ii][Ss][Ss][Ii][Ss][Ss][Ii][Pp][Pp][Ii]|
                [Mm][Ii][Ss][Ss][Oo][Uu][Rr][Ii]|
                [Mm][Oo][Nn][Tt][Aa][Nn][Aa]|
                [Nn][Ee][Bb][Rr][Aa][Ss][Kk][Aa]|
                [Nn][Ee][Vv][Aa][Dd][Aa]|
                [Nn][Ee][Ww]\ [Hh][Aa][Mm][Pp][Ss][Hh][Ii][Rr][Ee]|
                [Nn][Ee][Ww]\ [Jj][Ee][Rr][Ss][Ee][Yy]|
                [Nn][Ee][Ww]\ [Mm][Ee][Xx][Ii][Cc][Oo]|
                [Nn][Ee][Ww]\ [Yy][Oo][Rr][Kk]|
                [Nn][Oo][Rr][Tt][Hh]\ [Cc][Aa][Rr][Oo][Ll][Ii][Nn][Aa]|
                [Nn][Oo][Rr][Tt][Hh]\ [Dd][Aa][Kk][Oo][Tt][Aa]|
                [Oo][Hh][Ii][Oo]|
                [Oo][Kk][Ll][Aa][Hh][Oo][Mm][Aa]|
                [Oo][Rr][Ee][Gg][Oo][Nn]|
                [Pp][Ee][Nn][Nn][Ss][Yy][Ll][Vv][Aa][Nn][Ii][Aa]|
                [Rr][Hh][Oo][Dd][Ee]\ [Ii][Ss][Ll][Aa][Nn][Dd]|
                [Ss][Oo][Uu][Tt][Hh]\ [Cc][Aa][Rr][Oo][Ll][Ii][Nn][Aa]|
                [Ss][Oo][Uu][Tt][Hh]\ [Dd][Aa][Kk][Oo][Tt][Aa]|
                [Tt][Ee][Nn][Nn][Ee][Ss][Ss][Ee][Ee]|
                [Tt][Ee][Xx][Aa][Ss]|
                [Uu][Tt][Aa][Hh]|
                [Vv][Ee][Rr][Mm][Oo][Nn][Tt]|
                [Vv][Ii][Rr][Gg][Ii][Nn][Ii][Aa]|
                [Ww][Aa][Ss][Hh][Ii][Nn][Gg][Tt][Oo][Nn]|
                [Ww][Ee][Ss][Tt]\ [Vv][Ii][Rr][Gg][Ii][Nn][Ii][Aa]|
                [Ww][Ii][Ss][Cc][Oo][Nn][Ss][Ii][Nn]|
                [Ww][Yy][Oo][Mm][Ii][Nn][Gg]|
                # unincorporated & commonwealth territories
                [Aa][Mm][Ee][Rr][Ii][Cc][Aa][Nn]\ [Ss][Aa][Mm][Oo][Aa]
                |[Gg][Uu][Aa][Mm]|
                [Nn][Oo][Rr][Tt][Hh][Ee][Rr][Nn]\ [Mm][Aa][Rr][Ii][Aa][Nn][Aa]\ 
                [Ii][Ss][Ll][Aa][Nn][Dd][Ss]|
                [Pp][Uu][Ee][Rr][Tt][Oo]\ [Rr][Ii][Cc][Oo]|
                [Vv][Ii][Rr][Gg][Ii][Nn]\ [Ii][Ss][Ll][Aa][Nn][Dd][Ss]
            )
        )
        """

# TODO: doesn't catch cities containing French characters
city = r"""
        (?P<city>
            [A-Za-z]{1}[a-zA-Z\ \-\'\.]{2,20}
        )
        """

postal_code = r"""
            (?P<postal_code>
                (?:\d{5}(?:\-\d{4})?)
            )
            """

country = r"""
            (?:
                [Uu]\.?[Ss]\.?[Aa]\.?|
                [Uu][Nn][Ii][Tt][Ee][Dd]\ [Ss][Tt][Aa][Tt][Ee][Ss](?:\ [Oo][Ff]\ [Aa][Mm][Ee][Rr][Ii][Cc][Aa])?
            )
            """

full_address = r"""
                (?P<full_address>
                    {full_street} {div}
                    {city} {div}
                    {region1} {div}
                    (?:
                        (?:{postal_code}?(\ ?,?{country})?)
                    )
                )
                """.format(
    full_street=full_street,
    div=r'[\, ]{,2}',
    city=city,
    region1=region1,
    country=country,
    postal_code=postal_code,
)
