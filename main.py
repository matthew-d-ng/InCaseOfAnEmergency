# Project Name: In Case of Emergency
# Group Number: 22
# Client: Iman, School of Computer Science and Statistics

from flask import Flask, render_template
from flask_mysqldb import MySQL
app = Flask(__name__)

import math

earth_rad = 6371 #km

# Config MySQL

# MySQL is running on port 3306, w/c TCD blocks. Fix: Conenct to a different Wifi.
# To connect to our remote server, uncomment the lines below:
# app.config['MYSQL_HOST'] = '146.185.180.168'
# app.config['MYSQL_USER'] = 'sulla'
# app.config['MYSQL_PASSWORD'] = 'pass' # PLEASE DO NOT PUSH THE ACTUAL VALUE TO GITHUB.
# -----------------------------------------------------------------------------------

# To run locally, uncomment the lines below:
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'pass' # Change to your own root password. DO NOT PUSH TO GITHUB.
# -----------------------------------------------------------------------------------

app.config['MYSQL_DB'] = 'myflask'
app.config['MYSQL_CHARSET'] = 'utf8mb4'
app.config['MYSQL_INIT_COMMAND'] = 'SET NAMES utf8mb4;'
app.config['MYSQL_INIT_COMMAND'] = 'SET CHARACTER SET utf8mb4;'
app.config['MYSQL_INIT_COMMAND'] = 'SET character_set_connection=utf8mb4;'
app.config['MYSQL_INIT_COMMAND'] = 'SET SESSION CHARACTER_SET_SERVER = utf8mb4;'
app.config['MYSQL_INIT_COMMAND'] = 'SET SESSION CHARACTER_SET_DATABASE = utf8mb4;'

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
def find_nearest(longitude, latitude, distance):
    # Create SQL cursor.
    cur = mysql.connection.cursor()  

    # Euclidean distance b/w two points.
    # d = sqrt((x2-x1)^2 + (y2-y1)^2)
    d_sqrd = distance * distance
    query = 'SELECT place FROM earthquakes WHERE POW(latitude - , ' + latitude + \
            ', 2) + POW(longitude - ' + longitude + ', 2) < ' + d_sqrd +  ';'
    result = cur.execute(query)

    # This currently only prints raw data.
    print(query, "\n")

    cur.close()


# Request to get the nearest places.
@app.route('/earthquake', methods=['GET', 'POST'])
def find_nearest():
    if request.method == 'POST' and form.validate():


    return render_template('find_nearest.html', related_earthquakes=result)


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
