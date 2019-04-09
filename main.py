# Project Name: In Case of Emergency
# Group Number: 22
# Client: Iman, School of Computer Science and Statistics

from flask import (
    Flask,
    render_template,
    flash,
    redirect,
    url_for,
    session,
    request,
    logging,
)
from wtforms import Form, StringField, validators
from flask_mysqldb import MySQL
from feed_reader import get_latest_quakes
from earthquake import Earthquake
from emails import email_form, send_welcome_email

import logging
import datetime
import dateutil.parser
import math
import geocoder
import json
from db_realtime_updater import db_realtime

app = Flask(__name__)

earth_rad = 6371  # km
mysql = MySQL()

# Config MySQL

# MySQL is running on port 3306, w/c TCD blocks. Fix: Conenct to a different Wifi.
# To connect to our remote server, uncomment the lines below:
app.config['MYSQL_HOST'] = '146.185.180.168'
app.config['MYSQL_USER'] = 'sulla'
app.config['MYSQL_PASSWORD'] = 'sulla' # PLEASE DO NOT PUSH THE ACTUAL VALUE TO GITHUB.
# -----------------------------------------------------------------------------------

# To run locally, uncomment the lines below:
# app.config["MYSQL_HOST"] = "localhost"
# app.config["MYSQL_USER"] = "root"
# app.config["MYSQL_PASSWORD"] = "pass"  # Change to your own root password. DO NOT PUSH TO GITHUB.
# -----------------------------------------------------------------------------------

app.config["MYSQL_DB"] = "icoe"
app.config["MYSQL_CHARSET"] = "utf8mb4"
app.config["MYSQL_INIT_COMMAND"] = "SET NAMES utf8mb4;"
app.config["MYSQL_INIT_COMMAND"] = "SET CHARACTER SET utf8mb4;"
app.config["MYSQL_INIT_COMMAND"] = "SET character_set_connection=utf8mb4;"
app.config["MYSQL_INIT_COMMAND"] = "SET SESSION CHARACTER_SET_SERVER = utf8mb4;"
app.config["MYSQL_INIT_COMMAND"] = "SET SESSION CHARACTER_SET_DATABASE = utf8mb4;"

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
def find_nearest(latitude, longitude, distance):
    # Create SQL cursor.
    cur = mysql.connect.cursor()

    # Euclidean distance b/w two points.
    # p = (p1, p2) ; q = (q1, q2)
    # d = sqrt((q1-p1)^2 + (q2-p2)^2)
    # d_sqrd = distance * distance

    last_month = datetime.datetime.now() - dateutil.relativedelta.relativedelta(months=6)
    last_month_first_date = last_month.replace(day=1)
    date = last_month_first_date.strftime("%Y-%m-%d")
    date_format = "%%Y-%%m-%%d"
    print(date)

    query = "SELECT id, title, mag, timestamp, latitude, longitude, depth \
            FROM earthquakes WHERE \
            POW(latitude-%s, 2) + POW(%s-longitude, 2) <= 1000 \
            AND timestamp >= STR_TO_DATE(%s, '%%Y-%%m-%%d')"
    print(query)
    cur.execute(query, (latitude, longitude, date))
    results = cur.fetchall()
    logging.info(results)


    # Create an array of all the earthquake occurrences.
    print("here!")
    occurences = []
    for occ in results:
        # [TODO] added a temp ID.
        print(occ[6])
        occurences.append(
            Earthquake(occ[0], occ[1], occ[2], occ[3], occ[4], occ[5], occ[6])
        )

    cur.close()

    # Returns an array of Earthquakes.
    return occurences


# Mailing List Form
class MailingForm(Form):
    email = StringField("email", [validators.DataRequired()])
    location = StringField("location", [validators.DataRequired()])
    magnitude = StringField("magnitude", [validators.DataRequired()])


@app.route("/subscribe", methods=["GET", "POST"])
def subscribe():
    print("here")
    form = MailingForm(request.form)
    if form.validate():
        email = form.email.data
        loc = form.location.data
        mag = form.magnitude.data

        con = mysql.connect
        cur = con.cursor()
        query = 'INSERT INTO mailinglist (email, location, magnitude) VALUES ("{email}", "{loc}", {mag});'.format(
            email=email, loc=loc, mag=mag
        )
        print(query)
        res = cur.execute(query)
        con.commit()
        print(res)
        send_welcome_email(email)

    return redirect("/")


# Search Form
class SearchForm(Form):
    location = StringField("Location", [validators.DataRequired()])


@app.route("/", methods=["GET", "POST"])
def index():
    # This is the centre point of the map.
    # When unset, default is in Dublin, Ireland.
    center = {"latitude": 53.350140, "longitude": -6.266155}
    mform = MailingForm()
    sform = SearchForm(request.form)
    results = []

    sform.location.default = "Dublin, Ireland"

    if request.method == "POST" and sform.validate():        
        loc = sform.location.data
        coords = geocoder.google(loc)
        sform.location.default = coords.city
        latlng = coords.latlng
        print(coords)
        # Set centre as the search location.
        center = {"latitude": latlng[0], "longitude": latlng[1]}
        print(coords, " ", latlng[1], " ", latlng[0])
        # [TODO] This is returning None. [Rory]
        results = find_nearest(latlng[0], latlng[1], 100)

        if not results:
            #the flash line was breaking the code
            #flash("No results found!")
            center = {"latitude": latlng[0], "longitude": latlng[1]}

    earthquakes = []
    if len(results) != 0:
        for r in results:
            earthquakes.append(r.__dict__)

    json_str = json.dumps(earthquakes, indent=4, sort_keys=True, default=str)
    print(json_str)

    sform.process()


    # Requests data for the live feed.
    all_quakes = get_latest_quakes()
    earthQuakeList = all_quakes[0:9]
    APIKEY = "AIzaSyD1XIdaoi1PCBfttZe85pPnRBw25ZSADuU"

    return render_template(
        "home.html",
        earthQuakeList=earthQuakeList,
        APIKEY=APIKEY,
        searchform=sform,
        mailingform=mform,
        earthquakes=json_str,
        center=center,
    )

if __name__ == "__main__":
    app.run(debug=True)
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    monitor = db_realtime()
    monitor.run()
