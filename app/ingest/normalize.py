from datetime import datetime
import re
from typing import List

from babel import Locale
from rich.console import Console
from rich.table import Table

from app import model


console = Console()


class Consts:
    EMPTY_LATLONG = -999.999


class Strings:
    @staticmethod
    def split_camel_case(s: str) -> List[str]:
        matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', s)
        return [m.group(0) for m in matches]


class Addresses:
    @staticmethod
    def country_from_iso(iso_code: str, lang: str = 'en', territory: str = 'US'):
        loc = Locale(lang, territory)
        return loc.territories[iso_code.upper()]

    @staticmethod
    def normalize_address_line(s: str):
        lines = s.split(',')
        return ', '.join(line.strip() for line in lines)

    @staticmethod
    def is_valid_latlong(x: float) -> bool:
        if x == Consts.EMPTY_LATLONG:
            return False
        if type(x) != float:
            return False
        return abs(x) <= 180


class Amenities:
    @classmethod
    def to_normalized_tags(cls, *items: List[str]) -> List[str]:
        tags = [
            cls.normalize_tag(item)
            for item in items
        ]
        return sorted(list(set(tags)))  # sorting is just for unit tests
            

    @staticmethod
    def normalize_tag(item: str) -> str:
        item = item.strip()
        if item.lower() == 'wifi':
            return 'wifi'
        words = Strings.split_camel_case(item)
        return ' '.join(words).lower()


def lat_long_precision(x: float):
    if not Addresses.is_valid_latlong(x):
        return -1

    decimals = str(x).split('.')[1]
    return len(decimals)


def argmax(x, y, criteria=None, cmp=lambda x, y: x >= y):
    fx, fy = x, y
    if criteria:
        fx, fy = criteria(x), criteria(y)
    if fx == fy:
        return x

    if cmp(fx, fy):
        # console.log(f'  Keep:    {x}')
        # console.log(f'  Discard: {y}')
        return x

    else:
        # console.log(f'  Keep:    {y}')
        # console.log(f'  Discard: {x}')
        return y


class Hotels:
    @staticmethod
    def merge(curr: model.Hotel, next: model.Hotel) -> model.Hotel:
        # TODO: Save memory by updating in-place instead of re-allocating
        return model.Hotel(
            # Assume these don't change
            id=curr.id,
            destination_id=curr.destination_id,

            # For name and description, more verbose is better
            name=argmax(curr.name, next.name, len),
            description=argmax(curr.description, next.description, len),
        
            # For location, prefer more precision/verbosity
            location=model.Location(
                lat=argmax(curr.location.lat, next.location.lat, lat_long_precision),
                lng=argmax(curr.location.lng, next.location.lng, lat_long_precision),
                address=argmax(curr.location.address, next.location.address, len),
                city=argmax(curr.location.city, next.location.city, len),
                country=argmax(curr.location.country, next.location.country, len),
            ),

            # For amenities and images, merge everything
            amenities=model.Amenities(
                general=curr.amenities.general + next.amenities.general,
                room=curr.amenities.room + next.amenities.room,
            ),
            images=model.Images(
                rooms=curr.images.rooms + next.images.rooms,
                site=curr.images.site + next.images.site,
                amenities=curr.images.amenities + next.images.amenities,
            ),

            # For booking conditions, more verbose is better
            booking_conditions=argmax(curr.booking_conditions, next.booking_conditions, len),

            # For timestamps, take the first we see.
            # Ideally the initial object is a pre-existing record from our db which
            # should already have these fields populated.
            created_at=curr.created_at or next.created_at,
            updated_at=curr.updated_at or next.updated_at,
        )

    @staticmethod
    def normalize(h: model.Hotel, now: datetime):
        h.name = h.name.strip()
        h.description = h.description.strip()
        h.location.address = Addresses.normalize_address_line(h.location.address)
        h.location.city = h.location.city.strip()
        h.location.country = h.location.country.strip()
        h.amenities.general = Amenities.to_normalized_tags(*h.amenities.general)
        h.amenities.room = Amenities.to_normalized_tags(*h.amenities.room)

        if not (Addresses.is_valid_latlong(h.location.lat) and Addresses.is_valid_latlong(h.location.lng)):
            h.location.lat = None
            h.location.lng = None

        if not h.created_at:
            h.created_at = now
        h.updated_at = now
