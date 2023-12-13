# pyright: reportPrivateUsage=false
# -*- coding: utf-8 -*-

""" Test for parser classes """

import pytest

import pyap as ap
from pyap import parser
from pyap import address
from pyap import exceptions as e


def test_api_parse():
    test_address = (
        "xxx 225 E. John Carpenter Freeway, " + "Suite 1500 Irving, Texas 75062 xxx"
    )
    addresses = ap.parse(test_address, country="US")
    assert (
        str(addresses[0].full_address)
        == "225 E. John Carpenter Freeway, Suite 1500 Irving, Texas 75062"
    )


def test_api_parse_canada():
    test_address = "xxx 33771 George Ferguson Way Abbotsford, BC V2S 2M5 xxx"
    addresses = ap.parse(test_address, country="CA")
    assert (
        str(addresses[0].full_address)
        == "33771 George Ferguson Way Abbotsford, BC V2S 2M5"
    )


def test_api_parse_single_street():
    test_address = "255 SOUTH STREET"
    addresses = ap.parse_single_street(test_address, country="US")
    assert str(addresses[0].full_street) == "255 SOUTH STREET"
    assert str(addresses[0].full_address) == "255 SOUTH STREET"


def test_address_class_init():
    addr = address.Address(
        country_id="US",
        match_end=10,
        match_start=5,
        region1="USA ",
        city="CityVille, ",
        full_street="Street 1b",
        full_address="Street 1b CityVille USA",
    )
    assert addr.region1 == "USA"

    assert addr.city == "CityVille"

    assert addr.full_street == "Street 1b"

    assert str(addr) == "Street 1b CityVille USA"


def test_no_country_selected_exception():
    with pytest.raises(TypeError):
        parser.AddressParser()  # type: ignore


def test_country_detection_missing():
    with pytest.raises(e.CountryDetectionMissing):
        parser.AddressParser(country="TheMoon")  # type: ignore


def test_normalize_string():
    ap = parser.AddressParser(country="US")
    raw_string = (
        """, The  quick      \t, brown fox      jumps over the lazy dog, ‐ ‑ ‒ – — ―,"""
    )
    clean_string = ", The quick, brown fox jumps over the lazy dog, - - - - - -, "
    assert ap._normalize_string(raw_string) == clean_string


def test_combine_results():
    ap = parser.AddressParser(country="US")
    raw_dict = {"test_one": None, "test_one_a": 1, "test_two": None, "test_two_b": 2}
    assert ap._combine_results(raw_dict) == {"test_one": 1, "test_two": 2}


@pytest.mark.parametrize(
    "input,expected",
    [
        ("No address here", None),
        (
            "2590 Elm Road NE - Warren, OH 44483",
            {
                "street_number": "2590",
                "street_name": "Elm",
                "street_type": "Road",
                "post_direction": "NE",
                "city": "Warren",
                "region1": "OH",
                "postal_code": "44483",
                "full_address": "2590 Elm Road NE - Warren, OH 44483",
            },
        ),
        (
            "899 HEATHROW PARK LN 02-2135\nLAKE MARY,FL 32746",
            {
                "street_number": "899",
                "street_name": "HEATHROW PARK",
                "street_type": "LN",
                "city": "LAKE MARY",
                "region1": "FL",
                "postal_code": "32746",
                "full_address": "899 HEATHROW PARK LN 02-2135\nLAKE MARY, FL 32746",
            },
        ),
        (
            "696 BEAL PKWY NW\nFT WALTON BCH FL 32547",
            {
                "street_number": "696",
                "street_name": "BEAL",
                "street_type": "PKWY",
                "post_direction": "NW",
                "city": "FT WALTON BCH",
                "region1": "FL",
                "postal_code": "32547",
                "full_address": "696 BEAL PKWY NW\nFT WALTON BCH FL 32547",
            },
        ),
        (
            "xxx, 225 E. John Carpenter Freeway, Suite 1500 Irving, Texas 75062 xxx",
            {
                "street_number": "225",
                "street_name": "E. John Carpenter",
                "street_type": "Freeway",
                "occupancy": "Suite 1500",
                "city": "Irving",
                "region1": "Texas",
                "postal_code": "75062",
                "full_address": (
                    "225 E. John Carpenter Freeway, Suite 1500 Irving, Texas 75062"
                ),
            },
        ),
        (
            "1300 E MOUNT GARFIELD ROAD, NORTON SHORES 49441",
            {
                "street_number": "1300",
                "street_name": "E MOUNT GARFIELD",
                "street_type": "ROAD",
                "city": "NORTON SHORES",
                "region1": None,
                "postal_code": "49441",
                "full_address": "1300 E MOUNT GARFIELD ROAD, NORTON SHORES 49441",
            },
        ),
        (
            "7601 Penn Avenue South, Richfield MN 55423",
            {
                "street_number": "7601",
                "street_name": "Penn",
                "street_type": "Avenue",
                "post_direction": "South",
                "city": "Richfield",
                "region1": "MN",
                "postal_code": "55423",
            },
        ),
        (
            "STAFFING LLC, 242 N AVENUE 25 SUITE 300, LOS ANGELES, CA 900031, Period ",
            {
                "street_number": "242",
                "single_street_name": "N AVENUE 25",
                "occupancy": "SUITE 300",
                "city": "LOS ANGELES",
                "region1": "CA",
                "postal_code": None,
            },
        ),
        (
            "2633 Camino Ramon Ste. 400 San Ramon, CA 94583-2176",
            {
                "street_number": "2633",
                "street_type": "Camino",
                "street_name": "Ramon",
                "occupancy": "Ste. 400",
                "city": "San Ramon",
                "region1": "CA",
                "postal_code": "94583-2176",
            },
        ),
    ],
)
def test_parse_address(input: str, expected):
    ap = parser.AddressParser(country="US")
    if result := ap.parse(input):
        expected = expected or {}
        received = {key: getattr(result[0], key) for key in expected}
        assert received == expected
    else:
        assert expected is None


def test_parse_po_box():
    ap = parser.AddressParser(country="US")

    address = ap.parse_single_street(
        "ELECTRIC WIRING SYSTEMS INC, 1111 ASHLEY STREET, P.O. BOX 99999, "
        "BOWLING GREEN, KY 444444-9999"
    )[0]
    assert address.po_box == "P.O. BOX 99999"

    address = ap.parse_single_street("P.O. BOX 99999, One Velvet Drive")[0]
    assert address.po_box == "P.O. BOX 99999"

    address = ap.parse_single_street("P.O. BOX 99999")[0]
    assert address.po_box == "P.O. BOX 99999"
