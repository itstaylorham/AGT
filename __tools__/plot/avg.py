import json
import numpy as np
import matplotlib.pyplot as plt

# Load the data
with open('sesh.json') as f:
    data = json.load(f)

# Extract the light values and timestamps
light_values = [entry['Light'] for entry in data]
timestamps = [entry['Timestamp'] for entry in data]

# Since each timestamp is unique in your example, we don't need to calculate the average per timestamp
# We can directly plot the light values against the timestamps

# Plot the light values over time
plt.plot(timestamps, light_values)
plt.xlabel('Timestamp')
plt.ylabel('Light Value')
plt.show()
