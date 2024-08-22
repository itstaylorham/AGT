import os
import json
import matplotlib.pyplot as plt
from datetime import datetime

def plot_sensor_data(data, title):
    # Extract timestamps and sensor data
    timestamps = [entry['Timestamp'] for entry in data]
    temperatures = [entry['Temperature'] for entry in data]
    moistures = [entry['Moisture'] for entry in data]
    lights = [entry['Light'] for entry in data]
    conductivities = [entry['Conductivity'] for entry in data]

    # Create a 2x2 grid of subplots
    fig, axs = plt.subplots(2, 2, figsize=(15, 6), sharex=True)
    fig.suptitle(title, fontsize=16)

    # Plot Temperature data
    axs[0, 0].plot(timestamps, temperatures, label='Temperature', color='maroon', linestyle='-.', marker='o', markersize=5, linewidth=2)
    axs[0, 0].set_ylabel('Temperature')
    axs[0, 0].legend()
    axs[0, 0].grid(True)

    # Plot Moisture data
    axs[0, 1].plot(timestamps, moistures, label='Moisture', color='blue', linestyle='-.', marker='s', markersize=5, linewidth=2)
    axs[0, 1].set_ylabel('Moisture')
    axs[0, 1].legend()
    axs[0, 1].grid(True)

    # Plot Light data
    axs[1, 0].plot(timestamps, lights, label='Light', color='green', linestyle='-.', marker='^', markersize=5, linewidth=2)
    axs[1, 0].set_ylabel('Light')
    axs[1, 0].legend()
    axs[1, 0].grid(True)

    # Plot Conductivity data
    axs[1, 1].plot(timestamps, conductivities, label='Conductivity', color='orange', linestyle=':', marker='d', markersize=5, linewidth=2)
    axs[1, 1].set_ylabel('Conductivity')
    axs[1, 1].legend()
    axs[1, 1].grid(True)

    # Set x-label for bottom row
    axs[1, 0].set_xlabel('Timestamp')
    axs[1, 1].set_xlabel('Timestamp')

    plt.tight_layout()
    plt.show()

# Read from date folders and json files
read_files_dir = './files/read_files/'

# Find the most recent folder
latest_data = max(
    [f for f in os.listdir(read_files_dir) if os.path.isdir(os.path.join(read_files_dir, f))],
    key=lambda date_str: datetime.strptime(date_str, '%Y-%m-%d')
)

# Construct the path to the most recent JSON file
test_json_file_path = os.path.join(read_files_dir, latest_data, f'AGT-{latest_data}.json')

# Load and plot test data
with open(test_json_file_path, 'r') as file:
    test_data = json.load(file)
plot_sensor_data(test_data, 'Test Data Average')

# Load and plot control data
control_json_file_path = './files/batches/t_parsley.json'
with open(control_json_file_path, 'r') as file:
    control_data = json.load(file)
plot_sensor_data(control_data, 'Control Data Average')
