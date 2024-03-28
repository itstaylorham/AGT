from flowercare import FlowerCare, FlowerCareScanner
import time
from datetime import datetime
import json
import os
import threading

# Function to display elapsed time
def display_elapsed_time(start_time, stop_event):
    while not stop_event.is_set():
        elapsed_time = time.time() - start_time
        print(f"\rElapsed time: {elapsed_time:.2f} seconds", end='')
        time.sleep(.1)

# Start the timer
start_time = time.time()
stop_event = threading.Event()
timer_thread = threading.Thread(target=display_elapsed_time, args=(start_time, stop_event))
timer_thread.start()

# Initialize the scanner
print("\nInitializing scanner...")
scanner = FlowerCareScanner(interface='hci0')
print("\nScanner initialized.")

# MAC address of the FlowerCare device
device_mac = "c4:7c:8d:6d:4e:df"

# Scan for devices and find the specific device
try:
    print("\nScanning for devices...")
    devices = scanner.scan(timeout=10)
    device = next((d for d in devices if d.addr == device_mac), None)
    if device is None:
        print("\nDevice not found")
        stop_event.set()
        exit()
    print("\nDevice found.")
except Exception as e:
    print(f"\nError during scanning: {e}")
    stop_event.set()
    exit()

# Connect to the FlowerCare device
try:
    print("\nConnecting to FlowerCare device...")
    flower_care_device = FlowerCare(mac=device_mac, interface='hci0')
    print("\nConnected to device.")
except Exception as e:
    print(f"\nError connecting to device: {e}")
    stop_event.set()
    exit()

# Fetch sensor data
print("\nFetching sensor data...")
sensor_data = {
    'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    'MAC': flower_care_device.mac,
    'Temperature': flower_care_device.real_time_data.temperature,
    'Moisture': flower_care_device.real_time_data.moisture,
    'Light': flower_care_device.real_time_data.light,
    'Conductivity': flower_care_device.real_time_data.conductivity
}
print("\nSensor data fetched.")

# Save data to JSON file
print("\nSaving data to file...")
data_file = 'flowercare_data.json'
if os.path.exists(data_file):
    with open(data_file, 'r') as f:
        data = json.load(f)
else:
    data = []

data.append(sensor_data)

with open(data_file, 'w') as f:
    json.dump(data, f, indent=4)

print("\nData saved successfully.")

# Stop the timer thread
stop_event.set()
timer_thread.join()
print(f"\nTotal time elapsed: {time.time() - start_time:.2f} seconds.")
