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
    raw_string = """\n The  quick      \t, brown fox      jumps over the lazy dog,
    ‐ ‑ ‒ – — ―
    """
    clean_string = ", The quick, brown fox jumps over the lazy dog, - - - - - -, "
    assert ap._normalize_string(raw_string) == clean_string


def test_combine_results():
    ap = parser.AddressParser(country="US")
    raw_dict = {"test_one": None, "test_one_a": 1, "test_two": None, "test_two_b": 2}
    assert ap._combine_results(raw_dict) == {"test_one": 1, "test_two": 2}


def test_parse_address():
    ap = parser.AddressParser(country="US")
    result = ap.parse("No address here")
    assert not result

    ap = parser.AddressParser(country="US")
    test_address = (
        "xxx 225 E. John Carpenter Freeway, " + "Suite 1500 Irving, Texas 75062 xxx"
    )

    addresses = ap.parse(test_address)
    assert (
        addresses[0].full_address
        == "225 E. John Carpenter Freeway, Suite 1500 Irving, Texas 75062"
    )
