import datetime
import dateutil
import logging
import json

class Earthquake:

    def __init__(self, db_id, title, magnitude, timestamp, latitude, longitude, depth):
        self.id = db_id
        self.title = title
        self.__set_magnitude(magnitude)
        self.__set_timestamp(timestamp)
        self.__set_latitude(latitude)
        self.__set_longitude(longitude)
        self.depth = depth

    def time_string(self):
        return self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
    
    # Dumps this object as a json.
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

    def __set_magnitude(self, magnitude):
        try:
            self.magnitude = float(magnitude)
        except ValueError:
            logging.warning("Failed to set magnitude for: %s", self.title)

    def __set_timestamp(self, timestamp):
        try:
            if isinstance(timestamp, str):
                self.timestamp = dateutil.parser.parse(timestamp)
            elif isinstance(timestamp, datetime.datetime):
                self.timestamp = timestamp
        except ValueError:
            logging.warning("Failed to set timestamp for: %s", self.title)

    def __set_latitude(self, latitude):
        try:
            self.latitude = float(latitude)
        except ValueError:
            logging.warning("Failed to set latitude for: %s", self.title)

    def __set_longitude(self, longitude):
        try:
            self.longitude = float(longitude)
        except ValueError:
            logging.warning("Failed to set longitude for: %s", self.title)
