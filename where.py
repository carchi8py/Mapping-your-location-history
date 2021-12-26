import argparse
import logging

import google

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
    return parser.parse_args()


def main():
    options = parse_options()
    logging.debug("Starting Script")
    google.get_location_history(options.google)


if __name__ == "__main__":
    main()
