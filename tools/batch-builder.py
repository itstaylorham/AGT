import csv
import json
import numpy as np
import time

print('-- batch builder --')

# Define the time range
interval_duration = 10 * 60  # 10 minutes in seconds
past_hours = 24

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

# Generate rows with timestamp, temperature, moisture, light, and conductivity
current_time = int(time.time())  # Current Unix timestamp
for i in range(intervals):
    timestamp = current_time - (i * interval_duration)
    row = {
        "Timestamp": timestamp,
        "Temperature": round(temp[i], 2),
        "Moisture": round(moisture[i], 2),
        "Light": round(light[i], 2),
        "Conductivity": round(cond[i], 2)
    }
    data.append(row)

# Write the list of dictionaries to a CSV file
with open("./files/batches/new-batch.csv", "w", newline="") as csvfile:
    fieldnames = ["Timestamp", "Temperature", "Moisture", "Light", "Conductivity"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for row in data:
        writer.writerow(row)

print('')
print("'new-batch.csv' created successfully!")
