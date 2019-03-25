import yagmail
from feed_reader import get_latest_quakes
from earthquake import Earthquake

EMAIL = "incaseofanemergencySWE@gmail.com"
PASSWORD = "aeamthhhkrowsjdm"

def get_mailing_list():
    #todo
    #query the database to get the mailing list 

    return []

def get_earthquake_info():
    earthquakeList = get_latest_quakes()
    latest_quake = earthquakeList[0]
    body = "Earthquake time: " + latest_quake.timestring + " Magnitude & Location: " + latest_quake.title + " Longitude: " + str(latest_quake.longitude) + " Latitude: " + str(latest_quake.latitude)

    return body

def send_emails():
    yag = yagmail.SMTP(EMAIL, PASSWORD)
    mailing_list = get_mailing_list()
    body = get_earthquake_info()
    yag.send(mailing_list, 'Realtime eaerthquake notification!', body)
