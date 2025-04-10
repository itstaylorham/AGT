import csv
import json
import numpy as np
import time
from datetime import datetime, timedelta

print('-- batch builder --')

# Ask the user for how many days of data to generate
days = int(input("How many days of data should be generated? "))
assert days > 0, "Number of days must be greater than 0."

# Ask for the desired file name
file_name = input("Enter the name of the output CSV file (without extension): ")
file_name = f"./files/batches/{file_name}.csv"

# Define the time range
interval_duration = 10 * 60  # 10 minutes in seconds
past_hours = days * 24  # Convert days to hours

# Calculate the number of intervals
intervals = past_hours * 60 * 60 // interval_duration

# Get user input for the control parameter
control = float(input("Enter randomness value (1 - 10)"))
assert 1 <= control <= 10, "Control value must be between 1 and 10."

scale = (control - 1) / 9  # Scale the control value to a range of 0 to 1

print('')

# Input the baseline (midpoint), amplitude (half the range), and the period
print('STAGE 1: Build the sinusoidal components')
baseline_temp = float(input("Baseline Temperature: "))
amplitude_temp = float(input("Amplitude Temperature: "))
period_temp = float(input("Period Temperature: "))

baseline_moist = float(input("Baseline Moisture: "))
amplitude_moist = float(input("Amplitude Moisture: "))
period_moist = float(input("Period Moisture: "))

baseline_light = float(input("Baseline Light: "))
amplitude_light = float(input("Amplitude Light: "))
period_light = float(input("Period Light: "))

basline_cond = float(input("Baseline Conductivity: "))
amplitude_cond = float(input("Amplitude Conductivity: "))
period_cond = float(input("Period Conductivity: "))

# Build random values from the user-defined ranges
print('STAGE 2: Define ranges for components')
lowTemp = float(input("Lowest Temperature: "))
highTemp = float(input("Highest Temperature: "))
lowMoist = float(input("Lowest Moisture: "))
highMoist = float(input("Highest Moisture: "))
lowLight = float(input("Lowest Light: "))
highLight = float(input("Highest Light: "))
lowCond = float(input("Lowest Conductivity: "))
highCond = float(input("Highest Conductivity: "))

# Generate sinusoidal and random components
temp_sine = baseline_temp + amplitude_temp * np.sin(2 * np.pi * np.arange(intervals) / period_temp)
temp_rand = np.random.uniform(lowTemp, highTemp, size=intervals)

light_sine = baseline_light + amplitude_light * np.sin(2 * np.pi * np.arange(intervals) / period_light)
light_rand = np.random.uniform(lowLight, highLight, size=intervals)

moist_sine = baseline_moist + amplitude_moist * np.sin(2 * np.pi * np.arange(intervals) / period_moist)
moist_rand = np.random.uniform(lowMoist, highMoist, size=intervals)

cond_sine = basline_cond + amplitude_cond * np.sin(2 * np.pi * np.arange(intervals) / period_cond)
cond_rand = np.random.uniform(lowCond, highCond, size=intervals)

temp = scale * temp_sine + (1 - scale) * temp_rand
moisture = scale * moist_sine + (1 - scale) * moist_rand
light = scale * light_sine + (1 - scale) * light_rand
cond = scale * cond_sine + (1 - scale) * cond_rand

# Create a list to hold the data rows
data = []

# Get the current datetime and subtract the intervals
current_time = datetime.now()

# Generate rows with timestamp, MAC address, temperature, moisture, light, and conductivity
for i in range(intervals):
    timestamp = current_time - timedelta(seconds=i * interval_duration)
    # Format timestamp to "YYYY-MM-DD HH:MM:SS"
    formatted_timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')
    
    # Define a placeholder MAC address (XX:XX:XX:XX:XX:XX)
    mac_address = "c4:7c:8d:6d:26:c9"
    
    row = {
        "Timestamp": formatted_timestamp,
        "MAC": mac_address,
        "Temperature": round(temp[i], 2),
        "Moisture": round(moisture[i], 2),
        "Light": round(light[i], 2),
        "Conductivity": round(cond[i], 2)
    }
    data.append(row)

# Write the list of dictionaries to a CSV file
with open(file_name, "w", newline="") as csvfile:
    fieldnames = ["Timestamp", "MAC", "Temperature", "Moisture", "Light", "Conductivity"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for row in data:
        writer.writerow(row)

print('')
print(f"'{file_name}' created successfully!")
