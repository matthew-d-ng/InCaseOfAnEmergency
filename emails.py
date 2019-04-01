import yagmail, math
from feed_reader import get_latest_quakes
from earthquake import Earthquake
from wtforms import Form, StringField, validators
import geocoder, geopy, mysql.connector
from flask_mysqldb import MySQL

EMAIL = "incaseofanemergencySWE@gmail.com"
PASSWORD = "aeamthhhkrowsjdm"

#replace with your local credentials or sullas server ones
mysql = mysql.connector.connect(user='root', password='pass',
                              host='localhost',
                              database='icoe')

class email_form(Form):
    email = StringField('Email Address', [validators.Length(min=6, max=35)])

class email_reciever:
    def __init__(self, id,  email, magnitude, location):
        self.id = id
        self.email = email
        self.magnitude = magnitude
        self.location = location

def get_mailing_list():
    cur = mysql.cursor()
    query = ("SELECT * FROM MailingList;")
    cur.execute(query)
    records = cur.fetchall()
    
    user_list = []
    for row in records:
        temp = email_reciever(row[0], row[1], row[2], row[3])
        user_list.append(temp)
    return user_list


def get_refined_mailing_list():
    full_mailing_list = get_mailing_list()
    earthquakeList = get_latest_quakes()
    latest_quake = earthquakeList[0]
    refined_mailing_list = []
    for user in full_mailing_list:
        loc = geocoder.google(user.location)
        coords = loc.latlng
        within_radius = is_within_radius(coords[0], coords[1], 100, latest_quake.latitude, latest_quake.longitude)
        if(latest_quake.magnitude >= user.magnitude and within_radius):
            refined_mailing_list.append(user.email_address)
    return refined_mailing_list

def get_earthquake_info():
    earthquakeList = get_latest_quakes()
    latest_quake = earthquakeList[0]
    body = "Earthquake time: " + latest_quake.time_string() + "\nMagnitude & Location: " + latest_quake.title + "\nLongitude: " + str(latest_quake.longitude) + "\nLatitude: " + str(latest_quake.latitude)
    return body

def send_emails():
    mailing_list = get_refined_mailing_list()
    yag = yagmail.SMTP(EMAIL, PASSWORD)
    body = get_earthquake_info()
    if(len(mailing_list) > 0):
        yag.send(mailing_list, 'Realtime earthquake notification!', body) 
    else:
        print("Empty mailing list")

def send_welcome_email(email_address):
    yag = yagmail.SMTP(EMAIL, PASSWORD)
    yag.send(email_address, "Earthquake mailing list", "Welcome to the mailing list!\n You will be kept up to date with earthquakes within 100km of your subscribed location and above your subscribed magnitude")
    print("email sent")

def is_within_radius(centre_lat, centre_long, radius, input_lat, input_long):
    coords_1 = [centre_lat, centre_long]
    coords_2 = [input_lat, input_long]
    distance = geopy.distance.distance(coords_1, coords_2)
    if((distance) <= radius):
        return True
    else:
        return False  
