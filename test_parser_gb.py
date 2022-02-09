# -*- coding: utf-8 -*-

""" Test for USA address parser """

import re
import pytest
import itertools
import pyap
import pyap.parser
from pyap import utils
from pyap.packages import six
import pyap.source_GB.data as data_gb


def execute_matching_test(input, expected, pattern):
    match = utils.match(pattern, input, re.VERBOSE)
    is_found = match is not None
    if expected:
        assert is_found == expected and match.group(0) == input
    else:
        assert (is_found == expected) or (match.group(0) != input)


@pytest.mark.parametrize("input,expected", [
    # positive assertions
    ("ZERO ", True),
    ("one ", True),
    ("two ", True),
    ("Three ", True),
    ("FoUr ", True),
    ("FivE ", True),
    ("six ", True),
    ("SEvEn ", True),
    ("Eight ", True),
    ("Nine ", True),
    # negative assertions
    ("Nidnes", False),
    ("One", False),
    ("two", False),
    ("onetwothree ", False),
])
def test_zero_to_nine(input, expected):
    ''' test string match for zero_to_nine '''
    execute_matching_test(input, expected, data_gb.zero_to_nine)


@pytest.mark.parametrize("input,expected", [
    # positive assertions
    ("tEN ", True),
    ("TWENTY ", True),
    ("tHirtY ", True),
    ("FOUrty ", True),
    ("fifty ", True),
    ("sixty ", True),
    ("seventy ", True),
    ("eighty ", True),
    ("NINety ", True),
    # negative assertions
    ("ten", False),
    ("twenTY", False),
    ("sixtysixsty ", False),
    ("one twenty ", False),
])
def test_ten_to_ninety(input, expected):
    ''' test string match for ten_to_ninety '''
    execute_matching_test(input, expected, data_gb.ten_to_ninety)


@pytest.mark.parametrize("input,expected", [
    # positive assertions
    ("Hundred ", True),
    ("HuNdred ", True),
    # negative assertions
    ("HuNDdred", False),
    ("HuNDdred hundred ", False),
])
def test_hundred(input, expected):
    ''' tests string match for a hundred '''
    execute_matching_test(input, expected, data_gb.hundred)


@pytest.mark.parametrize("input,expected", [
    # positive assertions
    ("Thousand ", True),
    ("thOUSAnd ", True),
    # negative assertions
    ("thousand", False),
    ("THoussand ", False),
    ("THoussand", False),
    ("THOUssand THoussand ", False),
])
def test_thousand(input, expected):
    ''' tests string match for a thousand '''
    execute_matching_test(input, expected, data_gb.thousand)


@pytest.mark.parametrize("input,expected", [
    # positive assertions (words)
    ("One Thousand And Fifty Nine ", True),
    ("Two hundred and fifty ", True),
    ("Three hundred four ", True),
    ("Thirty seven ", True),
    ("FIFTY One ", True),
    ("Three hundred Ten ", True),
    # positive assertions (numbers)
    ("1 ", True),
    ("15 ", True),
    ("44 ", True),
    ("256 ", True),
    ("256 ", True),
    ("1256 ", True),
    ("32457 ", True),
    ("32457", True),
    ("9652", True),
    ("Number 32457 ", True),
    ("NO. 32457 ", True),
    ("Num. 256 ", True),
    # negative assertions (words)
    ("ONE THousszz22and FIFTY and four onde", False),
    ("ONE one oNe and onE Three", False),
    # negative assertions (numbers)
    ("536233", False),
    ("111111", False),
    ("1111ss11", False),
    ("123 456", False),
])
def test_street_number(input, expected):
    ''' tests positive exact string match for a street number '''
    execute_matching_test(input, expected, data_gb.street_number)


@pytest.mark.parametrize("input,expected", [
    # positive assertions
    ("Northeast Kentucky Industrial ", True),
    ("One ", True),
    ("First ", True),
    ("Ave 123 ", True),
    ("Northeast 5 ", True),
    ("Loiret Boulevard", True),
    # negative assertions
    ("Northeast Kentucky Industrial Maple ", False),
    ("a", False),
    ("1", False),
    ("ab", False),
])
def test_street_name(input, expected):
    ''' tests positive exact string match for a street name '''
    # The `street_name` pattern refers to the `street_number` pattern and so I've inserted
    # a fake `street_number` pattern that matches to the space between characters `\b\B`
    fake_street_number_pattern = r'(?P<street_number>fake_street_number)'
    execute_matching_test("fake_street_number" + input, expected, fake_street_number_pattern + data_gb.street_name)


@pytest.mark.parametrize("input,expected", [
    # positive assertions
    ("N. ", True),
    ("N ", True),
    ("S ", True),
    ("West ", True),
    ("eASt ", True),
    ("NW ", True),
    ("SE ", True),
    # negative assertions
    ("NW.", False),
    ("NW. ", False),
    ("NS ", False),
    ("EW ", False),
])
def test_post_direction(input, expected):
    ''' tests string match for a post_direction '''
    execute_matching_test(input, expected, data_gb.post_direction)


@pytest.mark.parametrize("input,expected", [
    # positive assertions
    ("Street", True),
    ("St.", True),
    ("St.", True),
    ("Blvd.", True),
    ("Blvd.", True),
    ("LN", True),
    ("RD", True),
    ("Cir", True),
    ("Highway", True),
    ("Hwy", True),
    ("Ct", True),
    ("Sq.", True),
    ("LP.", True),
    ("LP.", True),
    ("Street", True),
    ("blvd", True),
    # negative assertions
    # TODO

])
def test_street_type(input, expected):
    ''' tests string match for a street id '''
    execute_matching_test(input, expected, data_gb.street_type)


@pytest.mark.parametrize("input,expected", [
    # positive assertions
    ("floor 3 ", True),
    ("floor 11 ", True),
    ("floor 15 ", True),
    ("1st floor ", True),
    ("2nd floor ", True),
    ("15th floor ", True),
    ("16th. floor ", True),
    # negative assertions
    ("16th.floor ", False),
    ("1stfloor ", False),

])
def test_floor(input, expected):
    ''' tests string match for a floor '''
    execute_matching_test(input, expected, data_gb.floor)


@pytest.mark.parametrize("input,expected", [
    # positive assertions
    ("bldg m ", True),
    ("Building F ", True),
    ("bldg 2 ", True),
    ("building 3 ", True),
    ("building 100 ", True),
    ("Building ", True),
    ("building one ", True),
    ("Building three ", True),
    # negative assertions
    ("bldg", False),
    ("bldgm", False),
    ("bldg100 ", False),

])
def test_building(input, expected):
    ''' tests string match for a building '''
    execute_matching_test(input, expected, data_gb.building)


@pytest.mark.parametrize("input,expected", [
    # positive assertions
    ("suite 900 ", True),
    ("Suite #2 ", True),
    ("suite #218 ", True),
    ("suite J7 ", True),
    ("suite 102A ", True),
    ("suite a&b ", True),
    ("Suite J#200 ", True),
    ("suite 710-327 ", True),
    ("Suite A ", True),
    ("ste A ", True),
    ("Ste 101 ", True),
    ("ste 502b ", True),
    ("ste 14-15 ", True),
    ("ste E ", True),
    ("ste 9E ", True),
    ("Suite 1800 ", True),
    ("Apt 1B ", True),
    ("Rm. 52 ", True),
    ("Flat 2C ", True),
    ("Flat 81b ", True),
    ("Flat 52 ", True),
    ("Flat 546 ", True),
    ("Flat 14 ", True),
    ("Suite#2", True),
    ("suite900 ", True),
    ("suite218 ", True),
    ("1 ", False),
    ("1A ", False),
    ("12 ", False),
    ("123 ", False),
])
def test_occupancy(input, expected):
    ''' tests exact string match for a place id '''
    execute_matching_test(input, expected, data_gb.occupancy)


@pytest.mark.parametrize("input,expected", [
    # positive assertions
    ("po box 108", True),
    ("Po Box 53485", True),
    ("P.O. box 119", True),
    ("PO box 1070", True),
    ("po box108", True),
    ("PoBox53485", True),  # While not correctly formatted, this is clearly a PO Box
    ("P.O. box119", True),
    # negitive assertions
    ("POb ox1070", False),
    ("boxer 123", False),
])
def test_po_box_negative(input, expected):
    ''' tests string match for a po box '''
    execute_matching_test(input, expected, data_gb.po_box)


@pytest.mark.parametrize("input,expected", [
    # positive assertions
    ("9652 Loiret Boulevard", True),
    ("101 MacIntosh Boulevard", True),
    ("1 West Hegeler Lane", True),
    ("1270 Leeds Avenue", True),
    ("85-1190 Ranchview Rd. NW ", True),
    ("62 Portland Road", True),
    ("Suite 514, 200 N. Pine Avenue ", True),
    ("200 S. Alloy Drive", True),
    ("Two Hundred S. Alloy Drive", True),
    ("Two Hundred South Alloy Drive", True),
    ("Two Hundred South Alloy Dr.", True),
    ("11001 Fondren Rd.", True),
    ("Suite 500, 9606 North Mopac Expressway", True),
    ("9692 East Arapahoe Road", True),
    ("Building 2, 9 Grand Avenue", True),
    ("9C Grand Avenue", True),
    ("Flat 2, 9 Grand Avenue", True),
    ("Suite 1800 233 Richmond Highway", True),
    ("P.O. Box 472, 354 Eisenhower Parkway ", True),
    ("PO Box 2243, 6645 N Ensign St", True),
    ("POBox 2243, 6645 N Ensign St", True),
    ("1200 Old Fairhaven Pkwy", True),
    ("1659 Scott Blvd", True),
    ("377 Fisher Rd", True),
    ("1833 Stearman Ave", True),
    ("1737 S Lumpkin St ", True),
    ("101 N Court Sq", True),
    ("1790 Yardley Langhorne Rd", True),
    ("280 West Main Street", True),
    ("701 Tennessee Walk", True),
    ("7457 Harwin Dr", True),
    ("700 Davis Avenue", True),
    ("1 W 47th St", True),
    ("832 Seward St", True),
    ("2740 Timber Ridge Lane", True),
    ("810 E Western Ave", True),
    ("6223 Richmond Ave", True),
    ("400 Middle Street", True),
    ("81 N Main St", True),
    ("3705 West Memorial Road", True),
    ("4911 Matterhorn Dr", True),
    ("5830 Yahl Street", True),
    ("9400 Doliver Dr", True),
    ("10701 Stirling Road", True),
    ("1865 Corporate Dr", True),
    ("80 Beaman Rd", True),
    ("9691 Spratley Ave", True),
    ("10835 New Haven Rd NW ", True),
    ("320 W Broussard Rd", True),
    ("9001 Any Old Way", True),
    ("8967 Market St.", True),
    ("3724 Oxford Blvd.", True),
    ("901 Rainier Ave S ", True),
    ("01 Brett Street", True),
    ("Flat 14, Hilary road", True),
    ("049 Maurice island", True),
    ("Flat 81b, Abbie estate", True),
    ("SHEPPEY WAY", True),
    ("185-187 OXFORD STREET", True),
    ("32 London Bridge St", True),
    ("Marlborough Rd", True),
    ("Gresham Street", True),
    ("Corn St", True),
    ("223 30th Ave.", True),
    ("No. 22 The Light", True),
    ("55 Glenfada Park", True),

])
def test_full_street(input, expected):
    ''' tests exact string match for a full street '''
    execute_matching_test(input, expected, data_gb.full_street)


@pytest.mark.parametrize("input,expected", [
    # positive assertions
    ("BX1 1LT", True),
    ("sw1A 0AA", True),
    ("EC2V 7hh", True),
    ("M25DB", True),
    ("eh12ng", True),
    ("BT1 5GS", True),

    # negative assertions
    ("1", False),
    ("23", False),
    ("456", False),
    ("4567", False),
    ("750621", False),
    ("95130-642", False),
    ("95130-64212", False),
])
def test_postal_code(input, expected):
    ''' test exact string match for postal code '''
    execute_matching_test(input, expected, data_gb.postal_code)


@pytest.mark.parametrize("input,expected", [
    # positive assertions
    ("Montana", True),
    ("Nebraska", True),
    ("NJ", True),
    ("DC", True),
    ("PuErTO RIco", True),
    ("oregon", True),
    ("Surrey", True),
    ("Middlesex", True),
    ("Greater London", True),
])
def test_region1(input, expected):
    ''' test exact string match for province '''
    execute_matching_test(input, expected, data_gb.region1)


@pytest.mark.parametrize("input,expected", [
    # positive assertions
    ("England", True),
    ("ScoTlAnd", True),
    ("wales", True),
    ("CYMRU", True),
    ("United Kingdom", True),
    ("Great Britain", True),
    ("Britain", True),
    ("Britain and Northern Ireland", True),
    ("Great Britain and Northern Ireland", True),
    ("The United Kingdom of Great Britain and Northern Ireland", True),
    ("United States", False),
])
def test_country(input, expected):
    ''' test exact string match for country '''
    execute_matching_test(input, expected, data_gb.country)


@pytest.mark.parametrize("input,expected", [
    # positive assertions
    ("11-59 High Road, East Finchley London, N2 8AW", True),
    ("88 White parkway, Stanleyton, L2 3DB", True),
    ("Studio 96D, Graham roads, Westtown, L1A 3GP, Great Britain", True),
    ("01 Brett mall, Lake Donna, W02 3JQ", True),
    ("Flat 05, Byrne shores, Howardshire, GL6 8EA, UK", True),
    ("12 Henry route, Clementsborough, W2 5DQ", True),
    ("195 Jill hollow, Harryside, TF6 4YD, England", True),
    ("195 Jill hollow, TF6 4YD", True),
    ("SHEPPEY WAY, SITTINGBOURNE, ME9 8RZ", True),
    ("185-187 OXFORD STREET, WESTMINSTER, W1D 2JU", True),
    ("32 London Bridge St, London SE1 9SG", True),
    ("Marlborough Rd, St. James's, London SW1A 1BQ", True),
    ("Guildhall, Gresham Street, London, EC2V 7HH", True),
    ("The Corn Exchange, Corn St, Bristol BS1 1JQ", True),
    ("No. 22 The Light, The Headrow, Leeds LS1 8TL", True),
    ("55 Glenfada Park, Londonderry BT48 9DR", True),
    ("Studio 53, Harrison cove, Smithbury, G88 4US", True),
    ("Floor 4, 32 London Bridge St, London SE1 9SG", True),
    ("4th Floor, 32 London Bridge St, London SE1 9SG", True),
    # negative assertions
    ("85 STEEL REGULAR SHAFT - NE", False),
    ("3 STRUCTURE WITH PE", False),
    ("2013 Courtesy of DONNA LUPI, PR", False),
    ("44 sq. ft. 000 Columbia Ave. See Remarks, Newfield, NJ 08344", False),
    ("7901 SILVER CONDUCTIVE HOLE FILL MA", False),
    ("3 THIRD PARTY LIST IN", False),
    ("9 STORAGE OF INDIVIDUAL IN", False),
    ("4 BODY WAVE MODEL MO", False),
    ("4060 AUTOMATIC STRAPPING MACHINE KZB-II STRAPPING MA", False),
    ("130 AUTOMATIC STRAPPING MACHINE CO", False),
    ("6060 AUTOMATIC STRAPPING MACHINE SK", False),
    ("500 AUTO BLISTER PACKING SEALING MA", False),
    ("23 ELECTRICAL COLOURED-TAPE PR", False),
    ("1900 TRANSISTOR ELECTROMAGNETIC INDUCTION AL", False),
    ("3131 DR. MATTHEW WI", False),
    ("ONE FOR ANY DIRECT, INDIRECT, IN", False),
    ("2 TRACTOR HEAD Actros MP", False),
    ("00 Straight Fit Jean, USA", False),
])
def test_full_address(input, expected):
    ''' tests exact string match for a full address '''
    execute_matching_test(input, expected, data_gb.full_address)

def test_full_address_parts():
    """Tests that the right parts of the address are picked up by the right regex"""
    example_addresses = [
        {
            'full_address': '9 Shaun glen, East Joan, LN4 1LE',
            'street_name': 'Shaun glen',
            'street_number': '9',
            'postal_code': 'LN4 1LE',
        },
        {
            'full_address': '11-59 High Road\nEast Finchley London\nN2 8AW, UK',
            'street_name': 'High Road',
            'street_number': '11-59',
            'postal_code': 'N2 8AW',
            'country': 'UK',
        },
        {
            'full_address': 'Studio 53, Harrison cove, Smithbury, G88 4US, United Kingdom',
            'occupancy': 'Studio 53',
            'street_name': 'Harrison cove',
            'postal_code': 'G88 4US',
            'country': 'United Kingdom',
        },
    ]
    filler_text = "This is filler text that can be inserted both before and after addresses"
    punctuation = ["\n", ", ", ". ", " "]

    # Test each of the above addresses
    for address_parts in example_addresses:
        # Test with filler text before and after the address
        for filler_before, filler_after in itertools.product([False, True], [False, True]):
            # Use the following punctuation to join the filler text and the address
            for join_string in punctuation:
                filler_text_before = (filler_text + join_string) if filler_before else ''
                filler_text_after = (join_string + filler_text) if filler_after else ''
                address_text = filler_text_before + address_parts['full_address'] + filler_text_after

                parsed = pyap.parse(address_text, country='GB')
                print (pyap.parser.AddressParser._normalize_string(address_text))
                # Ensure that only one address is found
                assert len(parsed) == 1
                for k, v in six.iteritems(address_parts):
                    if k == 'full_address':
                        assert parsed[0].full_address == pyap.parser.AddressParser._normalize_string(v)
                    else:
                        # assert that every item in the above address dictionaries match the parsed address
                        assert parsed[0].__getattribute__(k) == v

