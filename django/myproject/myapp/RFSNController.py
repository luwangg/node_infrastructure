import sys, time, os, pickle, urllib, json, datetime
import requests
from myproject.myapp.models import *
from django.core.mail import send_mail
from .NodeListener import *

""" Issues commands to NodeListeners. """

# TEST ENV
listeners = ["localhost:8000", "rfsn1:5035",
        "rfsn2:5035", "rfsn3:5035"]

# PRODUCTION
'''
listeners = ["localhost:8000", "sn1-wifi.vip.gatech.edu:8094",
        "sn1-wifi.vip.gatech.edu:8095", "sn2-wifi.vip.gatech.edu:8094"]
'''


def schedule(session, rfsn):
    """Schedules a Session on an RFSN."""
    print(rfsn)
    url = "http://" + rfsn.hostname + ":" + rfsn.port + "/generate_epochs/";
    print("SCHEDULE URL: " + url)
    req = requests.post(url, data=Util.dumps(session))
    file_drop(session, rfsn)
    return req

def file_drop(session, rfsn):
    """Schedules a copy-back of recorded data the day after records."""
    last_time = session.recordings[-1].starttime
    formatted_date = last_time.strftime("%d%m%Y")
    hour = (rfsn-1) * 2
    if hour < 0:
        #Probably local testing because rfsn = 0, log it and replace
        print("ERROR: Copy-back schedule time failed! Scheduling for 2:00AM...")
        hour = 2
    formatted_schedule_time = (last_time.replace(hour=hour)
        + datetime.timedelta(days=1)).strftime("%H:%M %m/%d/%Y")
    data = {'spath': session.startingpath, 'rfsnid': rfsn, 'fpath':'test',
        'date': formatted_date, 'game':'gatech',
        'scheduletime': formatted_schedule_time, }
    json_data = Util.dumps(data)
    url = "http://" + listeners[int(rfsn)] + "/filedrop/"
    req = requests.post(url, data=json_data)
    return req

def getatq():
    url = "http://" + listeners[int(1)] + "/getatq/";
    print("GetATQ URL: " + url)
    req = requests.post(url)
    return req
