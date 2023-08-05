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


    def _select(self, filter) -> List[Hotel]:
        # Default sort order goes by name, ascending
        rows = [
            row for row in self.table.values()
            if filter(row)
        ]
        return sorted(self.table.values(),
                      key=lambda h: h.name)


    def find(self,
             hotel_ids: List[str],
             destination_ids: List[str],
             limit: int,
             offset: int,
             ) -> Tuple[List[Hotel], int]:
        """
        Equivalent to SELECT * ... WHERE id IN (?, ...) AND destination_ids IN (?, ...)
        """
        hotel_ids = hotel_ids or list(self.table.keys())
        destination_ids = destination_ids or [h.destination_id for h in self.table.values()]

        filter = lambda h: (h.id in hotel_ids) and (h.destination_id in destination_ids)
        matching_rows = self._select(filter)
        total_count = len(matching_rows)

        result: List[Hotel] = []
        for i, h in enumerate(matching_rows):
            if i < offset:
                continue
            if len(result) == limit:
                break
            result.append(h)

        return result, total_count
