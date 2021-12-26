import json
from decimal import *


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
    count = 0
    for each in locations:
        print(each)
        create_geoJson(locations[each], each + '.js', "mydata" + str(count))
        count += 1



def get_activity(place):
    if place.get('activity'):
        return place['activity'][0]['activity'][0]['type']
    return 'UNKNOWN'


def fixLatLon(latLon):
    return latLon * 0.0000001


def round_to_x(number, x):
    number = Decimal(number)
    return round(number, x)


def create_geoJson(locations, photo_data, var_name="mydata"):
    """
    Creates a GeoJson files that leaflet can read
    """
    with open(photo_data, 'w') as write_file:
        write_file.write("var " + var_name + " = {\n")
        write_file.write('    "features":[\n')
        for location in locations:
            write_file.write('    {\n')
            write_file.write('        "properties": {},\n')
            write_file.write('        "type":"Feature",\n')
            write_file.write('        "geometry": {\n')
            write_file.write('            "type": "Point",\n')
            str_location = str(location)
            write_file.write('            "coordinates": [' + str_location + ']\n')
            write_file.write('        }\n')
            write_file.write('    },\n')
        write_file.write('    ]')
        write_file.write(',"type":"FeatureCollection"};')