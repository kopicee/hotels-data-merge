from app.ingest.normalize import *


def test_split_camel_case():
    assert Strings.split_camel_case('CamelCase') ==  ['Camel', 'Case']
    assert Strings.split_camel_case('camelCase') == ['camel', 'Case']
    assert Strings.split_camel_case('camelCase123') == ['camel', 'Case123']


def test_country_from_iso():
    assert Addresses.country_from_iso('SG') == 'Singapore', 'happy case with default args'
    assert Addresses.country_from_iso('JP', 'en', 'US') == 'Japan', 'happy case with explicit args'


def test_to_normalized_tags():
    f = Amenities.to_normalized_tags
    assert f('tv', 'iron') == ['iron', 'tv'], 'should return in sorted order'
    assert f('Aircon', 'Tub') == ['aircon', 'tub'], 'should return lowercase'
    assert f('HairDryer', 'DryCleaning') == ['dry cleaning', 'hair dryer'], 'should split camel case'
    assert f('WiFi') == ['wifi'], 'should handle wifi edge case correctly'
    assert f('aircon', 'aircon') == ['aircon'], 'should remove duplicates'
    assert f('dry cleaning', 'hair dryer') == ['dry cleaning', 'hair dryer'], 'should noop if format already correct'


def test_lat_long_precision():
    assert lat_long_precision(1.23) == 2, 'should return number of decimal places'
    assert lat_long_precision(1) == -1, 'non-float should return -1'
    assert lat_long_precision(Consts.EMPTY_LATLONG) == -1, 'EMPTY_LATLONG should return -1'
    assert lat_long_precision(Consts.EMPTY_LATLONG) == -1, 'EMPTY_LATLONG should return -1'


def test_argmax():
    assert argmax(1, 5) == 5
    assert argmax('a', 'abcde', len) == 'abcde'
    assert argmax('a', 'b', len) == 'a'
    assert argmax(1.2, 1.234, lat_long_precision) == 1.234


def test_hotels_normalize():
    h = model.Hotel(
        # Assume these don't change
        id='id',
        destination_id=12345,

        # For name and description, more verbose is better
        name='  name   ',
        description='   description ',

        # For location, prefer more precision/verbosity
        location=model.Location(
            lat=123.4,
            lng=Consts.EMPTY_LATLONG,
            address='  address  ',
            city='  city ',
            country='  country ',
        ),

        # For amenities and images, merge everything
        amenities=model.Amenities(
            general=['WiFi', 'DryCleaning', 'dry cleaning'],
            room=[],
        ),
        images=model.Images(rooms=[], site=[], amenities=[]),
        booking_conditions=[],
        created_at=None,
        updated_at=None,
    )

    now = datetime(year=1991, month=12, day=25)
    Hotels.normalize(h, now)

    assert h.name == 'name'
    assert h.description == 'description'
    assert h.location.lat == None, 'invalid longitude should make lat/lng empty'
    assert h.location.lng == None, 'invalid longitude should make lat/lng empty'
    assert h.location.address == 'address'
    assert h.location.city == 'city'
    assert h.location.country == 'country'
    assert h.amenities.general == ['dry cleaning', 'wifi']
    assert h.created_at == now
    assert h.updated_at == now
