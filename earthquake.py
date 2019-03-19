import datetime
import dateutil
import logging

class Earthquake:

    def __init__(self, place, magnitude, mag_type, timestamp, latitude, longitude, depth):
        self.place = place
        self.__set_magnitude(magnitude)
        self.mag_type = mag_type
        self.__set_timestamp(timestamp)
        self.timestring = timestamp
        self.__set_latitude(latitude)
        self.__set_longitude(longitude)
        self.depth = depth

    def __set_magnitude(self, magnitude):
        try:
            self.magnitude = float(magnitude)
            return True
        except ValueError:
            logging.warning("Failed to set magnitude for: %s", self.place)
            return False

    def __set_timestamp(self, timestamp):
        try:
            self.timestamp = dateutil.parser.parse(timestamp)
            return True
        except ValueError:
            logging.warning("Failed to set timestamp for: %s", self.place)
            return False

    def __set_latitude(self, latitude):
        try:
            self.latitude = float(latitude)
            return True
        except ValueError:
            logging.warning("Failed to set latitude for: %s", self.place)
            return False

    def __set_longitude(self, longitude):
        try:
            self.longitude = float(longitude)
            return True
        except ValueError:
            logging.warning("Failed to set longitude for: %s", self.place)
            return False
