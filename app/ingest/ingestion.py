from collections import defaultdict
from functools import reduce
from typing import List

from rich.console import Console

from app.database import Database
from app.ingest.normalize import Address, Amenities, Const
from app.ingest.suppliers import get_extractors
from app import model


console = Console()


def extract_and_save(db: Database):
    hotels_by_id = defaultdict(list)

    for extract in get_extractors():  # TODO: parallel extracts
        for hotel in extract():
            hotels_by_id[hotel.id].append(hotel)

    for hotel_id, records in hotels_by_id.items():
        console.log(f'Merging hotel id: {hotel_id} from {len(records)} records')
        merged = merge(records)
        db.save(merged)


def merge(hotels: List[model.Hotel]) -> model.Hotel:
    h = reduce(
        merge_hotels,
        hotels[1:],
        hotels[0],
    )
    normalize_hotel(h)
    return h


def normalize_hotel(h: model.Hotel):
    h.name = h.name.strip()
    h.description = h.description.strip()
    h.location.address = Address.normalize_address_line(h.location.address)
    h.location.city = h.location.city.strip()
    h.location.country = h.location.country.strip()
    h.amenities.general = Amenities.to_normalized_tags(h.amenities.general)
    h.amenities.room = Amenities.to_normalized_tags(h.amenities.room)


def merge_hotels(curr: model.Hotel, next: model.Hotel) -> model.Hotel:
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
            country=argmax(curr.location.city, next.location.city, len),
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
        booking_conditions=argmax(curr.booking_conditions, next.booking_conditions, len)
    )


def lat_long_precision(x: float):
    if x == Const.EMPTY_LATITUDE or x == Const.EMPTY_LONGITUDE:
        return -1

    # Choose the option with higher precision
    if type(x) != float:
        return -1

    decimals = str(x).split('.')[1]
    return len(decimals)


def argmax(x, y, criteria=None):
    fx, fy = x, y
    if criteria:
        fx, fy = criteria(x), criteria(y)
    return x if fx > fy else y
