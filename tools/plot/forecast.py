import os
import json
import matplotlib.pyplot as plt
import statsmodels.api as sm
from datetime import datetime, timedelta

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

# Define the number of steps to forecast
n_steps = 5

# Fit the ARIMA model to the temperature data
model = sm.tsa.ARIMA(temperatures, order=(1, 1, 1))
model_fit = model.fit()
predictions_temperatures = model_fit.predict(start=len(temperatures), end=len(temperatures)+n_steps-1)

# Fit the ARIMA model to the moisture data
model = sm.tsa.ARIMA(moistures, order=(1, 1, 1))
model_fit = model.fit()
predictions_moistures = model_fit.predict(start=len(moistures), end=len(moistures)+n_steps-1)

# Fit the ARIMA model to the light data
model = sm.tsa.ARIMA(lights, order=(1, 1, 1))
model_fit = model.fit()
predictions_lights = model_fit.predict(start=len(lights), end=len(lights)+n_steps-1)
print(predictions_lights)

# Fit the ARIMA model to the conductivity data
model = sm.tsa.ARIMA(conductivities, order=(1, 1, 1))
model_fit = model.fit()
predictions_conductivities = model_fit.predict(start=len(conductivities), end=len(conductivities)+n_steps-1)

# Assuming timestamps are in seconds
# Determine the interval between each timestamp
interval = timestamps[-1] - timestamps[-2]

# Generate new timestamps based on this interval for n_steps into the future
new_timestamps = [timestamps[-1] + interval * i for i in range(1, n_steps+1)]

# append new timestamps to existing timestamps
timestamps += new_timestamps

print(predictions_temperatures)
print(predictions_lights)
print(predictions_moistures)
print(predictions_conductivities)

# Append the predictions to the existing data
temperatures += predictions_temperatures.tolist()
moistures += predictions_moistures.tolist()
lights += predictions_lights.tolist()
conductivities += predictions_conductivities.tolist()

predictions = {
    "Timestamp": timestamps,
    "Temperature": temperatures,
    "Moisture": moistures,
    "Light": lights,
    "Conductivity": conductivities
}

# Create a copy of the predictions for saving to predictions.json
predictions_raw = predictions.copy()

# Remove the 'timestamp' and 'health_score' key-value pair from the dictionary
predictions_raw.pop('timestamp', None)
predictions_raw.pop('health_score', None)

with open('files/predict/predictions.json', 'w') as f:
    json.dump(predictions_raw, f)

# Save data

# Get current date and time and format them as strings
current_date = datetime.now().strftime("%Y-%m-%d")
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Define the folder for today's data
daily_folder = os.path.join("files/predict", current_date)

# Create the directory for the current day if it doesn't already exist
if not os.path.exists(daily_folder):
    os.makedirs(daily_folder)

# Define the daily JSON file path
daily_json_file = os.path.join(daily_folder, f'AGT-PRED-{current_date}.json')

# Load existing data if the file exists, otherwise create an empty list
if os.path.exists(daily_json_file):
    with open(daily_json_file, 'r') as f:
        daily_data = json.load(f)
else:
    daily_data = []

# Append new records to the existing data
daily_data.append(predictions)

# Save the updated data to the daily JSON file
with open(daily_json_file, 'w') as f:
    json.dump(daily_data, f)
