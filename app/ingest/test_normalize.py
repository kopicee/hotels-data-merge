from app.ingest.normalize import *


def test_split_camel_case():
    testcases = {
        'CamelCase': ['Camel', 'Case'],
        'camelCase': ['camel', 'Case'],
        'camelCase123': ['camel', 'Case123'],
    }
    for input, expect in testcases.items():
        assert Strings.split_camel_case(input) == expect


def test_country_from_iso():
    testcases = {
        ('SG', 'en', 'US'): 'Singapore',
        ('JP', 'en', 'US'): 'Japan',
    }
    for input, expect in testcases.items():
        assert Addresses.country_from_iso(*input) == expect


def test_to_normalized_tags():
    testcases = {
        ('tv', 'iron'): ['iron', 'tv'],  # sorting
        ('Aircon', 'Tub'): ['aircon', 'tub'],  # lowercasing
        ('HairDryer', 'DryCleaning'): ['dry cleaning', 'hair dryer'],  # camel case
        ('WiFi',): ['wifi'],  # wifi edge case
        ('aircon', 'aircon'): ['aircon']  # de-duplication
    }
    for input, expect in testcases.items():
        assert Amenities.to_normalized_tags(input) == expect


def test_lat_long_precision():
    assert lat_long_precision(1.23) == 2
    assert lat_long_precision(1) == -1
    assert lat_long_precision(Consts.EMPTY_LATITUDE) == -1
    assert lat_long_precision(Consts.EMPTY_LONGITUDE) == -1


def test_argmax():
    assert argmax(1, 5) == 5
    assert argmax('a', 'abcde', len) == 'abcde'
    assert argmax('a', 'b', len) == 'a'
    assert argmax(1.2, 1.234, lat_long_precision) == 1.234
