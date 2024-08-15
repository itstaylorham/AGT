# model.py
# Necessary imports
import os
import torch
import json
import torch.nn as nn
import torch.optim as optim
import sys
from sklearn.metrics import r2_score
from nn import SoilHealthPredictor    # necessary if nn is a different python file
from data_prep import X_train, y_train, X_test, y_test, scaler, args  # import the prepared data and the scaler
from arima_model import fit_arima_model, calculate_residuals
from datetime import datetime
import numpy as np

model = SoilHealthPredictor()

criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)

# Training parameters
epochs = 100
batch_size = 32

# Load time series data


# Training loop
for epoch in range(epochs):
    for i in range(0, len(X_train), batch_size):
        # Get mini-batch
        inputs = X_train[i:i + batch_size]
        labels = y_train[i:i + batch_size]

        # Forward pass
        outputs = model(inputs)
        loss = criterion(outputs, labels)

        # Backward pass and optimization
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    # Calculate training and test losses
    with torch.no_grad():
        train_loss = criterion(model(X_train), y_train)
        test_loss = criterion(model(X_test), y_test)
    
    if not args.from_main:
        print(f'Epoch [{epoch+1}/{epochs}], Train Loss: {train_loss:.4f}, Test Loss: {test_loss:.4f}')
    else:
        progress = (epoch + 1) / epochs * 100
        sys.stdout.write(f'\rTraining Progress: {progress:.2f}%')
        sys.stdout.flush()

    if args.progress_bar:
        progress = (epoch + 1) / epochs * 100
        sys.stdout.write(f'\rTraining Progress: {progress:.2f}%')
        sys.stdout.flush()
else:
    print(f'Epoch [{epoch+1}/{epochs}], Train Loss: {train_loss:.4f}, Test Loss: {test_loss:.4f}')

with torch.no_grad():
    test_predictions = model(X_test)
    actual_temperatures = y_test[:, 0].numpy()
    predicted_temperatures = test_predictions[:, 0].numpy()

temperature_r2_score = r2_score(actual_temperatures, predicted_temperatures)

# Calculate R2 score for Moisture, Light, and Conductivity
actual_moisture = y_test[:, 1].numpy()
predicted_moisture = test_predictions[:, 1].numpy()
moisture_r2_score = r2_score(actual_moisture, predicted_moisture)

actual_light = y_test[:, 2].numpy()
predicted_light = test_predictions[:, 2].numpy()
light_r2_score = r2_score(actual_light, predicted_light)

actual_conductivity = y_test[:, 3].numpy()
predicted_conductivity = test_predictions[:, 3].numpy()
conductivity_r2_score = r2_score(actual_conductivity, predicted_conductivity)

print('')
print('Evaluation Metrics:')
print(f'Temperature R2 Score: {temperature_r2_score:.4f}')
print(f'Moisture R2 Score: {moisture_r2_score:.4f}')
print(f'Light R2 Score: {light_r2_score:.4f}')
print(f'Conductivity R2 Score: {conductivity_r2_score:.4f}')
print('/ / / / / / / / / / / /')
# Save the trained model
torch.save(model.state_dict(), 'trained_model.pth')
print('Model saved successfully at "trained_model.pth" on ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
# Load the saved model
loaded_model = SoilHealthPredictor()
loaded_model.load_state_dict(torch.load('trained_model.pth'))
loaded_model.eval()

# Save for visualization
np.save('y_test.npy', y_test.numpy())
np.save('test_predictions.npy', test_predictions.numpy())
np.save('y_train.npy', y_train.numpy())
np.save('X_train.npy', X_train.numpy())
torch.save(model.state_dict(), 'trained_model.pth')

health_score = 0
 
# Get current date and time and format them as strings
current_date = datetime.now().strftime("%Y-%m-%d")
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Define the data
r2_scores = {
    "timestamp": current_time,  # added timestamp directly to the dictionary
    "temperature_r2": temperature_r2_score,
    "moisture_r2": moisture_r2_score,
    "light_r2": light_r2_score,
    "conductivity_r2": conductivity_r2_score,
}

# Create a copy of the r2_scores for saving to r2_scores.json
r2_scores_raw = r2_scores.copy()

# Remove the 'timestamp' and 'health_score' key-value pair from the dictionary
r2_scores_raw.pop('timestamp', None)
r2_scores_raw.pop('health_score', None)

with open('/home/jeremy/Documents/AGT/files/metrics/r2_scores.json', 'w') as f:
    json.dump(r2_scores_raw, f)

# Calculate the health score
r2_scores_keys = list(r2_scores.keys())
health_score = 0  # initialize this to prevent an error in case it's not defined earlier
for key in r2_scores_keys:
    if key != 'timestamp':  # Skip the timestamp field
        r2 = max(r2_scores[key], 0)  # Ensure the score is not negative
        health_score += r2 * 100  # Scale to 0-100
health_score /= len(r2_scores_keys) - 1  # Subtract 1 from the denominator because we're not including the timestamp field

print(f'\nAccruacy: {health_score:.2f}\n')

r2_scores['timestamp'] = current_time
r2_scores['health_score'] = health_score

# Define the folder for today's data
daily_folder = os.path.join("/home/jeremy/Documents/AGT/files/metrics", current_date)

# Create the directory for the current day if it doesn't already exist
if not os.path.exists(daily_folder):
    os.makedirs(daily_folder)

# Define the daily JSON file path
daily_json_file = os.path.join(daily_folder, f'AGT-STAT-{current_date}.json')

# Load existing data if the file exists, otherwise create an empty list
if os.path.exists(daily_json_file):
    with open(daily_json_file, 'r') as f:
        daily_data = json.load(f)
else:
    daily_data = []

# Append new records to the existing data
daily_data.append(r2_scores)

# Save the updated data to the daily JSON file
with open(daily_json_file, 'w') as f:
    json.dump(daily_data, f)

exit(0)

