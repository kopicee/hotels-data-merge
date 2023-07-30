import json

from app.ingest.suppliers.supplier_5ebbea1f2e00002b009f4000 import *



def test_to_hotel():
    DTO(
        id='abc',
        destination=123,
        name='name',
        info='info',
        images=ImagesDTO(
            rooms=None, site=None, amenities=None
        ),
        lat=12.30,
        lng=45.60,
        address='address',
        amenities=None
    ).to_hotel()

def test_to_hotel_zero_lat_long():
    hotel = DTO(
        id='abc',
        destination=123,
        name='name',
        info='info',
        images=ImagesDTO(
            rooms=None, site=None, amenities=None
        ),
        lat=0,
        lng=None,
        address='address',
        amenities=None
    ).to_hotel()
    assert hotel.location.lat == Consts.EMPTY_LATITUDE
    assert hotel.location.lng == Consts.EMPTY_LONGITUDE

