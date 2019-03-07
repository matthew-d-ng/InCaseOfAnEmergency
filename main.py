from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

import math

#earthquake class for storing the rows queried from the database
class Earthquake:
    def __init__(self, magnitude, location_name, latitude, longitude, 
    year_occured, month_occured, day_occured):
        self.magnitude = magnitude           #float
        self.location_name = location_name   #String
        self.latitude = latitude             #double
        self.longitude = longitude           #double
        self.year_occured = year_occured     #int
        self.month_occured = month_occured   #int
        self.day_occured = day_occured       #int


class Boundary:
    def _init_(left, right, top, bottom):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom

# Find the distance between two places given their latitude and longitude.
# get_distance returns the distance betwen place1 and place2.
def get_distance(latitude, longitude, source_lat, source_long):
    # Δσ: central angle, φ1: latitude1,
    # φ2: latitude2, Δφ: difference b/w lat,
    # Δλ: difference b/w long
    #
    # Δσ = 2 * arcsin √(sin^2(Δφ/2) + cos(φ1) * cos(φ2) * sin^2(Δλ/2))
    # distance = rΔσ, where r is radius of the given sphere (earth)

    delta_lat = math.fabs(source_lat - latitude)
    delta_long = math.fabs(source_long - longitude)
    a = math.pow(math.sin(delta_lat / 2), 2)
    b = math.cos(source_lat) * math.cos(latitude)
    c = math.pow(math.sin(delta_long / 2), 2)
    central_angle = 2 * math.asin(math.sqrt(a + b * c))
    return earth_rad * central_angle


# get_boundary returns an object that contains the latitude and longitude
# values of a square boundary around a queries city.
def get_boundary(longitude, latitude):



@app.route('/')
def index():
    earthQuakeList = ["USGSted: Prelim M5.5 Earthquake central Mid-Atlantic Ridge Feb-25 15:05 UTC",
                    "USGSted: Prelim M5.5 Earthquake Macquarie Island region Feb-24 06:00 UTC",
                    "USGSted: Prelim M5.5 Earthquake southern Mid-Atlantic Ridge Feb-22 21:15 UTC",
                    "USGSted: Prelim M5.5 Earthquake near the coast of Ecuador Feb-22 10:40 UTC",
                    "USGSted: Prelim M7.5 Earthquake Peru-Ecuador border region Feb-22 10:17 UTC"]
    APIKEY = "AIzaSyD1XIdaoi1PCBfttZe85pPnRBw25ZSADuU"
    return render_template('home.html', earthQuakeList = earthQuakeList, APIKEY = APIKEY)

if __name__ == '__main__':
   app.run(debug = True)
