from typing import Annotated, List

from fastapi import APIRouter, Query
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from app.model import Hotel
from app.database import Database


class GetHotelsResponse(BaseModel):
    result: List[Hotel]
    total_count: int


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
                       destinations: Annotated[List[str], Query(description='List of destination IDs')] = None,
                       page: Annotated[int, Query(description='Page number')] = 1,
                       per_page: Annotated[int, Query(description='Records per page')] = 20,
                       ) -> GetHotelsResponse:
            hotels, count = self.db.find(hotels,
                                         destinations,
                                         limit=per_page,
                                         offset=(page - 1) * per_page)

            return GetHotelsResponse(
                result=hotels,
                total_count=count,
            )

        return router
