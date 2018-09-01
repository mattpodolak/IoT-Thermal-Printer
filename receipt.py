#!/usr/bin/python

from Adafruit_Thermal import *

printer = Adafruit_Thermal("/dev/serial0", 19200, timeout=5)

#print header
printer.setSize('L')
printer.println("Napoli Pizza")
printer.setSize('M')
printer.println("Order Num")
printer.setSize('S')
printer.boldOn()
printer.println("Date")
printer.boldOff()
printer.println("")

#print items ordered