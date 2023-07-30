import json

from app.ingest.suppliers.supplier_5ebbea002e000054009f3ffc import *



def test_to_hotel():
    dto = DTO(
        Id='abc',
        DestinationId=123,
        Name='name',
        Latitude=12.3,
        Longitude=45.6,
        Address='address',
        City='Singapore',
        Country='SG',
        PostalCode='12345',
        Description='',
        Facilities=['iron'],
    )
    h = dto.to_hotel()
    assert h.location.country == 'Singapore'


def test_to_hotel_zero_lat_long():
    dto = DTO(
        Id='abc',
        DestinationId=123,
        Name='name',
        Latitude=0,
        Longitude=0,
        Address='address',
        City='Singapore',
        Country='SG',
        PostalCode='12345',
        Description='',
        Facilities=['iron'],
    )

    h1 = dto.to_hotel()
    assert h1.location.lat == Consts.EMPTY_LATLONG
    assert h1.location.lng == Consts.EMPTY_LATLONG

    dto.Latitude = ''
    dto.Longitude = ''
    assert h1.location.lat == Consts.EMPTY_LATLONG
    assert h1.location.lng == Consts.EMPTY_LATLONG


def test_join_address():
    assert DTO.join_address('address', 'postcode') == 'address, postcode'
    assert DTO.join_address('address', '') == 'address'
    assert DTO.join_address('address 123', '123') == 'address 123'
    assert DTO.join_address('123 address', '123') == '123 address'
