#!/usr/bin/env python3

import json
import os
from subprocess import PIPE, run

import cgi
import cgitb

#cgitb.enable()

#from subprocess import PIPE, run

#def run(command):
#    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
#    return result.stdout

configFile = open('config.json')
allDevices = json.load(configFile)

deviceResponses = []
success = True
error = ""

for device in allDevices:
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
        break

    results = result["result"]
    
    #TODO: Support other controls
    currentResponse = {"parameterName":deviceParameter, "deviceType":deviceType}
    if deviceType == "switch":
        currentResponse.update(results)

    deviceResponses.append(currentResponse)

responseDict = dict()
if success == False:
    responseDict = {"success":0, "error":error}
else:
    responseDict = {"success":1, "status":deviceResponses}

print("Content-Type: text/html; charset=utf-8")

print("\r\n")

print(json.dumps(responseDict))
