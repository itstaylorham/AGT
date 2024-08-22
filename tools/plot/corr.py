import os
from datetime import datetime
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data from the static test JSON file
test = pd.read_json("./files/batches/t_parsley.json")

# Dynamic loading of the most recent control JSON file
read_files_dir = './files/read_files/'

# Find the most recent folder
latest_data = max(
    [f for f in os.listdir(read_files_dir) if os.path.isdir(os.path.join(read_files_dir, f))],
    key=lambda date_str: datetime.strptime(date_str, '%Y-%m-%d')
)

# Construct the path to the most recent JSON file
control_json_file_path = os.path.join(read_files_dir, latest_data, f'AGT-{latest_data}.json')

# Load the most recent control JSON file
control = pd.read_json(control_json_file_path)

# Combine the data from both DataFrames
df = pd.concat([test, control], ignore_index=True)

# Check the data types to understand what transformations are needed
print(df.dtypes)

# Convert the columns if they are lists or other non-float types
if isinstance(df['Moisture'].iloc[0], list):
    df['Moisture'] = df['Moisture'].apply(lambda x: x[0] if isinstance(x, list) else x)

if isinstance(df['Light'].iloc[0], list):
    df['Light'] = df['Light'].apply(lambda x: x[0] if isinstance(x, list) else x)

if isinstance(df['Temperature'].iloc[0], list):
    df['Temperature'] = df['Temperature'].apply(lambda x: x[0] if isinstance(x, list) else x)

if isinstance(df['Conductivity'].iloc[0], list):
    df['Conductivity'] = df['Conductivity'].apply(lambda x: x[0] if isinstance(x, list) else x)

# Convert to float (if not already)
df['Moisture'] = df['Moisture'].astype(float)
df['Light'] = df['Light'].astype(float)
df['Temperature'] = df['Temperature'].astype(float)
df['Conductivity'] = df['Conductivity'].astype(float)

# Calculate the Pearson correlation coefficient between light and temperature
correlation = df.corr(numeric_only=True)

# Create a heatmap to visualize the correlation
sns.heatmap(correlation, annot=True, cmap='YlGnBu')
plt.show()

print(correlation)

