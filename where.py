import argparse
import logging
import os

import google
import photos

name_to_level = {
    'CRITICAL': logging.CRITICAL,
    'ERROR': logging.ERROR,
    'WARNING': logging.WARNING,
    'INFO': logging.INFO,
    'DEBUG': logging.DEBUG,
}

def enable_logging(level):
    """
    Enable logging at the given level.
    :param level:
    """
    logging.basicConfig(level=name_to_level[level])


def parse_options():
    """
    Parse command line options.
    :return: parsed options
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--log', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], default='WARNING')
    parser.add_argument('--google', default='Location History.json')
    parser.add_argument('--photo', dest="photo", default=os.path.expanduser("~/Pictures/Photos Library.photoslibrary"),
                        help="Path to Apple Photos directory. The default is already set for Photos")
    return parser.parse_args()


def main():
    options = parse_options()
    enable_logging(options.log)
    logging.debug("Starting Script")
    logging.debug("Starting google")
    google.get_location_history(options.google)
    logging.debug("Start Photos")
    photos.get_locations(options.photo)


if __name__ == "__main__":
    main()
