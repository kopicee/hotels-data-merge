from typing import Dict, List, Tuple

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

    def find(self,
             hotel_ids: List[str],
             destination_ids: List[str],
             limit: int,
             offset: int,
             ) -> Tuple[List[Hotel], int]:
        """
        Equivalent to SELECT * ... WHERE id IN (?, ...) AND destination_ids IN (?, ...)
        """
        matching_rows: List[Hotel] = []
        for id, hotel in self.table.items():
            is_match_id = True if not bool(hotel_ids) \
                          else id in hotel_ids
            is_match_destinations = True if not bool(destination_ids) \
                                         else hotel.destination_id in destination_ids
            if is_match_id and is_match_destinations:
                matching_rows.append(hotel)

        total_count = len(matching_rows)
        result = []
        for i, h in enumerate(matching_rows):
            if i < offset:
                continue
            if len(result) == limit:
                break
            result.append(h)

        return result, total_count
