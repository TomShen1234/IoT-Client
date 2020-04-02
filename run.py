#!/usr/bin/env python3

import json
import os
from subprocess import PIPE, run

import cgi
import cgitb

#cgitb.enable()

arguments = cgi.FieldStorage()
commandStr = arguments['command'].value

configFile = open('config.json')
allDevices = json.load(configFile)

command = json.loads(commandStr)
targetName = command['device']

targetDevice = None

success = True

response = {}

for device in allDevices:
    paramName = device['parameterName']
    devType = device['type']
    if paramName == targetName:
        targetDevice = device
        break

if targetDevice is None:
    success = False

if success is True:
    deviceClass = targetDevice['className']
   
    # Append the device dictionary onto command
    command['deviceInfo'] = targetDevice
    commandJSONEscaped = json.dumps(command).replace("\"", "\\\"").replace("{", "\\{").replace("}", "\\}").replace(" ", "")

    execStr = "python3 {}.py set {}".format(deviceClass, commandJSONEscaped)

    resultStr = os.popen(execStr).read()

    #print("Content-Type: text/html; charset=utf-8")
    #print("\r\n")
    #print("Hello!")
    #print(resultStr)
    #exit()

    response = json.loads(resultStr)
else:
    response = {"success":0, "error":"Can not find device"}

print("Content-Type: text/html; charset=utf-8")

print("\r\n")

print(json.dumps(response))
