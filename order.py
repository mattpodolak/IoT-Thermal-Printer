#!/usr/bin/python

from Adafruit_Thermal import *
from main import login
import requests

printer = Adafruit_Thermal("/dev/serial0", 19200, timeout=5)

while 1:
    # try logging in
    resp = login()
    if resp['status'] == "success":
        resp = resp['data']
        auth = resp['authToken']
        userId = resp['userId']
        break
    else:
        print("error logging in")

#get order info
url = "https://pizza-admin.herokuapp.com/api/print/Napoli"
headers = {"X-Auth-Token": auth, "X-User-Id": userId}
resp = requests.get(url, headers=headers)
resp = resp.json()
resp = resp['data']

if resp != None:
    #print header
    printer.justify('C')
    printer.setSize('M')
    printer.println("Napoli Pizza")
    printer.setSize('S')
    printer.println("855 Ridge Road West")
    printer.println("")
    printer.justify('L')
    printer.println("ORDER NUM: ")
    printer.println("DATE: ")
    printer.println("")

    #print customer info

    #print order info