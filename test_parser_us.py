# -*- coding: utf-8 -*-

""" Test for USA address parser """

import re
import pytest
from pyap import utils
from pyap.packages import six
import pyap.source_US.data as data_us


def execute_matching_test(input, expected, pattern):
    match = utils.match(pattern, input, re.VERBOSE)
    is_found = match is not None
    if expected:
        assert is_found == expected and match.group(0) == input
    else:
        """we check that:
           - input should not to match our regex
           - our match should be partial if regex matches some part of string
        """
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
    execute_matching_test(input, expected, data_us.zero_to_nine)


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
    execute_matching_test(input, expected, data_us.ten_to_ninety)


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
    execute_matching_test(input, expected, data_us.hundred)


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
    execute_matching_test(input, expected, data_us.thousand)


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
    ''' tests string match for a street number '''
    execute_matching_test(input, expected, data_us.street_number)


@pytest.mark.parametrize("input,expected", [
    # positive assertions
    ("Northeast Kentucky Industrial ", True),
    ("One ", True),
    ("First ", True),
    ("Ave 123 ", True),
    ("Northeast 5 ", True),
    # negative assertions
    ("Northeast Kentucky Industrial Maple ", False),
    ("a", False),
    ("ab", False),
])
def test_street_name(input, expected):
    ''' tests positive string match for a street name '''
    execute_matching_test(input, expected, data_us.street_name)


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
    execute_matching_test(input, expected, data_us.post_direction)


@pytest.mark.parametrize("input,expected", [
    # positive assertions
    ("Street ", True),
    ("St. ", True),
    ("St.", True),
    ("Blvd.", True),
    ("Blvd. ", True),
    ("LN ", True),
    ("RD", True),
    ("Cir", True),
    ("Highway ", True),
    ("Hwy ", True),
    ("Ct", True),
    ("Sq.", True),
    ("LP. ", True),
    ("LP. (Route A1 )", True),
    ("Street route 5 ", True),
    ("blvd", True),
    ("Estate", True),
    ("Manor", True),
    # negative assertions
    # TODO

])
def test_street_type(input, expected):
    ''' tests string match for a street id '''
    execute_matching_test(input, expected, data_us.street_type)


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
    execute_matching_test(input, expected, data_us.floor)


@pytest.mark.parametrize("input,expected", [
    # positive assertions
    ("bldg m ", True),
    ("Building F ", True),
    ("bldg 2 ", True),
    ("building 3 ", True),
    ("building 100 ", True),
    ("building 1000 ", True),
    ("Building ", True),
    ("building one ", True),
    ("Building three ", True),
    # negative assertions
    ("bldg", False),
    ("bldgm", False),
    ("bldg100 ", False),
    ("building 10000 ", False),

])
def test_building(input, expected):
    ''' tests string match for a building '''
    execute_matching_test(input, expected, data_us.building)


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
    ("#2b ", True),
    # positive assertions
    ("suite900 ", False),
    ("Suite#2", False),
    ("suite218 ", False),
])
def test_occupancy(input, expected):
    ''' tests string match for a place id '''
    execute_matching_test(input, expected, data_us.occupancy)


@pytest.mark.parametrize("input,expected", [
    # positive assertions
    ("po box 108", True),
    ("Po Box 53485", True),
    ("P.O. box 119", True),
    ("PO box 1070", True),
    # negative assertions
    ("po box108 ", False),
    ("PoBox53485 ", False),
    ("P.O. box119", False),
    ("POb ox1070 ", False),
])
def test_po_box_positive(input, expected):
    ''' tests exact string match for a po box '''
    execute_matching_test(input, expected, data_us.po_box)


@pytest.mark.parametrize("input,expected", [
    # positive assertions
    ("9652 Loiret Boulevard", True),
    ("101 MacIntosh Boulevard", True),
    ("1 West Hegeler Lane", True),
    ("1270 Leeds Avenue", True),
    ("85-1190 Ranchview Rd. NW ", True),
    ("62 Portland Road (Route 1)", True),
    ("200 N. Pine Avenue Suite 514", True),
    ("200 S. Alloy Drive", True),
    ("Two Hundred S. Alloy Drive", True),
    ("Two Hundred South Alloy Drive", True),
    ("Two Hundred South Alloy Dr.", True),
    ("11001 Fondren Rd,", True),
    ("9606 North Mopac Expressway Suite 500", True),
    ("9692 East Arapahoe Road,", True),
    ("9 Grand Avenue, Suite 2", True),
    ("9 Grand Avenue Building 2, Suite 2", True),
    ("9 Grand Avenue Building 2, Suite 2A", True),
    ("233 Richmond Highway Suite 1800", True),
    ("354 Eisenhower Parkway P.O. Box 472", True),
    ("6645 N Ensign St", True),
    ("1200 Old Fairhaven Pkwy Apt 106", True),
    ("1659 Scott Blvd Ste 26", True),
    ("377 Fisher Rd Ste C", True),
    ("1833 Stearman Ave", True),
    ("1737 S Lumpkin St Ste B", True),
    ("101 N Court Sq Ste 16", True),
    ("1790 Yardley Langhorne Rd, Suite #205", True),
    ("280 West Main Street", True),
    ("701 Tennessee Walk", True),
    ("7457 Harwin Dr", True),
    ("700 Davis Avenue", True),
    ("1 W 47th St", True),
    ("832 Seward St", True),
    ("2740 Timber Ridge Lane", True),
    ("810 E Western Ave", True),
    ("6223 Richmond Ave Ste 105", True),
    ("400 Middle Street", True),
    ("81 N Main St", True),
    ("3705 West Memorial Road", True),
    ("4911 Matterhorn Dr", True),
    ("5830 Yahl Street, #2b", True),
    ("9400 Doliver Dr Apt 13", True),
    ("10701 Stirling Road", True),
    ("1865 Corporate Dr Ste 225", True),
    ("80 Beaman Rd", True),
    ("9691 Spratley Ave", True),
    ("10835 New Haven Rd NW ", True),
    ("320 W Broussard Rd", True),
    ("9001 Any Old Way", True),
    ("8967 Market St.", True),
    ("3724 Oxford Blvd.", True),
    ("901 Rainier Ave S ", True),
])
def test_full_street_positive(input, expected):
    ''' tests exact string match for a full street '''
    execute_matching_test(input, expected, data_us.full_street)


@pytest.mark.parametrize("input,expected", [
    # positive assertions
    ("0 OLD MILL RD, Maynard, MA 01754", True),
    ("103 Morgan Lane, Suite 102 Plainsboro, NJ 08536", True),
    ("3409 16th St Metairie, LA 70002", True),
    ("1505 NW 14th Street Miami, FL 33125", True),
    ("01 Main Rd. Newfield, NJ", True),
    ("28 Gorgo Lane Newfield, NJ", True),
    ("1720 HARDING HWY NEWFIELD, NJ", True),
    ("4409 N DELSEA DR NEWFIELD, NJ", True),
    ("742 FORSYTHIA DR NEWFIELD, NJ", True),
    ("9 N EAST BLVD NEWFIELD, NJ 10000", True),
    ("1640 Harding Hwy Newfield, NJ", True),
    ("1720 Harding Highway NEWFIELD, NJ", True),
    ("1014 CATAWBA AVE NEWFIELD, NJ", True),
    ("11 ARCH AVE NEWFIELD, NJ", True),
    ("133 TAYLOR RD NEWFIELD, NJ", True),
    ("4409 N Delsea Drive Newfield, NJ", True),
    ("8 TAYLOR RD NEWFIELD, NJ", True),
    ("28 GORGO LN NEWFIELD, NJ", True),
    ("900 COLUMBIA AVE. NEWFIELD, NJ", True),
    ("3201 MAIN RD NEWFIELD, NJ", True),
    ("4421 N DELSEA DR NEWFIELD, NJ", True),
    ("742 Forsythia Drive Newfield, NJ", True),
    ("1450 E. Chestnut Avenue, Vineland NJ,", True),
    ("50 Harry S Truman Parkway Annapolis, MD 21401", True),
    ("420 Crompton Street Charlotte , North Carolina 28273", True),
    ("204 East 3rd Ave Cheyenne, WY 82001", True),
    ("1806 Dominion Way Ste B Colorado Spgs, CO 80918-8409", True),
    ("2600 South Shore Blvd Ste. 300 League City, TX 77573", True),
    ("2675 Antler Drive Carson City, NV 89701-1451", True),
    ("3719 Lockwood Dr., Houston, TX 77026", True),
    ("154 Grand Street New York, NY 10013", True),
    ("3655 Torrance Blvd Suite 230 Torrance CA 90503", True),
    ("800 Sixth Ave #31A New York, NY 10001", True),
    ("8861 Research Drive, Ste. 200, Irvine, CA 92618", True),
    ("317 N. Mission St. Ste. 200 Wenatchee, WA 98801", True),
    ("2709 Bickford Avenue, Suite A Snohomish, WA 98290", True),
    ("7307 N. Division Street, Suite 102 Spokane, WA 99208", True),
    ("1530 South Union Avenue, Suite 7 Tacoma, WA 98405", True),
    ("3131 Smokey Point Drive, Suite 14 A Arlington, WA 98223", True),
    ("1603 Grove Street Marysville, WA 98270", True),
    ("15701 E. Sprague Avenue, Suite F Spokane Valley, WA 99037", True),
    ("18204 Bothell Everett Hwy, Suite E Bothell, WA 98012", True),
    ("3505 188th Street SW Lynnwood, WA 98037", True),
    ("3218 NE 12th Street, Suite B Renton, WA 98056", True),
    ("22035 SE Wax Road, Suite 5 Maple Valley, WA 98038", True),
    ("8861 Research Drive, Ste. 200 Irvine, CA 92618", True),
    ("4031 University Drive Suite 200 Fairfax, Virginia 22030", True),
    ("586 W. 207 St. New York, NY 10034", True),
    ("85 Newbury St, Boston, MA 02116", True),
    ("1827 Union St, San Francisco, CA 94123", True),
    ("1636 Main St Sarasota, FL 34236", True),
    ("1015 South Western Avenue, Chicago, IL 60649", True),
    ("510 W 7th St. Los Angeles, CA 90014", True),
    ("225 North Larchmont Blvd Los Angeles, CA 90004", True),
    ("3760 E. Tremont Ave. Throgsneck, NY 10465", True),
    ("8126 S. Stony Island Ave Chicago, IL 60617", True),
    ("68116 HEM 908 B WEST 12th St. Austin, TX 78703", True),
    ("546 West Colorado Street Glendale CA 91204", True),
    ("2210 N Halsted St, Chicago, IL 60614", True),
    ("4090 Westown Pkwy Ste B2 Chicago, IL 60614", True),
    ("7000 Peachtree Dunwoody Rd NE Bldg 7, Miami, FL, USA", True),
    ("98-025 Hekaha St Ste 221A, Cityville, Arizona", True),
    ("225 E. John Carpenter Freeway, Suite 1500 Irving, Texas 75062 U.S.A.", True),
    ("643 Lincoln Rd. Miami Beach, FL 33139", True),
    ("300 Market St. Harrisburg, PA 17101", True),
    ("2 Kings Hwy Shreveport, LA 71104", True),
    ("1500 Westlake Avenue North Suite 108 Seattle, WA 98109", True),
    ("840 Garrison Brooks Suite 985, New Sarah, OH 38255", True),
    ("840 Garrison Brooks Suite 985 New Sarah, OH 38255", True),
    ("5545 Langston Blvd, Floor 2, Arlington, VA 22207", True),
    ("5545 Langston Blvd., 2nd Floor, Arlington, VA 22207", True),
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
    execute_matching_test(input, expected, data_us.full_address)


@pytest.mark.parametrize("input,expected", [
    # positive assertions
    ("75062", True),
    ("15032", True),
    ("95130-6482", True),
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
    execute_matching_test(input, expected, data_us.postal_code)


@pytest.mark.parametrize("input,expected", [
    # positive assertions
    ("Montana", True),
    ("Nebraska", True),
    ("NJ", True),
    ("DC", True),
    ("PuErTO RIco", True),
    ("oregon", True),
])
def test_region1(input, expected):
    ''' test exact string match for province '''
    execute_matching_test(input, expected, data_us.region1)


@pytest.mark.parametrize("input,expected", [
    # positive assertions
    ("USA", True),
    ("U.S.A", True),
    ("United States", True),
])
def test_country(input, expected):
    ''' test exact string match for country '''
    execute_matching_test(input, expected, data_us.country)
