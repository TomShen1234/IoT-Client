#!/usr/bin/env python3

# This script is a class and is not intended to be called through cgi
# TODO: Move to a separate folder outside of the cgi

import RPi.GPIO as io
import sys
import json

io.setwarnings(False)

io.setmode(io.BCM)

#io.setup(4, io.OUT)

mode = sys.argv[1]
deviceInfo = sys.argv[2]
response = dict()
#Get value of parameter
if mode == 'status':
    # Get state
    infoDict = json.loads(deviceInfo)
    
    gpioPort = infoDict["gpio"]
    io.setup(gpioPort, io.OUT)

    status = io.input(gpioPort)

    response = {"success":1, "result":{"state":status}}
elif mode == 'set':
    # Set state 
    device = json.loads(deviceInfo)
    infoDict = device['deviceInfo']

    gpioPort = infoDict["gpio"]
    io.setup(gpioPort, io.OUT)

    state = device["state"]
    io.output(gpioPort, state)

    response = {"success":1}
else:
    response = {"success":0, "error":"Invalid Mode"}

#print("Content-Type: text/html; charset=utf-8")

#print("\r\n")

print(json.dumps(response))

#io.cleanup()
