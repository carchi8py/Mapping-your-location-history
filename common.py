

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