import matplotlib.pyplot as plt
from datetime import datetime
import json
import numpy as np

# Load JSON data from file
file_path = '/home/jeremy/Documents/AGT/sesh.json'
with open(file_path, 'r') as file:
    data = json.load(file)

# Extract sensor data and MAC addresses
mac_addresses = data[0]['MAC']
sensor_data = {sensor: [] for sensor in data[0] if sensor not in ['Timestamp', 'MAC']}

def generate_subplots(sensor_data, mac_addresses):
    num_sensors = len(sensor_data)
    num_rows = num_cols = int(num_sensors ** 0.5)  # For a square-like layout
    fig, axs = plt.subplots(num_rows, num_cols, figsize=(12, 12))  # Adjust figure size
    axs = axs.flatten()  # Flatten the axes array for easier indexing

    for i, (sensor_name, readings) in enumerate(sensor_data.items()):
        for entry in data:
            timestamps = [datetime.strptime(ts, "%Y-%m-%d %H:%M:%S") for ts in entry['Timestamp']]  # Extract timestamps for the current entry
            for j, device_readings in enumerate(entry[sensor_name]):  # Iterate over readings for the current sensor
                if j < len(mac_addresses):
                    # Ensure device readings are in list format
                    if isinstance(device_readings, list):
                        if len(timestamps) != len(device_readings):
                            # Interpolate or pad the data to ensure they have the same length
                            device_readings = np.interp(np.linspace(0, len(timestamps) - 1, len(device_readings)), np.arange(len(device_readings)), device_readings)
                        axs[i].plot(timestamps, device_readings, label=f"Device {j+1} ({mac_addresses[j]})")
        
        # Set major ticks to occur at the beginning of each day
        axs[i].xaxis.set_major_locator(plt.MaxNLocator(nbins=10))  # Adjust number of bins as needed
        axs[i].tick_params(axis='x', rotation=45)  # Rotate x-axis labels for better visibility
        
        # Set x-axis label, y-axis label, legend, and title for each subplot
        axs[i].set_xlabel('Time')  
        axs[i].set_ylabel(sensor_name)
        axs[i].legend(loc='upper right', fontsize='small') 
        axs[i].set_title(f"Trending data for {sensor_name}")

    # Hide any unused subplots
    for ax in axs[num_sensors:]:
        ax.axis('off')

    plt.tight_layout()
    plt.show()

# Generate subplots for each sensor
generate_subplots(sensor_data, mac_addresses)
