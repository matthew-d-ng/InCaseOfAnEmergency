import yagmail, math
from feed_reader import get_latest_quakes
from earthquake import Earthquake
from wtforms import Form, StringField, validators
import geocoder
from flask_mysqldb import MySQL

EMAIL = "incaseofanemergencySWE@gmail.com"
PASSWORD = "aeamthhhkrowsjdm"
mysql = MySQL()

class email_form(Form):
    email = StringField('Email Address', [validators.Length(min=6, max=35)])

class email_reciever:
    def __init__(self, email_address, magnitude, location):
        self.email_address = email_address
        self.magnitude = magnitude
        self.location = location

def get_mailing_list():
    '''
    cur = mysql.connect.cursor()
    query = 'SELECT * FROM MailingList'
 
    cur.execute(query)
    mailing_list = cur.fetchall()

    user_list = []
    for user in mailing_list:
        email_reciever(user[0], user[1], user[2])

    return user_list
    '''
    
    test_user = email_reciever("omullan99@gmail.com", 4.5, "Tokyo, Japan")
    return [test_user]

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


def is_within_radius(centre_lat, centre_long, radius, input_lat, input_long):
    distance = math.sqrt((input_lat - centre_lat)**2 + (input_long - centre_long)**2)
    if((distance) / 111 <= radius):
        return True
    else:
        return False  

