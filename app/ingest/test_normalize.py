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
        ('WiFi',): ['wifi'],  # wifi edge case & de-duplication
    }
    for input, expect in testcases.items():
        assert Amenities.to_normalized_tags(input) == expect

