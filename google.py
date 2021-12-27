import json
from decimal import *
import common


def get_location_history(data_file):
    locations = {}
    # Number of places in Lat/Lon to Round to. 4 a good options. 5 would create to large of a data set to load in javascript
    # 3 = about 78 meters of percision
    # 4 = about 7.8 meters of percision
    # 5 = about 0.78 meters of percision
    round_to = 4
    with open(data_file, 'r') as f:
        data = json.load(f)
        places = data["locations"]
        for place in places:
            lat = round_to_x(fixLatLon(place['latitudeE7']), round_to)
            lon = round_to_x(fixLatLon(place['longitudeE7']), round_to)
            location_str = str(lon) + ',' + str(lat)
            activity = get_activity(place)
            if locations.get(activity):
                locations[activity][location_str] = 1
            else:
                locations[activity] = {location_str: 1}
    for count, (each, value) in enumerate(locations.items()):
        common.create_geoJson(value, each + '.js', "mydata" + str(count))



def get_activity(place):
    if place.get('activity'):
        return place['activity'][0]['activity'][0]['type']
    return 'UNKNOWN'


def fixLatLon(latLon):
    return latLon * 0.0000001


def round_to_x(number, x):
    number = Decimal(number)
    return round(number, x)
