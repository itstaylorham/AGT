import json
import matplotlib.pyplot as plt
from datetime import datetime

# Load the JSON data from the file
with open('/home/jeremy/Documents/AGT/sesh.json') as f:
    data = json.load(f)

# Define colors for each MAC address
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

# Extract data from the JSON into separate lists organized by MAC address
mac_data = {}

for entry in data:
    for i, mac in enumerate(entry['MAC']):
        if mac not in mac_data:
            mac_data[mac] = {
                'Timestamp': [],
                'Temperature': [],
                'Moisture': [],
                'Light': [],
                'Conductivity': []
            }
        mac_data[mac]['Timestamp'].extend(entry['Timestamp'])
        mac_data[mac]['Temperature'].extend(entry['Temperature'])
        mac_data[mac]['Moisture'].extend(entry['Moisture'])
        mac_data[mac]['Light'].extend(entry['Light'])
        mac_data[mac]['Conductivity'].extend(entry['Conductivity'])

# Convert timestamps to datetime objects
for mac in mac_data:
    mac_data[mac]['Timestamp'] = [datetime.strptime(ts, "%Y-%m-%d %H:%M:%S") for ts in mac_data[mac]['Timestamp']]

# Calculate the difference in change for each sensor type for each MAC address
diff_percentages_mac = {}

for mac, sensor_data in mac_data.items():
    diff_percentages_mac[mac] = {}
    for sensor_type in ['Temperature', 'Moisture', 'Light', 'Conductivity']:
        values = sensor_data[sensor_type]
        diff_values = [values[i] - values[i-1] for i in range(1, len(values))]
        diff_percentages_mac[mac][sensor_type] = sum(diff_values) / len(diff_values) if diff_values else 0

# Calculate the average change between consecutive readings across all MAC addresses
overall_diff_percentages = {sensor_type: [] for sensor_type in ['Temperature', 'Moisture', 'Light', 'Conductivity']}

for mac, sensor_diffs in diff_percentages_mac.items():
    for sensor_type, diff in sensor_diffs.items():
        overall_diff_percentages[sensor_type].append(diff)

for sensor_type, diffs in overall_diff_percentages.items():
    overall_diff_percentages[sensor_type] = sum(diffs) / len(diffs)

# Print the average change between consecutive readings across all MAC addresses
print("Average Change in Readings Across All MAC Addresses:")
for sensor_type, diff in overall_diff_percentages.items():
    print(f"  {sensor_type}: {diff:.2f}")

# Plot sensor data for each MAC address
for idx, (mac, sensor_data) in enumerate(mac_data.items()):
    # Selecting the last 144 entries
    sensor_data = {key: value for key, value in sensor_data.items()}
    
    fig, axs = plt.subplots(2, 2)

    for sensor_type, ax in zip(['Temperature', 'Moisture', 'Light', 'Conductivity'], axs.flat):
        ax.plot(sensor_data['Timestamp'], sensor_data[sensor_type], label=f'{sensor_type} - MAC: {mac[-5:]}', color=colors[idx], linewidth=0.95)
        ax.legend()
        ax.grid(linewidth=0.5, linestyle='--', color='gray')

    fig.suptitle(f"{mac[-5:]} PAST 24HR")

plt.show()
