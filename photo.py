import exifread
import os
import sys
from decimal import *

    
def convert_to_degree(number):
    """
    Takes a Degree in the Degree min second format and covert it to a decimal
    """
    #convert from IfdTag to a string so we can parse it
    number = str(number)
    #Remove [] from the ends
    number = number[1:-1]
    degree, min, sec = number.split(',')
    s_t, s_b = sec.split('/')
    sec = (float(s_t) / float(s_b)) / 3600
    dd = Decimal(degree) + Decimal(min)/60 + Decimal(sec)
    #Limit us to 4 places after the point
    dd = round(dd, 4)
    return dd

def read_image(image, full_path):
    """
    Read an Image, and get the EXIF data that include the GPS data
    """
    with open(os.path.join(full_path, image), 'rb') as f:
        if image.find('JPG') == -1:
            return
        tags = exifread.process_file(f)
        try:
            lat = tags['GPS GPSLatitude']
            long = tags['GPS GPSLongitude']
            lat_directions = tags['GPS GPSLatitudeRef']
            long_direction = tags['GPS GPSLongitudeRef']
                
            lat_degree = convert_to_degree(lat)
            if str(lat_directions) == "S":
                lat_degree = -lat_degree
            long_degree = convert_to_degree(long)
            if str(long_direction) == "W":
                long_degree = -long_degree
            return str(long_degree) + ',' + str(lat_degree)
        except:
            return
    
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

def get_photos(iphoto_location, photo_data):
    """
    Finds all photos in Iphoto or Photo libaray
    """
    locations = {}
    masters = "Masters"
    start_location = os.getcwd()
    os.chdir(iphoto_location)
    years = os.listdir(os.path.join(os.getcwd(), masters))
    for year in years:
        if year != "2017":
            continue
        print year
        months = os.listdir(os.path.join(os.getcwd(), masters, year))
        for month in months:
            full_path = os.path.join(os.getcwd(), masters, year, month)
            days = os.listdir(full_path)
            for day in days:
                full_path = (os.path.join(os.getcwd(), masters, year, month, day))
                times = os.listdir(full_path)
                for time in times:
                    full_path = os.path.join(os.getcwd(), masters, year, month, day, time)
                    images = os.listdir(full_path)
                    total_images = len(images)
                    i = 0
                    for image in images:
                        if not i%2000:
                            print str(i) + ' of ' + str(total_images) + " left"
                            #print locations
                            #create_geoJson(locations, photo_data)
                        location = read_image(image, full_path)
                        if not location:
                            i += 1
                            continue
                        print location
                        if location in locations:
                            locations[location] += 1
                        else:
                            locations[location] = 1
                        i += 1
                        create_geoJson(locations, photo_data)
