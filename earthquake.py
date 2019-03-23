import datetime
import dateutil
import logging

class Earthquake:

    def __init__(self, db_id, title, magnitude, timestamp, latitude, longitude, depth):
        self.id = db_id
        self.title = title
        self.__set_magnitude(magnitude)
        self.timestamp = timestamp
        self.timestring = timestamp.strftime("%d-%m-%Y %H:%M:%S")
        self.__set_latitude(latitude)
        self.__set_longitude(longitude)
        self.depth = depth

    def __set_magnitude(self, magnitude):
        try:
            self.magnitude = float(magnitude)
            return True
        except ValueError:
            logging.warning("Failed to set magnitude for: %s", self.title)
            return False

    """def __set_timestamp(self, timestamp):
        try:
            self.timestamp = dateutil.parser.parse(timestamp)
            return True
        except ValueError:
            logging.warning("Failed to set timestamp for: %s", self.title)
            return False
    """
    def __set_latitude(self, latitude):
        try:
            self.latitude = float(latitude)
            return True
        except ValueError:
            logging.warning("Failed to set latitude for: %s", self.title)
            return False

    def __set_longitude(self, longitude):
        try:
            self.longitude = float(longitude)
            return True
        except ValueError:
            logging.warning("Failed to set longitude for: %s", self.title)
            return False
