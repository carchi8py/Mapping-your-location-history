import exifread
import os
import sys

def convert_to_degree(number):
    #convert from IfdTag to a string so we can parse it
    number = str(number)
    #Remove [] from the ends
    number = number[1:-1]
    d, m, s = number.split(',')
    s_t, s_b = s.split('/')
    s = float(s_t) / float(s_b)
    s = str(s)
    dd = float(d) + float(m)/60 + float(s)/3600
    return dd

def read_image(image, full_path):
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
    
def create_geoJson(locations):
    data_file = os.path.join("/Users/carchi/Documents/workspace/Where i have been", 'dataset.js')
    with open(data_file, 'w') as write_file:
        write_file.write("var mydata = {\n")
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
            
    
        
locations = {}

iphoto_location = "/Users/carchi/Pictures/Photos Library.photoslibrary/"
masters = "Masters"
start_location = os.getcwd()
os.chdir(iphoto_location)
years = os.listdir(os.path.join(os.getcwd(), masters))
for year in years:
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
                        print locations
                        create_geoJson(locations)
                    location = read_image(image, full_path)
                    if not location:
                        i += 1
                        continue
                    if location in locations:
                        locations[location] += 1
                    else:
                        locations[location] = 1
                    i += 1
                print locations
sys.exit(1)
