import argparse
import os
import sys

import photo
import foursquare
import google

def main():
    options = parse_options()
    print "Starting google"
    #google.get_locations(options.google)
    print "Starting FourSquare"
    #data_file = foursquare.import_foursquare(options.foursquare)
    #foursquare.get_locations(data_file)
    #sys.exit(1)
    print "Starting photos"
    photo_data = os.path.join(options.save, 'photo.js')
    photo.get_photos(options.photo, photo_data)
    

def parse_options():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--photo', dest="photo",
                        default=os.path.expanduser(
                                "~/Pictures/Photos Library.photoslibrary"),
                        help="Path to Iphotos or Photos directory. The default is already set for Photos")
    parser.add_argument('-s', '--save', dest="save",
                       default = os.getcwd(),
                       help="Location to save data, default is CWD")
    parser.add_argument('-f', '--foursquare', dest="foursquare",
                        default="C2VVPGGTTRXZ1MFODZXTQRETCQFDBVU2E2S1GKRQEXIQJMMO",
                        help="Your fourquare oauth token")
    parser.add_argument('-g', '--google', dest="google",
                        default="LocationHistory.json",
                        help="Your google Json file")
    return parser.parse_args()

if __name__ == "__main__":
    main()  