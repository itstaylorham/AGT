import json
import matplotlib.pyplot as plt
import os
from datetime import datetime

# Load the JSON data from the file
with open('sesh.json') as f:
    data = json.load(f)

# Convert timestamp to integer if necessary
for i in range(len(data)):
    if type(data[i]['Timestamp'][0]) != int:
        data[i]['Timestamp'][0] = int(data[i]['Timestamp'][0])

# Extract data from the JSON into separate lists
timestamps = [i['Timestamp'][0] for i in data]
temperatures = [i['Temperature'][0] for i in data]
moistures = [i['Moisture'][0] for i in data]
lights = [i['Light'][0] for i in data] 
conductivities = [i['Conductivity'][0] for i in data]

# Create subplots for each sensor value
fig, axs = plt.subplots(2, 2)

# Plot the temperature data
axs[0, 0].plot(timestamps, temperatures, label='Temperature', color='#8B5E3C', linewidth=0.8)
axs[0, 0].legend()

# Plot the moisture data
axs[0, 1].plot(timestamps, moistures, label='Moisture', color='#87CEEB', linewidth=0.95)
axs[0, 1].legend()

# Plot the light data
axs[1, 0].plot(timestamps, lights, label='Light', color='#9ACD32', linewidth=0.95)
axs[1, 0].legend()

# Plot the conductivity data
axs[1, 1].plot(timestamps, conductivities, label='Conductivity', color='#228B22', linewidth=0.95)
axs[1, 1].legend()

# Add gridlines to each graph
axs[0, 0].grid(linewidth=0.5, linestyle='--', color='gray')
axs[0, 1].grid(linewidth=0.5, linestyle='--', color='gray')
axs[1, 0].grid(linewidth=0.5, linestyle='--', color='gray')
axs[1, 1].grid(linewidth=0.5, linestyle='--', color='gray')

# Change the title of the window
fig.suptitle("Sensor Data")

# Show the graph
plt.show()

