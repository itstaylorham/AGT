import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# Function to load JSON data from a file
def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Load the data from the JSON file
data = load_json('/home/jeremy/Documents/AGT/__files__/batches/parsley.json')

# Extract data from JSON
timestamps = [item['Timestamp'] for item in data]
temperatures = [item['Temperature'] for item in data]
moistures = [item['Moisture'] for item in data]
lights = [item['Light'] for item in data]
conductivities = [item['Conductivity'] for item in data]

# Convert timestamps to datetime objects for better plotting
dates = [datetime.fromtimestamp(ts) for ts in timestamps]

# Create a figure with subplots
fig, axs = plt.subplots(4, 1, figsize=(10, 8), sharex=True)

# Plot Temperature
axs[0].plot(dates, temperatures, marker='o', color='r')
axs[0].set_ylabel('Temperature (°C)')
axs[0].set_title('Temperature Over Time')

# Plot Moisture
axs[1].plot(dates, moistures, marker='o', color='b')
axs[1].set_ylabel('Moisture (%)')
axs[1].set_title('Moisture Over Time')

# Plot Light
axs[2].plot(dates, lights, marker='o', color='g')
axs[2].set_ylabel('Light (lux)')
axs[2].set_title('Light Over Time')

# Plot Conductivity
axs[3].plot(dates, conductivities, marker='o', color='m')
axs[3].set_ylabel('Conductivity (µS/cm)')
axs[3].set_title('Conductivity Over Time')

# Format the x-axis to show date and time
axs[3].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
fig.autofmt_xdate()

# Add labels and show plot
plt.xlabel('Timestamp')
plt.tight_layout()
plt.show()

