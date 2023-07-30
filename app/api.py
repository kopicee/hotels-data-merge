from typing import Annotated, List

from fastapi import APIRouter, Query
from fastapi.responses import RedirectResponse

from app.model import Hotel
from app.database import Database


class Controller:
    def __init__(self, db):
        self.db: Database = db

    def router(self) -> APIRouter:
        router = APIRouter()

        @router.get('/', response_class=RedirectResponse, include_in_schema=False)
        def redirect_to_docs():
            return '/docs'

        @router.get('/api/v1/hotels', tags=['Hotels'])
        def get_hotels(hotels: Annotated[List[str], Query(description='List of hotel IDs')] = None,
                       destinations: Annotated[List[str], Query(description='List of destination IDs')] = None
                       ) -> List[Hotel]:
            return self.db.find(hotels, destinations)

        return router
