import datetime

class Earthquake:

    def __init__(self, place, magnitude, timestamp, latitude, longitude, depth):
        self.place = place
        self.magnitude = magnitude
        self.timestamp = timestamp
        self.latitude = latitude
        self.longitude = longitude
        self.depth = depth
