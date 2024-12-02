import datetime
import locale
import pytz
from flask import session

API_URL = "http://nginx_api:81"

def getAuthorizationHeader():
    token = session.get('token')
    if(not token):
        return None
    headers = {
        "Authorization": f"Bearer {token}"
    }
    return headers


def isoDateToHumanDate(date_obj):
    locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
    toronto_tz = pytz.timezone('America/Toronto')
    date_obj = datetime.datetime.strptime(date_obj, "%Y-%m-%d %H:%M:%S")

    date_obj = date_obj.astimezone(toronto_tz)
    return date_obj.strftime("%A %d %b %Y à %H:%M")