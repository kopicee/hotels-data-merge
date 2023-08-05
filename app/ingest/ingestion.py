from collections import defaultdict
from datetime import datetime
from functools import partial, reduce
import threading
from typing import List

from rich.console import Console

from app.database import Database
from app.ingest.normalize import Hotels
from app.ingest.suppliers import get_extractors
from app import model


console = Console()


class ResultThread(threading.Thread):
    def __init__(self, **kwargs):
        self.result = None

        target = kwargs['target']
        def wrapped(*a, **k):
            self.result = target(*a, **k)
        kwargs['target'] = wrapped

        super().__init__(**kwargs)


def extract_and_save(db: Database):
    threads = [
        ResultThread(target=extract)
        for extract in get_extractors()
    ]

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    hotels_by_id = defaultdict(list)
    for t in threads:
        for hotel in t.result:
            hotels_by_id[hotel.id].append(hotel)

    for hotel_id, records in hotels_by_id.items():
        console.line()
        console.log(f'===== Merging hotel id: {hotel_id} from {len(records)} records')
        merged = merge(records)
        db.save(merged)


def merge(hotels: List[model.Hotel]) -> model.Hotel:
    now = datetime.now()
    h = reduce(
        Hotels.merge,
        hotels[1:],
        hotels[0],  # ideally, initial value is a pre-existing record in our db
    )
    Hotels.normalize(h, now)
    return h
