<?php
// Initialization Script

$hostname = gethostname();

$configStr = file_get_contents('config.json');

// read config as assoc object
$config = json_decode($configStr, true);
?>
<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">

  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

  <title><?php echo $hostname; ?>: Controls</title>
</head>
<body>
  <nav class="navbar navbar-expand-md navbar-dark bg-dark">
    <a class="navbar-brand" href="/">IoT Device</a>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>

    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <ul class="navbar-nav mr-auto"> 
        <li class="nav-item"><a class="nav-link" href="javascript:showAbout()" onclick="">About</a></li>
      </ul>
    </div>
  </nav>
  <div class="container mt-3">
    <h1>Device: <?php echo $hostname; ?></h1>

    <table class="table table-bordered table-hover">
      <thead class="thead-light">
        <tr>
          <td>Device Name</td>
          <td>State</td>
          <td>Control</td>
        </tr>
      </thead>
      <tbody>
      <?php
	foreach ($config as $control) {
	  $controlDisplay = $control['displayName'];
	  $controlParam = $control['parameterName'];
	  $controlType = $control['type'];
      ?> 
        <tr>
	  <td><?php echo $controlDisplay.' ('.$controlParam.')'; ?></td>
          <!-- TODO: Other control types -->
	  <td>
	    <?php //echo switchStateReadable(getSwitchStatus($control)); ?>
	    <span class='iot-status <?php echo 'iot-status-'.$controlParam; ?>'>
	      <div class="spinner-border spinner-border-sm"></div>
            </span>
          </td>
      	  <td>
	    <button id='<?php echo 'iot-switch-'.$controlParam; ?>' class='iot-switch'>Toggle</button>
            <!--<div class="spinner-border spinner-border-sm"></div>-->
          </td>
        </tr>	
      <?php 
      }
      ?>
      </tbody>
    </table>
  </div>

  <script src="https://code.jquery.com/jquery-3.4.1.slim.min.js" integrity="sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n" crossorigin="anonymous"></script>
  <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
  <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js" integrity="sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6" crossorigin="anonymous"></script>
  <script src="iot.js"></script>

  <script type="text/javascript">
    getControlState();

    // Set action of Switch toggles
    $(document).ready(function() {
      $('.iot-switch').click(function() {
        var id = this.id;
        var idSplit = id.split('-');
        var name = idSplit[2]; // Get last object for the name

        setControlState(name);
      });
    });
  </script>
</body>
</html>
