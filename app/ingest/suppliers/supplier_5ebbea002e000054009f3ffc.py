from dataclasses import dataclass
from typing import Iterator, List, Optional

from dacite import from_dict
import requests

from app import model
from app.ingest.normalize import String, Address, Const


"""
Sample:
  {
    "Id": "iJhz",
    "DestinationId": 5432,
    "Name": "Beach Villas Singapore",
    "Latitude": 1.264751,
    "Longitude": 103.824006,
    "Address": " 8 Sentosa Gateway, Beach Villas ",
    "City": "Singapore",
    "Country": "SG",
    "PostalCode": "098269",
    "Description": "  This 5 star hotel is located on the coastline of Singapore.",
    "Facilities": [
      "Pool",
      "BusinessCenter",
      "WiFi ",
      "DryCleaning",
      " Breakfast"
    ]
  },
"""

@dataclass
class DTO:
    Id: str
    DestinationId: int
    Name: Optional[str]
    Latitude: Optional[float|str]
    Longitude: Optional[float|str]
    Address: Optional[str]
    City: Optional[str]
    Country: Optional[str]
    PostalCode: Optional[str]
    Description: Optional[str]
    Facilities: Optional[List[str]]

    @staticmethod
    def join_address(address, postcode) -> str:
        if postcode in address:
            return address
        elif postcode:
            return f'{address}, {postcode}'
        else:
            return address

    def to_hotel(self) -> model.Hotel:
        return model.Hotel(
            id=self.Id,
            destination_id=self.DestinationId,
            name=self.Name or '',
            description='',
            location=model.Location(
                lat=float(self.Latitude or Const.EMPTY_LATITUDE),
                lng=float(self.Longitude or Const.EMPTY_LONGITUDE),
                address=self.join_address(self.Address, self.PostalCode),
                city=self.City or '',
                country=Address.country_from_iso(self.Country) if self.Country else '',
            ),
            amenities=model.Amenities(
                general=self.Facilities or [],
                room=[],
            ),
            images=model.Images(
                rooms=[],
                site=[],
                amenities=[],
            ),
            booking_conditions=[],
        )


def fetch() -> Iterator[DTO]:
    url = 'http://www.mocky.io/v2/5ebbea002e000054009f3ffc'
    json = requests.get(url).json()

    dtos = [
        from_dict(data_class=DTO, data=obj)
        for obj in json
    ]
    for dto in dtos:
        yield dto


def to_hotels(dtos: Iterator[DTO]) -> Iterator[model.Hotel]:
    for dto in dtos:
        yield dto.to_hotel()


def extract() -> List[model.Hotel]:
    return list(to_hotels(fetch()))
