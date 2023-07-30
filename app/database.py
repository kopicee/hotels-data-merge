from typing import Dict, List

from app.model import Hotel


class Database:
    def __init__(self):
        # Equivalent to
        #   CREATE TABLE hotels(id, ...) PRIMARY KEY id
        # The keys of the dict correspond to PRIMARY KEY.
        self.table: Dict[str, Hotel] = dict()


    @classmethod
    def connect(cls, dsn):
        return Database()


    def save(self, h: Hotel):
        """
        Upsert into database
        
        Equivalent to INSERT ... ON DUPLICATE KEY UPDATE
        """
        self.table[h.id] = h


    def find(self, hotel_ids: List[str], destination_ids=List[str]) -> List[Hotel]:
        hotel_ids = hotel_ids or list(self.table.keys())
        destination_ids = destination_ids or [h.destination_id for h in self.table.values()]

        rows: List[Hotel] = []
        for h in self.table.values():
            if (h.id in hotel_ids) and (h.destination_id in destination_ids):
                rows.append(h)

        return rows
