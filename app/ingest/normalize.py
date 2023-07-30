import re
from typing import List

from babel import Locale


class Const:
    EMPTY_LATITUDE = -999.999
    EMPTY_LONGITUDE = -999.999


class String:
    @staticmethod
    def split_camel_case(s: str) -> List[str]:
        matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', s)
        return [m.group(0) for m in matches]


class Address:
    @staticmethod
    def country_from_iso(iso_code: str, lang: str = 'en', territory: str = 'US'):
        loc = Locale(lang, territory)
        return loc.territories[iso_code.upper()]

    @staticmethod
    def normalize_address_line(s: str):
        lines = s.split(',')
        return ', '.join(line.strip() for line in lines)


class Amenities:
    @classmethod
    def to_normalized_tags(cls, items: List[str]) -> List[str]:
        tags = [
            cls.normalize_tag(item)
            for item in items
        ]
        return list(set(tags))
            

    @staticmethod
    def normalize_tag(item: str) -> str:
        item = item.strip()
        if item.lower() == 'wifi':
            return 'wifi'
        words = String.split_camel_case(item)
        return ' '.join(words).lower()
