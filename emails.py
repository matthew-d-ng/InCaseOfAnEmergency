import yagmail, math
from feed_reader import get_latest_quakes
from earthquake import Earthquake
from wtforms import Form, StringField, validators


EMAIL = "incaseofanemergencySWE@gmail.com"
PASSWORD = "aeamthhhkrowsjdm"

class email_form(Form):
    email = StringField('Email Address', [validators.Length(min=6, max=35)])

class email_reciver:
    def __init__(self, email_address, magnitude, location):
        self.email_address = email_address
        self.magnitude = magnitude
        self.location = location

def get_mailing_list():
    #todo
    #query the database to get the mailing list 

    return ["omullan99@gmail.com"]

def get_earthquake_info():
    earthquakeList = get_latest_quakes()
    latest_quake = earthquakeList[0]
    body = "Earthquake time: " + latest_quake.timestring + "\nMagnitude & Location: " + latest_quake.title + "\nLongitude: " + str(latest_quake.longitude) + "\nLatitude: " + str(latest_quake.latitude)

    return body

def send_emails():
    yag = yagmail.SMTP(EMAIL, PASSWORD)
    mailing_list = get_mailing_list()
    body = get_earthquake_info()
    yag.send(mailing_list, 'Realtime earthquake notification!', body)


def is_within_radius(centre_lat, centre_long, radius, input_lat, input_long):
    distance = math.sqrt((input_lat - centre_lat)**2 + (input_long - centre_long)**2)
    if(distance <= radius):
        return True
    else:
        return False  