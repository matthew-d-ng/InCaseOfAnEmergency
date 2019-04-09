import datetime
import dateutil
import logging
import json

class Earthquake:

    def __init__(self, timestamp, latitude, longitude, depth, magnitude, db_id, title):
        self.__set_timestamp(timestamp)
        self.__set_latitude(latitude)
        self.__set_longitude(longitude)
        self.__set_magnitude(magnitude)
        self.depth = depth
        self.id = db_id
        self.title = title
        

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
