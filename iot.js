// IoT Web JS Scripts

function getControlState() {
    var host = window.location.host;
    var protocol = window.location.protocol;
    var fullLink = protocol + "//" + host + "/status.py";

    fetch(fullLink)
      .then((response) => {
	    return response.json();
      })
      .then((data) => {
        // Set content
		
        var success = data["success"];
        var htmlToSet = "Error";
        if (success == 1) {
            var allStatus = data["status"];
            allStatus.forEach(function(statusDict) {
                var controlName = statusDict['parameterName'];
                var deviceType = statusDict['deviceType'];
                var control = ".iot-status-" + controlName;
                // TODO: Support for other device types
                if (deviceType == "switch") {
                    var state = statusDict["state"];
                    $(control).html(booleanState(state));
                } else {
                    // TODO: Support other control types
                    $(control).html("Unsupported Device");
                }
            });
        } else {
            getStatusError();
        }
      })
      .catch(err => {
        getStatusError();
      });
}

// Set state for 'switch' control
function setControlState(input) {
    var host = window.location.host;
    var protocol = window.location.protocol;
    var fullLink = protocol + "//" + host + "/run.py";

    var tableClassName = 'iot-status-' + input;

    // Read current state from HTML (search by class) and parse the info
    var currentStateHTML = document.getElementsByClassName(tableClassName)[0].innerHTML;
    var currentState = boolFromString(currentStateHTML);
        
    // Format GET request
    var commandDict = {device: input, state: !currentState}; 

    // Convert to JSON string
    var commandStr = JSON.stringify(commandDict);

    var finalCommand = "?command=" + commandStr;
    var finalURL = fullLink + finalCommand;

    // Add spinner to row
    var tableCellName = '.' + tableClassName;
    $(tableCellName).html('<div class="spinner-border spinner-border-sm"></div>');

    fetch(finalURL)
    .then((response) => {
        return response.json();
    })
    .then((data) => {
        var success = data['success'];
        if (success) {
            // Success, update table
            $(tableCellName).html(booleanState(!currentState));
        } else {
            // Failed, update table back to original and show alert
            $(tableCellName).html(booleanState(currentState));
            alert("Failed to toggle device!");
        }
    });
}

// TODO: Support other control types


function getStatusError() {
    $('.iot-status').html("Error");
}

// Converts bool into readable string
function booleanState(input) {
    if (input == true) {
        return "On";
    } else {
        return "Off";
    }
}

// Convert readable string into bool
function boolFromString(input) {
    if (input == "On") {
        return true;
    } else {
        return false;
    }
}

function showAbout() {
    alert("Made by Tom Shen, you can use this program as much as you like. However, no warranty is provided!");
}
