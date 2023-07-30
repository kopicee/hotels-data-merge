from collections import defaultdict
from functools import reduce
from typing import List

from rich.console import Console

from app.database import Database
from app.ingest.normalize import Hotels
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
        Hotels.merge,
        hotels[1:],
        hotels[0],
    )
    Hotels.normalize(h)
    return h
