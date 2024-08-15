import matplotlib.pyplot as plt

# Provided data
data = [
    {"Timestamp": 1675401126597, "Temperature": 22.5, "Moisture": 19.5, "Light": 6000, "Conductivity": 2.0},
    {"Timestamp": 1675401267091, "Temperature": 23.1, "Moisture": 18.8, "Light": 5800, "Conductivity": 1.9},
    {"Timestamp": 1675401361203, "Temperature": 22.8, "Moisture": 20.2, "Light": 5500, "Conductivity": 2.1},
    {"Timestamp": 1675401423651, "Temperature": 23.1, "Moisture": 19.0, "Light": 5600, "Conductivity": 2.2},
    {"Timestamp": 1675401536289, "Temperature": 23.8, "Moisture": 20.5, "Light": 5200, "Conductivity": 2.3},
]

# Generate some example predicted values
predicted_values = [
    {"Temperature": 23.3, "Moisture": 19.8, "Light": 5400, "Conductivity": 2.1},
]

# Extract the data from the dictionaries
timestamps = [d["Timestamp"] for d in data]
actual_temp = [d["Temperature"] for d in data]
actual_moisture = [d["Moisture"] for d in data]
actual_light = [d["Light"] for d in data]
actual_conductivity = [d["Conductivity"] for d in data]

predicted_temp = [d["Temperature"] for d in predicted_values]
predicted_moisture = [d["Moisture"] for d in predicted_values]
predicted_light = [d["Light"] for d in predicted_values]
predicted_conductivity = [d["Conductivity"] for d in predicted_values]

# Plot the actual and predicted values
plt.plot(timestamps, actual_temp, label="Actual Temperature")
plt.plot(timestamps[-1:], predicted_temp, 'o', label="Predicted Temperature")

plt.plot(timestamps, actual_moisture, label="Actual Moisture")
plt.plot(timestamps[-1:], predicted_moisture, 'o', label="Predicted Moisture")

plt.plot(timestamps, actual_light, label="Actual Light")
plt.plot(timestamps[-1:], predicted_light, 'o', label="Predicted Light")

plt.plot(timestamps, actual_conductivity, label="Actual Conductivity")
plt.plot(timestamps[-1:], predicted_conductivity, 'o', label="Predicted Conductivity")

# Configure the plot appearance
plt.xlabel("Timestamp")
plt.ylabel("Values")
plt.title("Plant Growth Patterns")
plt.legend(loc="best")
plt.grid(True)

# Show the plot
plt.show()
