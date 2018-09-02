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
url = "https://pizza-admin.herokuapp.com/api/receipt/Napoli"
headers = {"X-Auth-Token": auth, "X-User-Id": userId}
resp = requests.get(url, headers=headers)
resp = resp.json()
print(resp)
resp = resp['data']

if resp != None:
    # info for receipt
    cart = resp['cart']
    orderNum = resp['orderNum']
    orderType = resp['deliveryType']

    subtotal = resp['subtotal']
    tax = resp['tax']
    tip = resp['tip']
    deliv = resp['delivery']
    total = float(subtotal) + float(tax) + float(tip) + float(deliv)
    total = str(total)

    date = resp['createdAt']
    date = date.split(':')
    date = date[0]
    phone = resp['phone']

    #print header
    printer.justify('C')
    printer.setSize('M')
    printer.println("Napoli Pizza")
    printer.setSize('S')
    printer.println("855 Ridge Road West")
    printer.println("")
    printer.justify('L')
    printer.println("ORDER NUM: " + orderNum)
    printer.println("ORDER TYPE: " + orderType)
    printer.println("DATE: " + date)
    printer.println("")

    #print items ordered
    for item in cart:
        printer.justify('L')
        printer.println(item['name'])
        printer.justify('R')
        printer.println(item['price'])

    #print totals
    printer.justify('R')
    printer.println('Subtotal: $' + subtotal)
    printer.println('Delivery: $' + deliv)
    printer.println('Tip: $' + tip)
    printer.println('Tax: $' + tax)
    printer.println('Total: $' + total)
    printer.println("")
    printer.justify('C')
    printer.println("Thank You")