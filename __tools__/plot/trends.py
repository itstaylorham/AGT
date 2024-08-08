import os
import json
import matplotlib.pyplot as plt
import pandas as pd

def plot_sensor_data(test_data, control_data, title):
    # Convert to DataFrames for easy manipulation
    test_df = pd.DataFrame(test_data)
    control_df = pd.DataFrame(control_data)

    # Ensure 'Timestamp' is in datetime format
    test_df['Timestamp'] = pd.to_datetime(test_df['Timestamp'])
    control_df['Timestamp'] = pd.to_datetime(control_df['Timestamp'])

    # Merge the DataFrames on 'Timestamp' to align the data
    merged_df = pd.merge_asof(test_df.sort_values('Timestamp'), control_df.sort_values('Timestamp'), 
                               on='Timestamp', suffixes=('_test', '_control'))

    # Extract columns for plotting
    timestamps = merged_df['Timestamp']
    test_temperatures = merged_df['Temperature_test']
    control_temperatures = merged_df['Temperature_control']
    test_moistures = merged_df['Moisture_test']
    control_moistures = merged_df['Moisture_control']
    test_lights = merged_df['Light_test']
    control_lights = merged_df['Light_control']
    test_conductivities = merged_df['Conductivity_test']
    control_conductivities = merged_df['Conductivity_control']

    # Create a 2x2 grid of subplots
    fig, axs = plt.subplots(2, 2, figsize=(15, 6), sharex=True)
    fig.suptitle(title, fontsize=16)

    # Plot Temperature data
    axs[0, 0].plot(timestamps, test_temperatures, label='Test Temperature', color='maroon', linestyle='-.', marker='o', markersize=5, linewidth=2)
    axs[0, 0].plot(timestamps, control_temperatures, label='Control Temperature', color='red', linestyle='--', marker='x', markersize=5, linewidth=2)
    axs[0, 0].set_ylabel('Temperature')
    axs[0, 0].legend()
    axs[0, 0].grid(True)

    # Plot Moisture data
    axs[0, 1].plot(timestamps, test_moistures, label='Test Moisture', color='blue', linestyle='-.', marker='s', markersize=5, linewidth=2)
    axs[0, 1].plot(timestamps, control_moistures, label='Control Moisture', color='skyblue', linestyle='--', marker='P', markersize=5, linewidth=2)
    axs[0, 1].set_ylabel('Moisture')
    axs[0, 1].legend()
    axs[0, 1].grid(True)

    # Plot Light data
    axs[1, 0].plot(timestamps, test_lights, label='Test Light', color='green', linestyle='-.', marker='^', markersize=5, linewidth=2)
    axs[1, 0].plot(timestamps, control_lights, label='Control Light', color='lightgreen', linestyle='--', marker='v', markersize=5, linewidth=2)
    axs[1, 0].set_ylabel('Light')
    axs[1, 0].legend()
    axs[1, 0].grid(True)

    # Plot Conductivity data
    axs[1, 1].plot(timestamps, test_conductivities, label='Test Conductivity', color='orange', linestyle=':', marker='d', markersize=5, linewidth=2)
    axs[1, 1].plot(timestamps, control_conductivities, label='Control Conductivity', color='gold', linestyle='--', marker='*', markersize=5, linewidth=2)
    axs[1, 1].set_ylabel('Conductivity')
    axs[1, 1].legend()
    axs[1, 1].grid(True)

    # Set x-label for bottom row
    axs[1, 0].set_xlabel('Timestamp')
    axs[1, 1].set_xlabel('Timestamp')

    plt.tight_layout()
    plt.show()

# Load test data
test_json_file_path = './__files__/read_files/2024-04-30/AGT-2024-04-30.json'
with open(test_json_file_path, 'r') as file:
    test_data = json.load(file)

# Load control data
control_json_file_path = './__files__/batches/t_parsley.json'
with open(control_json_file_path, 'r') as file:
    control_data = json.load(file)

# Plot both test and control data
plot_sensor_data(test_data, control_data, 'Comparison of Test and Control Data')