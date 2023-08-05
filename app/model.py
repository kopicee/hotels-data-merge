from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


@dataclass
class Location:
    lat: Optional[float]
    lng: Optional[float]
    address: str
    city: str
    country: str

@dataclass
class Amenities:
    general: List[str]
    room: List[str]

@dataclass
class Image:
    link: str
    description: str

@dataclass
class Images:
    rooms: List[Image]
    site: List[Image]
    amenities: List[Image]

class Hotel(BaseModel):
    id: str
    destination_id: int
    name: str
    description: str
    location: Location
    amenities: Amenities
    images: Images
    booking_conditions: List[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    "id": "iJhz",
                    "destination_id": 5432,
                    "name": "Beach Villas Singapore",
                    "location": {
                        "lat": 1.264751,
                        "lng": 103.824006,
                        "address": "8 Sentosa Gateway, Beach Villas, 098269",
                        "city": "Singapore",
                        "country": "Singapore"
                    },
                    "description": "Amenities include posh restaurant, plus an outdoor pool, a hot tub, and free parking.",
                    "amenities": {
                        "general": ["outdoor pool", "indoor pool", "breakfast"],
                        "room": ["aircon", "tv"]
                    },
                    "images": {
                        "rooms": [
                            { "link": "https://d2ey9sqrvkqdfs.cloudfront.net/0qZF/2.jpg", "description": "Double room" },
                            { "link": "https://d2ey9sqrvkqdfs.cloudfront.net/0qZF/4.jpg", "description": "Bathroom" }
                        ],
                        "site": [
                            { "link": "https://d2ey9sqrvkqdfs.cloudfront.net/0qZF/1.jpg", "description": "Front" }
                        ],
                        "amenities": [
                            { "link": "https://d2ey9sqrvkqdfs.cloudfront.net/0qZF/0.jpg", "description": "RWS" }
                        ]
                    },
                    "booking_conditions": [
                        "Pets are not allowed.",
                        "WiFi is available in all areas and is free of charge.",
                    ]
                }
            ]
        }
    }
