#!/usr/bin/env python3

# This script gets the status of 1 device by it's name, reading from config file

import json
import os
from subprocess import PIPE, run

import cgi
import cgitb

success = True
error = ""

arguments = cgi.FieldStorage()
deviceName = arguments['device'].value

configFile = open('config.json')
allDevices = json.load(configFile)
configFile.close()

device = None
for deviceTmp in allDevices:
    if deviceTmp['parameterName'] == deviceName:
        device = deviceTmp

if device is None:
    success = False
    error = "Cannot find device"
if success is True:
    #deviceResponses = []
    currentResponse = None

    deviceClass = device['className']
    deviceType = device['type']
    deviceParameter = device['parameterName']
    deviceJSON = json.dumps(device)

    # Escape string before passing onto shell statement
    # Escaped characters: ", {, }, and space
    deviceJSONEscaped = deviceJSON.replace("\"", "\\\"").replace("{", "\\{").replace("}", "\\}").replace(" ", "")

    execStr = "python3 {}.py status {}".format(deviceClass, deviceJSONEscaped)
    
    #resultStr = run("python3 {deviceClass}.py status {deviceJSON}")
    resultStr = os.popen(execStr).read()

    result = json.loads(resultStr)

    #TODO: Output data
    success = result['success']
    if success == 0:
        success = False
        error = "Unable to get status, check your configuration file!"
    else:
        results = result["result"]
    
        #TODO: Support other controls
        currentResponse = {"parameterName":deviceParameter}
        if deviceType == "switch":
            currentResponse.update(results)
    
responseDict = dict()
if success == False:
    responseDict = {"success":0, "error":error}
else:
    responseDict = {"success":1, "status":currentResponse}

print("Content-Type: text/html; charset=utf-8")

print("\r\n")

print(json.dumps(responseDict))
