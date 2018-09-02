#!/usr/bin/python

from Adafruit_Thermal import *
import requests

printer = Adafruit_Thermal("/dev/serial0", 19200, timeout=5)

#login to use API
def login():
  user = "Napoli"
  password = "PASSWORD"
  url = 'https://pizza-admin.herokuapp.com/api/login/'
  r = requests.post(url, data={"username": user, "password": password})
  r = r.json()
  return r

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
    printer.println("ORDER NUM: " + str(orderNum))
    printer.println("ORDER TYPE: " + orderType)
    printer.println("DATE: " + date)
    printer.println("")

    #print items ordered
    for item in cart:
        printer.justify('L')
        printer.print1(str(item['name']))
        printer.justify('R')
        printer.print1(' $' + str(item['price']) + '\n')

    printer.feed(1)
    printer.justify('R')
    printer.println('Subtotal: $' + str(subtotal))
    printer.println('Delivery: $' + str(deliv))
    printer.println('Tip: $' + str(tip))
    printer.println('Tax: $' + str(tax))
    printer.println('Total: $' + str(total))
    printer.println("")
    printer.justify('C')
    printer.println("Thank You")
    printer.feed(3)