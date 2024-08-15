import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data from two JSON files
test = pd.read_json("./files/batches/t_parsley.json")
control = pd.read_json("./files/read_files/2024-07-17/AGT-2024-07-17.json")

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

