# Project Name: In Case of Emergency
# Group Number: 22
# Client: Iman, School of Computer Science and Statistics

from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from wtforms import Form, StringField, validators
from flask_mysqldb import MySQL
from feed_reader import get_latest_quakes
from earthquake import Earthquake
from emails import email_form

import logging
import datetime
import dateutil.parser
import math
import geocoder

app = Flask(__name__)

earth_rad = 6371 #km
mysql = MySQL()

# Config MySQL

# MySQL is running on port 3306, w/c TCD blocks. Fix: Conenct to a different Wifi.
# To connect to our remote server, uncomment the lines below:
app.config['MYSQL_HOST'] = '146.185.180.168'
app.config['MYSQL_USER'] = 'sulla'
app.config['MYSQL_PASSWORD'] = 'pass' # PLEASE DO NOT PUSH THE ACTUAL VALUE TO GITHUB.
# -----------------------------------------------------------------------------------

# To run locally, uncomment the lines below:
#app.config['MYSQL_HOST'] = 'localhost'
#app.config['MYSQL_USER'] = 'root'
#app.config['MYSQL_PASSWORD'] = 'pass' # Change to your own root password. DO NOT PUSH TO GITHUB.
# -----------------------------------------------------------------------------------

app.config['MYSQL_DB'] = 'icoe'
app.config['MYSQL_CHARSET'] = 'utf8mb4'
app.config['MYSQL_INIT_COMMAND'] = 'SET NAMES utf8mb4;'
app.config['MYSQL_INIT_COMMAND'] = 'SET CHARACTER SET utf8mb4;'
app.config['MYSQL_INIT_COMMAND'] = 'SET character_set_connection=utf8mb4;'
app.config['MYSQL_INIT_COMMAND'] = 'SET SESSION CHARACTER_SET_SERVER = utf8mb4;'
app.config['MYSQL_INIT_COMMAND'] = 'SET SESSION CHARACTER_SET_DATABASE = utf8mb4;'

mysql.init_app(app)

# Find the distance between two places given their latitude and longitude.
# get_distance returns the distance in km between place1 and place2.
# Parameters must be in radians.
def get_distance(latitude, longitude, source_lat, source_long):
    # Great Circle Distance
    # ca: central angle, lat1: latitude1,
    # lat2: latitude2, latdiff: difference b/w lat,
    # longdiff: difference b/w long
    #
    # ca = 2 * arcsin sqrt(sin^2(latdiff/2) + cos(lat1) * cos(lat2) * sin^2(longdiff/2))
    # distance = r(ca), where r is radius of the given sphere (earth)

    delta_lat = math.fabs(source_lat - latitude)
    delta_long = math.fabs(source_long - longitude)
    a = math.pow(math.sin(delta_lat / 2), 2)
    b = math.cos(source_lat) * math.cos(latitude)
    c = math.pow(math.sin(delta_long / 2), 2)
    central_angle = 2 * math.asin(math.sqrt(a + b * c))
    return earth_rad * central_angle

# find_nearest finds the nearest places to a given latitude and longitude
# using the basic Euclidian Distance formula.
# Returns a tuple of every earthquake occurrence data. (Tuple of tuples.)
def find_nearest(longitude, latitude, distance):
    # Create SQL cursor.
    cur = mysql.connect.cursor()

    # Euclidean distance b/w two points.
    # d = sqrt((x2-x1)^2 + (y2-y1)^2)
    d_sqrd = distance * distance

    query = 'SELECT place, mag, magType, time, latitude, longitude, depth FROM earthquakes WHERE POW(latitude -  ' + "(" + str(latitude) + ")" + \
            ', 2) + POW(longitude - ' + "(" + str(longitude) +  ")" + ', 2) < ' + str(d_sqrd) +  ';'
    logging.info(query)
    cur.execute(query)
    results = cur.fetchall()

    # Create an array of all the earthquake occurrences.
    occurences = []
    for occ in results:
        occurences.append(Earthquake(occ[0], occ[1], occ[2], occ[3], occ[4], occ[5], occ[6]))

    cur.close()

    # Returns an array of Earthquakes.
    return occurences

# Search Form
class SearchForm(Form):
    location = StringField('Location', [validators.DataRequired()])

APIKEY = "AIzaSyD1XIdaoi1PCBfttZe85pPnRBw25ZSADuU"
@app.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm(request.form)
    earthquakes = []

    if request.method == 'POST' and form.validate():
        loc = form.location.data
        print(loc, "\n")
        coords = geocoder.google(loc)
        print(coords)
        # [TODO] This is returning None. [Rory]
        earthquakes = find_nearest(45.15, -75.14, 100)

        if not earthquakes:
            flash('No results found!')
            return redirect('/')

    # Requests data for the live feed.
    all_quakes = get_latest_quakes()
    earthQuakeList = all_quakes[0:9]

    return render_template('home.html', earthQuakeList = earthQuakeList, APIKEY = APIKEY, form=form, earthquakes=earthquakes)

@app.route('/updates')
def updates():
    all_quakes = get_latest_quakes()
    earthQuakeList = all_quakes[0:9]

    return render_template('updates.html', earthQuakeList = earthQuakeList, APIKEY = APIKEY)

if __name__ == '__main__':
   app.run(debug = True)
