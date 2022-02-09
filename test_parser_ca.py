# -*- coding: utf-8 -*-

""" Tests for CANADA address parser """

import re
import pytest
import pyap.source_CA.data as data_ca
from pyap import utils


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
    is_found = utils.match(
        data_ca.zero_to_nine,
        input,
        re.VERBOSE) is not None
    assert is_found == expected


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
    is_found = utils.match(data_ca.ten_to_ninety, input, re.VERBOSE)\
        is not None
    assert is_found == expected


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
    is_found = utils.match(data_ca.hundred, input, re.VERBOSE) is not None
    assert is_found == expected


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
    is_found = utils.match(data_ca.thousand, input, re.VERBOSE) is not None
    assert is_found == expected


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
    # positive assertions (street intersections)
    ("718 - 8th ", True),
])
def test_street_number_positive(input, expected):
    ''' tests positive exact string match for a street number '''
    match = utils.match(data_ca.street_number, input, re.VERBOSE)
    is_found = match is not None
    # check for exact match
    assert (is_found == expected) and\
           (match.group(0) == utils.unicode_str(input))


@pytest.mark.parametrize("input,expected", [
    # negative assertions (words)
    ("ONE THousszz22and FIFTY and four onde", False),
    ("ONE one oNe and onE Three", False),
    # negative assertions (numbers)
    ("536233", False),
    ("111111", False),
    ("1111ss11", False),
    ("123 456", False),
])
def test_street_number_negative(input, expected):
    ''' tests negative string match for a street number '''
    match = utils.match(
        data_ca.street_number,
        utils.unicode_str(input), re.VERBOSE)
    is_found = match is not None
    """we check that:
       - input should not to match our regex
       - our match should be partial if regex matches some part of string
    """
    assert (is_found == expected) or \
           (match.group(0) != utils.unicode_str(input))


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
    is_found = utils.match(
        data_ca.post_direction,
        utils.unicode_str(input), re.VERBOSE)\
        is not None
    assert is_found == expected


@pytest.mark.parametrize("input,expected", [
    # positive assertions
    ("Street ", True),
    ("St. ", True),
    ("St.", True),
    ("Blvd.", True),
    ("Blvd. ", True),
    ("RD", True),
    ("Cir", True),
    ("Highway ", True),
    ("Hwy ", True),
    ("Ctr", True),
    ("Sq.", True),
    ("Street route 5 ", True),
    ("blvd", True),
    # negative assertions
    # TODO
])
def test_street_type(input, expected):
    ''' tests string match for a street id '''
    is_found = utils.match(
        data_ca.street_type,
        utils.unicode_str(input), re.VERBOSE)\
        is not None
    assert is_found == expected


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
    is_found = utils.match(
        data_ca.floor,
        utils.unicode_str(input), re.VERBOSE)\
        is not None
    assert is_found == expected


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
    is_found = utils.match(
        data_ca.building,
        utils.unicode_str(input), re.VERBOSE)\
        is not None
    assert is_found == expected


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
    ("Unit B ", True),
    ("ste A ", True),
    ("Ste 101 ", True),
    ("ste 502b ", True),
    ("ste 14-15 ", True),
    ("ste E ", True),
    ("ste 9E ", True),
    ("Suite 1800 ", True),
    ("Apt 1B ", True),
    ("Rm. 52 ", True),
    ("#2b ", True),
])
def test_occupancy_positive(input, expected):
    ''' tests exact string match for a place id '''
    match = utils.match(
        data_ca.occupancy,
        utils.unicode_str(input), re.VERBOSE)
    is_found = match is not None
    assert (is_found == expected) and\
           (match.group(0) == utils.unicode_str(input))


@pytest.mark.parametrize("input,expected", [
    # positive assertions
    ("suite900 ", False),
    ("Suite#2", False),
    ("suite218 ", False),
])
def test_occupancy_negative(input, expected):
    ''' tests string match for a place id '''
    match = utils.match(
        data_ca.occupancy,
        utils.unicode_str(input), re.VERBOSE)
    is_found = match is not None
    assert (is_found == expected)


@pytest.mark.parametrize("input,expected", [
    # positive assertions
    ("po box 108", True),
    ("Po Box 53485", True),
    ("P.O. box 119", True),
    ("PO box 1070", True),
])
def test_po_box_positive(input, expected):
    ''' tests exact string match for a po box '''
    match = utils.match(
        data_ca.po_box,
        utils.unicode_str(input), re.VERBOSE)
    is_found = match is not None
    assert (is_found == expected) and\
           (match.group(0) == utils.unicode_str(input))


@pytest.mark.parametrize("input,expected", [
    # positive assertions
    ("po box108 ", False),
    ("PoBox53485 ", False),
    ("P.O. box119", False),
    ("POb ox1070 ", False),
])
def test_po_box_negative(input, expected):
    ''' tests string match for a po box '''
    match = utils.match(
        data_ca.po_box,
        utils.unicode_str(input), re.VERBOSE)
    is_found = match is not None
    assert (is_found == expected)

"""
NOTE:
Testing for 'full_street' below is meaningless
since "full_street_b" regexp is based on positive
lookahead assertion and lazy regex before it,
so it will fail most of the tests below, while
still finding correct matches in full_address
"""


@pytest.mark.parametrize("input,expected", [
    # positive assertions
    ("15979 Bow Bottom Trail SE, Calgary, AB T2J 6T5", True),
    ("1730 McPherson Crt. Unit 35, Pickering, ON",
        True),
    ("20 Fleeceline Road, Toronto, Ontario M8V 2K3", True),
    ("7034 Gilliespie Lane, Mississauga, ON L5W1E8", True),
    ("12991 Keele Street King City, Ontario L7B 1G2 CANADA", True),
    ("15979 Bow Bottom Trail SE, Calgary, AB T2J 6T5", True),
    ("718 - 8th Avenue SW Calgary, AB T2P 1H3", True),
    ("67 Lougheed Rd Unit B Barrie, Ontario L4N 8G1", True),
    ("200 - 5050 Kingsway Ave. Burnaby, BC. Canada", True),
    ("202-121 14th Street NW Calgary, AB T2N 1Z6", True),
    ("108 - 1550 Hartley Avenue Coquitlam, B.C. V3K 7A1", True),
    ("1555 Walkley Road Unit 3, Ottawa, ON, K1V 6P4 Canada", True),
    ("238 Jarvis Ave, Winnipeg MB R2W 3A2", True),
    ("104-18663 52 AVE SURREY, BC V3S 8E5", True),
    ("14952 121a Ave NW, Edmonton, AB T5V 1A3, Canada", True),
    ("8623 Granville Street Unit 143 Vancouver, BC V6P 5A2", True),
    ("40 Ferrier St. Markham, ON L3R 2Z5", True),
    ("13009 239b St. Maple Ridge, BC V4R 0A5", True),
    ("40, Rue Ruskin, Ottawa (Ontario) K1Y 4W7 Canada", True),
    ("25 Bethridge Road Toronto, Ontario, Canada", True),
    ("3000 Steeles Avenue East, Suite 700 Markham, Ontario Canada", True),
    ("30 Titan Road Unit 17 Toronto, Ontario M8Z 5Y2", True),
    ("405, rue Sainte Montreal Québec", True),
    ("405, rue Sainte-Catherine Est Montréal (Québec) H2L 2C4", True),
    ("5800, rue Saint-Denis, bureau 1105 Montréal (Québec) H2S 3L5 Canada",
        True),
    ("3744, rue Jean-Brillant Bureau 490 Montréal (Québec)", True),
    ("2275, rue Holt Montréal (Québec) H2G 3H1", True),
    ("475, boulevard De Maisonneuve Est Montréal (Québec) H2L 5C4", True),
    ("133 Ilsley Avenue, Unit A Dartmouth (Nova Scotia) B3B 1S9", True),
    ("5205 Satellite Drive Mississauga (Ontario) L4W 5J7", True),
    ("400 Main Street, Bureau 2080 Saint John (New Brunswick) E2K 4N5", True),
    ("16, Place du Commerce Île des Soeurs Verdun (Québec) H3E 2A5", True),
    ("4260, Still Creek Drive Burnaby (Colombie-Britannique) V5C 6C6", True),
    ("201, avenue Portage, Bureau 1750 Winnipeg (Manitoba)", True),
    ("555, boulevard de l'Université Chicoutimi (Québec) Canada", True),
    ("283, boulevard Alexandre-Taché Gatineau (Québec) Canada J9A 1L8", True),
    ("5, rue Saint-Joseph Saint-Jérôme (Québec) J7Z 0B7", True),
    ("58, rue Principale Ripon (Québec) J0V 1V0", True),
    ("33771 George Ferguson Way Abbotsford, BC V2S 2M5", True),
    ("33771 George Ferguson Way Suite 668 Abbotsford, BC V2S 2M5", True),
    ("11, rue Notre-Dame Ouest Montréal (Québec) H2Y 4A7", True),
    ("775, rue Saint-Viateur Québec (Québec) G2L 2Z3", True),
    ("2275, rue Holt Montréal (Québec) H2G 3H1", True),
    ("475, boulevard De Maisonneuve Est Montréal (Québec) H2L 5C4", True),
    ("1050, chemin Sainte-Foy Québec (Québec) G1S 4L8", True),
    ("1401, 18e rue Québec (Québec) G1J 1Z4", True),
    ("1050, chemin Sainte-Foy Québec (Québec) G1S 4L8", True),
    ("101, rue Saint-Jean-Bosco Gatineau (Québec) Canada J8Y 3G5", True),
    ("205, avenue de la Cathédrale Case postale 710 Rimouski (Québec) G5L 7C7",
        True),
    ("3351, boul. des Forges C.P. 500, Trois-Rivières (Québec)"
        " Canada, G9A 5H7", True),
    ("3264 Mainway Burlington L7M 1A7 Ontario, Canada", True),
    ("20 Fleeceline Road, Floor 3, Toronto, Ontario M8V 2K3", True),
    ("20 Fleeceline Road, 3rd Floor, Toronto, Ontario M8V 2K3", True),
])
def test_full_address_positive(input, expected):
    ''' tests exact string match for a full address '''
    match = utils.match(
        data_ca.full_address,
        utils.unicode_str(input), re.VERBOSE | re.U)
    is_found = match is not None
    assert (is_found == expected) and\
           (match.group(0) == utils.unicode_str(input))


@pytest.mark.parametrize("input,expected", [
    # positive assertions
    ("T2P 1H3", True),
    ("T2P1H3", True),
    ("L1W3E6", True),
    ("L4N 8G1", True),
    ("J8Y 3G5", True),
    ("J9A 1L8", True),
])
def test_postal_code_positive(input, expected):
    ''' test exact string match for postal code '''
    match = utils.match(
        data_ca.postal_code,
        utils.unicode_str(input), re.VERBOSE)
    is_found = match is not None
    assert is_found == expected and\
        match.group(0) == utils.unicode_str(input)


@pytest.mark.parametrize("input,expected", [
    # positive assertions
    ("1", False),
    ("23", False),
    ("456", False),
    ("4567", False),
    ("750621", False),
    ("95130-642", False),
    ("95130-64212", False),
])
def test_postal_code_negative(input, expected):
    ''' test exact string match for postal code '''
    match = utils.match(
        data_ca.postal_code,
        utils.unicode_str(input), re.VERBOSE)
    is_found = match is not None
    assert (is_found == expected) or\
           (match.group(0) != utils.unicode_str(input))


@pytest.mark.parametrize("input,expected", [
    # positive assertions
    ("Quebec", True),
    ("Nova Scotia", True),
    ("Colombie-Britannique", True),
    ("New Brunswick", True),
    ("Quebec", True),
    ("Québec", True),
    ("Territoires Du Nord-Ouest", True),
])
def test_region1(input, expected):
    ''' test exact string match for province '''
    match = utils.match(data_ca.region1, input, re.VERBOSE)
    is_found = match is not None
    assert is_found == expected and \
        match.group(0) == utils.unicode_str(input)


@pytest.mark.parametrize("input,expected", [
    # positive assertions
    ("CANADA", True),
    ("Canada", True),
])
def test_country(input, expected):
    ''' test exact string match for country '''
    match = utils.match(data_ca.country, input, re.VERBOSE)
    is_found = match is not None
    assert is_found == expected and match.group(0) == input
