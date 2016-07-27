import argparse
import os

import photo

def main():
    options = parse_options()
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
    return parser.parse_args()

if __name__ == "__main__":
    main()  