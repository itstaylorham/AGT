# -*- coding: utf-8 -*-
import json
import os
import pandas as pd
from flowercare import FlowerCare, FlowerCareScanner
import time
from datetime import datetime
import sys
import threading
import itertools
import bluepy
import configparser
import ast

def load_config():
    """Load configuration from setup.cfg file"""
    config = configparser.ConfigParser()
    config.read('setup.cfg')
    
    # Parse the MAC addresses string into a list
    try:
        device_macs = ast.literal_eval(config['DEVICE']['macs'])
        if not isinstance(device_macs, list):
            raise ValueError("MAC addresses must be in list format")
    except (KeyError, SyntaxError, ValueError) as e:
        print(f"Error reading MAC addresses from config: {e}")
        sys.exit(1)
        
    return device_macs

# Load MAC addresses from config
device_macs = load_config()

print(f"Loaded {len(device_macs)} MAC addresses from config")

# Initialize the scanner with BT interface
print("\n>>> Finding devices\n")
scanner = FlowerCareScanner(
    interface='hci0',
    callback=lambda device: print(device.addr)
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
        print(f"\n>>> Sensor readings for device {device_mac}\n")
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

        # Query the information for the specified device
        try:
            flower_care_device = FlowerCare(
                mac=device_mac, 
                interface='hci0'
            )
            data = {
                'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                'MAC': flower_care_device.mac, 
                'Temperature': flower_care_device.real_time_data.temperature, 
                'Moisture': flower_care_device.real_time_data.moisture,
                'Light': flower_care_device.real_time_data.light, 
                'Conductivity': flower_care_device.real_time_data.conductivity
            }
            sensor_data_list.append(data)
        except Exception as e:
            print(f"Error reading device {device_mac}: {e}")
            continue

        # Display current readings
        pd.set_option("display.max_rows", None)
        pd.set_option("display.max_columns", None)
        df = pd.DataFrame(sensor_data_list)
        print(df)
    else:
        print(f"Device {device_mac} not found during scan")

# Save data to daily folder
timestamp = datetime.now().strftime("%Y-%m-%d")
daily_folder = os.path.join("files/read_files", timestamp)

# Create directory if it doesn't exist
if not os.path.exists(daily_folder):
    os.makedirs(daily_folder)

# Define daily JSON file path
daily_json_file = os.path.join(daily_folder, f'AGT-{timestamp}.json')

# Load or create daily data
if os.path.exists(daily_json_file):
    with open(daily_json_file, 'r') as f:
        daily_data = json.load(f)
else:
    daily_data = []

# Prepare DataFrame for JSON
if sensor_data_list:
    df = pd.DataFrame(sensor_data_list)
    df["Timestamp"] = pd.to_datetime(df["Timestamp"]).dt.strftime("%Y-%m-%d %H:%M:%S")
    df["MAC"] = df["MAC"].astype(str)

    # Append new records
    daily_data.extend(df.to_dict(orient='records'))

    # Save updated data
    with open(daily_json_file, 'w') as f:
        json.dump(daily_data, f)

    # Update sesh.json
    sesh_file = 'sesh.json'
    if os.path.exists(sesh_file):
        with open(sesh_file, 'r') as f:
            sesh_data = json.load(f)
    else:
        sesh_data = []

    sesh_data.extend(df.to_dict(orient='records'))
    
    with open(sesh_file, 'w') as f:
        json.dump(sesh_data, f, indent=4)

done = True