import logging
import os
import exifread
from decimal import *
import common


def get_locations(photos_location):
    locations = {}
    masters = "originals"
    home_dir = os.getcwd()
    os.chdir(photos_location)
    photo_dirs = os.listdir(os.path.join(os.getcwd(), masters))
    for photo_dir in photo_dirs:
        logging.debug("photo_dir: %s", photo_dir)
        full_path = os.path.join(os.getcwd(), masters, photo_dir)
        photos = os.listdir(full_path)
        for photo in photos:
            location = read_image(photo, full_path)
            if location:
                locations[location] = 1
    os.chdir(home_dir)
    common.create_geoJson(locations, 'photo.js')



def read_image(image, full_path):
    """
    Read an Image, and get the EXIF data that include the GPS data
    """
    with open(os.path.join(full_path, image), 'rb') as f:
        if image.find('jpeg') == -1:
            return
        tags = exifread.process_file(f)
        try:
            return get_exifread_data(tags)
        except:
            return

def get_exifread_data(tags):
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

def convert_to_degree(number):
    """
    Covert degree min:sec to decimal
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
