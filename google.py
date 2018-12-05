import json
from decimal import *
import photo

def get_locations(data_file):
    locations = {}
    with open(data_file, 'r') as f:
        data = json.load(f)
        places = data["locations"]
        for place in places:
            try:
                place["altitude"]
            except:
                place["altitude"] = 0
            lat = round_to_four(fixLatLon(place['latitudeE7']))
            lon = round_to_four(fixLatLon(place["longitudeE7"]))
            location_str = str(lon) + ',' + str(lat)
            if location_str in locations:
                locations[location_str] += 1
            else:
                locations[location_str] = 1
    photo.create_geoJson(locations, 'google.js', "mydata3")
            


def fixLatLon(latLon):
    return latLon * 0.0000001

def round_to_four(number):
    number = Decimal(number)
    return round(number, 4)