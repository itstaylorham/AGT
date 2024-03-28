Agrotech Live is a data collection and analysis tools for agriculture applications.
IMPORTANT FOR BLUETOOTH ACCESS
- Give bluepy-helper sudo access before running anything.

## Giving bluepy-helper permissions on Linux

1. Make sure you have the bluepy package installed on your system. If not, you can install it using pip:
```pip install bluepy```

2. Navigate to the directory where the bluepy-helper file is located. It should be located at <path_to_bluepy>/bluepy/bluepy-helper
3. Give the bluepy-helper file the execute permission by running the following command:
```chmod +x bluepy-helper```

4. Give the bluepy-helper file the necessary capabilities by running the following command:
```sudo setcap 'cap_net_raw,cap_net_admin+eip' bluepy-helper```
This command will give the bluepy-helper file the `cap_net_raw` and `cap_net_admin` capabilities, which are necessary for it to access the system's Bluetooth adapter.

5. To verify if the capabilities have been correctly set, you can use the command
```getcap bluepy-helper```
This command will return the path of the file followed by the capabilities set on it.

6. Finally, to test if bluepy-helper has the necessary permissions, you can try running your script (that uses bluepy-helper) with `sudo` and see if it runs without any errors. If it runs without errors, it means that bluepy-helper has the necessary permissions to access the system's Bluetooth adapter.

## ENCOUNTERING PyQt5/6 ERRORS?
run this: "sudo apt install make g++ pkg-config libgl1-mesa-dev libxcb*-dev libfontconfig1-dev libxkbcommon-x11-dev python libgtk-3-dev
"


Command List:
>> scan: Runs the stats method from the scan.py module, likely to scan and display device or data statistics.

>> read: Executes the read.py script, which is designed to read data from some source.

>> find: Outputs the device_id from the find.py module, possibly showing the ID of a specific device.

>> sesh: Initiates a reading session and regularly runs a neural network model script model.py every 10 minutes.

>>  push: Begins a read session and then directly runs the neural network model script model.py.

>>  live: Starts a real-time application, possibly a live data dashboard, and then pauses for 10 minutes.

>>  new sesh: Deletes current session data and starts a new session, periodically reading data every 10 minutes.

>>  line: Visualizes data in a line plot by running the line.py script in the __tools__/plot/ directory.

>> trend: Visualizes data trends by running the trends.py script in the __tools__/plot/ directory.

>> fcast: Visualizes forecasted data by running the forecast.py script in the __tools__/plot/ directory.

>> fcast 3d: Visualizes forecasted data in 3D by running the data3d.py script in the __tools__/plot/ directory.

>> summary: Provides a summary of data by running the summary.py script in the __tools__/ directory.

>> corr: Performs a correlation analysis on the data by running the corr.py script in the __tools__/plot/ directory.

>> pred: Makes predictions on data by running the arima.py script in the __tools__/ directory.

>> cleaner: Cleans data by running the cleaner.py script in the __tools__/ directory.

>> nn: Executes a neural network script nn.py in the __tools__/neural_net/ directory.

>> export: Reads the current session data, cleans it, and saves it as a JSON file in the __files__/export/ directory.

>> export csv: Reads the current session data, cleans it, and saves it as a CSV file in the __files__/export/ directory.

>> export xl: Reads the current session data, cleans it, and saves it as an Excel file in the __files__/export/ directory.


These commands should work regardless of your BLE transmitter configuration.


