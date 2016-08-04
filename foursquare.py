import requests
import json
import sys
import photo
from decimal import *

def import_foursquare(token):
    url_template = 'https://api.foursquare.com/v2/users/self/checkins?limit=250&oauth_token={}&v=20131026&offset={}'
    oauth_token = token
    offset = 0
    data = []
    data_file = "oursquare.json"
    with open(data_file, 'w') as f:
        while True:
            response = requests.get(url_template.format(oauth_token, offset))
            if len(response.json()['response']['checkins']['items']) == 0:
                break
            data.append(response.json())
            offset += 250
        f.write(json.dumps(data, indent=2))
    return data
    
    
def get_locations(data_file):
    locations = {}
    for response in data_file:
        for item in response['response']['checkins']['items']:
            try:
                venue = item['venue']
                lat = round_to_four(venue['location']['lat'])
                lng = round_to_four(venue['location']['lng'])
                location_str = str(lng) + ',' + str(lat)
                if location_str in locations:
                    locations[location_str] += 1
                else:
                    locations[location_str] = 1
            except:
                continue
    photo.create_geoJson(locations, 'foursquare.js', "mydata2")

def round_to_four(number):
    number = Decimal(number)
    return round(number, 4)