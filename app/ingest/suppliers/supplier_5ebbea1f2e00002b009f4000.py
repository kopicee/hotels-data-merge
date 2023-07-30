from dataclasses import dataclass, field
from typing import Iterator, List, Optional

from dacite import from_dict
import requests

from app import model
from app.ingest.normalize import Const, String, Address


"""
Sample:
  {
    "id": "iJhz",
    "destination": 5432,
    "name": "Beach Villas Singapore",
    "lat": 1.264751,
    "lng": 103.824006,
    "address": "8 Sentosa Gateway, Beach Villas, 098269",
    "info": "Located at the western tip of Resorts World Sentosa, guests at the Beach Villas are guaranteed privacy while they enjoy spectacular views of glittering waters. Guests will find themselves in paradise with this series of exquisite tropical sanctuaries, making it the perfect setting for an idyllic retreat. Within each villa, guests will discover living areas and bedrooms that open out to mini gardens, private timber sundecks and verandahs elegantly framing either lush greenery or an expanse of sea. Guests are assured of a superior slumber with goose feather pillows and luxe mattresses paired with 400 thread count Egyptian cotton bed linen, tastefully paired with a full complement of luxurious in-room amenities and bathrooms boasting rain showers and free-standing tubs coupled with an exclusive array of ESPA amenities and toiletries. Guests also get to enjoy complimentary day access to the facilities at Asia’s flagship spa – the world-renowned ESPA.",
    "amenities": ["Aircon", "Tv", "Coffee machine", "Kettle", "Hair dryer", "Iron", "Tub"],
    "images": {
      "rooms": [
        { "url": "https://d2ey9sqrvkqdfs.cloudfront.net/0qZF/2.jpg", "description": "Double room" },
        { "url": "https://d2ey9sqrvkqdfs.cloudfront.net/0qZF/4.jpg", "description": "Bathroom" }
      ],
      "amenities": [
        { "url": "https://d2ey9sqrvkqdfs.cloudfront.net/0qZF/0.jpg", "description": "RWS" },
        { "url": "https://d2ey9sqrvkqdfs.cloudfront.net/0qZF/6.jpg", "description": "Sentosa Gateway" }
      ]
    }
  },
  {
    "id": "f8c9",
    "destination": 1122,
    "name": "Hilton Tokyo Shinjuku",
    "lat": 35.6926,
    "lng": 139.690965,
    "address": null,
    "info": null,
    "amenities": null,
    "images": {
      "rooms": [
        { "url": "https://d2ey9sqrvkqdfs.cloudfront.net/YwAr/i10_m.jpg", "description": "Suite" },
        { "url": "https://d2ey9sqrvkqdfs.cloudfront.net/YwAr/i11_m.jpg", "description": "Suite - Living room" }
      ],
      "amenities": [
        { "url": "https://d2ey9sqrvkqdfs.cloudfront.net/YwAr/i57_m.jpg", "description": "Bar" }
      ]
    }
  }
"""

@dataclass
class ImageDTO:
    url: str
    description: str

@dataclass
class ImagesDTO:
    rooms: Optional[List[ImageDTO]] = field(default_factory=list)
    site: Optional[List[ImageDTO]] = field(default_factory=list)
    amenities: Optional[List[ImageDTO]] = field(default_factory=list)

@dataclass
class DTO:
    id: str
    destination: int
    name: str
    images: ImagesDTO
    info: Optional[str]
    lat: Optional[float]
    lng: Optional[float]
    address: Optional[str] = ''
    amenities: Optional[List[str]] = field(default_factory=list)

    def to_hotel(self) -> model.Hotel:
        return model.Hotel(
            id=self.id,
            destination_id=self.destination,
            name=self.name or '',
            description=self.info or '',
            location=model.Location(
                lat=self.lat or Const.EMPTY_LATITUDE,
                lng=self.lng or Const.EMPTY_LONGITUDE,
                address=self.address or '',
                city='',
                country='',
            ),
            amenities=model.Amenities(
                room=self.amenities or [],
                general=[],
            ),
            images=model.Images(
                rooms=[
                    model.Image(link=img.url, description=img.description)
                    for img in (self.images.rooms or [])
                ],
                site=[
                    model.Image(link=img.url, description=img.description)
                    for img in (self.images.site or [])
                ],
                amenities=[
                    model.Image(link=img.url, description=img.description)
                    for img in (self.images.amenities or [])
                ],
            ),
            booking_conditions=[],
        )


def fetch() -> Iterator[DTO]:
    url = 'https://www.mocky.io/v2/5ebbea1f2e00002b009f4000'
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
