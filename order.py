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
url = "https://pizza-admin.herokuapp.com/api/print/Napoli"
headers = {"X-Auth-Token": auth, "X-User-Id": userId}
resp = requests.get(url, headers=headers)
resp = resp.json()
resp = resp['data']

if resp != None:
    # info for receipt
    cart = resp['cart']
    orderNum = resp['orderNum']
    orderType = resp['deliveryType']
    orderType = orderType.split(':')
    orderType = orderType[0]

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

    url = 'https://pizza-admin.herokuapp.com/api/check/Napoli/' + phone
    resp = requests.get(url, headers=headers)   
    resp = resp.json()
    resp = resp['data']
    name = resp['first_name'] + ' ' + resp['last_name']
    address_one = resp['address_one']
    address_two = resp['address_two']
    city = resp['city']
    postal_code = ['postal_code']

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

    #print customer info
    printer.println("CUSTOMER: ")
    printer.println(name)
    printer.println(address_one + ', ' + address_two)
    printer.println(postal_code + ', ' + city)

    #print items ordered
    for item in cart:
        printer.justify('R')
        item_name = str(item['name'])
        if len(item_name) < 7:
            printer.println(item_name + '\t\t\t\t\t $' + str(item['price']))
        elif len(item_name) < 12:
            printer.println(item_name + '\t\t\t\t $' + str(item['price']))
        else:
            printer.println(item_name + '\t\t\t $' + str(item['price'])) 
        
        custom = item['custom']
        special_notes = custom['specialNotes']
        addons = custom['addOns']
        pops = custom['pops']
        dips = custom['dips']

        try:
            toppings = custom['toppings']
            printer.println('Pizza 1')
            if toppings != null:
                for topping in toppings:
                    printer.println(topping)
            else:
                printer.println('No Toppings') 
        except:
            print('no toppings')  

        try:
            toppings2 = custom['toppings2']
            printer.println('Pizza 2')
            if toppings != null:
                for topping in toppings2:
                    printer.println(topping)
            else:
                printer.println('No Toppings') 
        except:
            print('no toppings') 

        try:
            toppings3 = custom['toppings3']
            printer.println('Pizza 3')
            if toppings != null:
                for topping in toppings3:
                    printer.println(topping)
            else:
                printer.println('No Toppings') 
        except:
            print('no toppings')  
        
        try:
            wings = custom['wings']
            printer.println('Wings: ' + wings) 
        except:
            print('no wings')
        
        try:
            pasta = custom['pasta']
            printer.println('Pasta: ' + pasta) 
        except:
            print('no pasta')

        if special_notes != null:
            printer.println(special_notes)
        
        if addons !=null:
            printer.println(addons)
        
        if pops != null:
            for pop in pops:
                printer.println(pop)
        
        if dips != null:
            for dip in dips:
                printer.println(dip)

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