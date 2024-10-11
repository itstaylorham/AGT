# -*- coding: utf-8 -*-
import json
import os
import pandas as pd
from flowercare import FlowerCare, FlowerCareScanner
import time
from datetime import datetime, timedelta
import sys
import threading
import itertools
import bluepy

# List of MAC addresses for FlowerCare devices
device_macs = ["c4:7c:8d:6d:26:c9",
"c4:7c:8d:6d:24:ed",
"c4:7c:8d:6d:24:9e",
"c4:7c:8d:6d:4e:df"]

# Initialize the scanner with BT interface and a 
# custom callback for newly discovered devices.
print("");
print(">>> Finding devices")
print("");
scanner = FlowerCareScanner(
    interface='hci0',  # hci0 is default, explicitly stating for demo purpose
    callback=lambda device: print(device.addr)
    # any lambda with the device as the sole argument will do
)

sensor_data_list = []

# Perform a single scan
while True:
    try:
        devices = scanner.scan(timeout=10)
    except bluepy.btle.BTLEDisconnectError as e:
        print(f"BTLEDisconnectError occurred: {e}. Restarting the scan...")
        continue
    else:
        break

# Iterate over each device MAC address
for device_mac in device_macs:
    # Find the specified device by MAC address
    device = next((d for d in devices if d.addr == device_mac), None)
    if device is not None:
        # Query the information for the specified device.
        print("")
        print(f">>> Sensor readings for device {device_mac}")
        print("")
        done = False

        def animate():
            for c in itertools.cycle(['.  ', ' . ', '  .']):
                if done:
                    break
                sys.stdout.write('\rWorking ' + c)
                sys.stdout.flush()
                time.sleep(0.1)
            sys.stdout.write('\r              please wait ')
            current_time = datetime.now()
            sys.stdout.write('\r  *** Data saved as \'read_data.json\' on  ')
            sys.stdout.write(current_time.strftime("%Y-%m-%d %H:%M:%S"))
            sys.stdout.write(current_time.strftime(" *** "))

        t = threading.Thread(target=animate)
        t.start()

        # Query the information for the specified device.
        flower_care_device = FlowerCare(
            mac=device_mac, 
            interface='hci0'
        )
        data = {'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                'MAC': flower_care_device.mac, 
                'Temperature': flower_care_device.real_time_data.temperature, 
                'Moisture': flower_care_device.real_time_data.moisture,
                'Light': flower_care_device.real_time_data.light, 
                'Conductivity': flower_care_device.real_time_data.conductivity}
        sensor_data_list.append(data)

        # Pretty print device information
        pd.set_option("display.max_rows", None)
        pd.set_option("display.max_columns", None)

        df = pd.DataFrame(sensor_data_list)
        print(df)

# Save the data for all devices to a common JSON file
timestamp = datetime.now().strftime("%Y-%m-%d")
daily_folder = os.path.join("files/read_files", timestamp)

# Create a directory for the current day if it doesn't already exist
if not os.path.exists(daily_folder):
    os.makedirs(daily_folder)

# Define the daily JSON file path
daily_json_file = os.path.join(daily_folder, f'AGT-{timestamp}.json')

# Load existing data if the file exists, otherwise create an empty list
if os.path.exists(daily_json_file):
    with open(daily_json_file, 'r') as f:
        daily_data = json.load(f)
else:
    daily_data = []

# Convert the Timestamp column to a string before saving to JSON
df["Timestamp"] = pd.to_datetime(df["Timestamp"]).dt.strftime("%Y-%m-%d %H:%M:%S")
df["MAC"] = df["MAC"].astype(str)

# Append new records to the existing data
daily_data.extend(df.to_dict(orient='records'))

# Save the updated data to the daily JSON file
with open(daily_json_file, 'w') as f:
    json.dump(daily_data, f)

done = True

# Adding sensor data to the "sesh.json" file in the same format as daily data
file_name = 'sesh.json'
if os.path.exists(file_name):
    with open(file_name, 'r') as f:
        data = json.load(f)
else:
    data = []

# Convert the Timestamp column to a string before saving to JSON
df["Timestamp"] = pd.to_datetime(df["Timestamp"]).dt.strftime("%Y-%m-%d %H:%M:%S")
df["MAC"] = df["MAC"].astype(str)

# Append the entire dataframe as a single dictionary to the "sesh.json" file
data.append(df.to_dict(orient='list'))

with open(file_name, 'w') as f:
    json.dump(data, f)
