import json
import torch
import numpy as np
import argparse
from datetime import datetime, timedelta
import os
from sklearn.preprocessing import StandardScaler

# Add argument parser for command line input
parser = argparse.ArgumentParser()
parser.add_argument('--from_main', action='store_true', help='Indicates if the script is called from main.py')
parser.add_argument('--progress_bar', action='store_true', help='Show training progress as percentage')
args = parser.parse_args()

# Load spider plant ideal dataset
with open('/home/jeremy/Documents/AGT/files/batches/spiderplant.json', 'r') as f:
    ideal_data = json.load(f)

# Extract features and normalize
features = []
targets = []

for entry in ideal_data:
    features.append([
        entry["Light"], entry["Moisture"], entry["Conductivity"],
        entry["Temperature"]
    ])
    targets.append([
        entry["Temperature"], entry["Moisture"], entry["Light"],
        entry["Conductivity"]
    ])

scaler = StandardScaler()
features = scaler.fit_transform(features)

# Set the random seed for PyTorch
torch.manual_seed(20)

# Set the random seed for NumPy
np.random.seed(20)

X_train = torch.tensor(features, dtype=torch.float32)
y_train = torch.tensor(targets, dtype=torch.float32)

current_day = datetime.now().day

num_days_loaded = 0
num_days_missing = 0

# Initialize some things
test_data = []
num_days_loaded = 0
num_days_missing = 0

# Get today's date
today = datetime.now()

# Load the past 30 days of test data
for i in range(1, 15):
    # Calculate the date for each file
    test_date = today - timedelta(days=i)
    
    # Format the date as a string in the desired format
    # date_string = test_date.strftime('%Y-%m-%d')

    date_string = '2024-02-29'

    filename = f'files/read_files/{date_string}/AGT-{date_string}.json'
    
    if os.path.isfile(filename):
        with open(filename, 'r') as f:
            day_data = json.load(f)
            test_data.extend(day_data)
            num_days_loaded += 1
    else:
        num_days_missing += 1

print(f"Loaded {num_days_loaded} days of data out of {i} days expected.")
if num_days_missing > 0:
    print(f"Data not found for {num_days_missing} day(s).")
    
test_features = []
test_targets = []

for entry in test_data:
    test_features.append([
        entry["Light"], entry["Moisture"], entry["Conductivity"],
        entry["Temperature"]
    ])
    test_targets.append([
        entry["Temperature"], entry["Moisture"], entry["Light"],
        entry["Conductivity"]
    ])

test_features = scaler.transform(test_features)  # use the same scaler to ensure the same scale is used

X_test = torch.tensor(test_features, dtype=torch.float32)
y_test = torch.tensor(test_targets, dtype=torch.float32)
