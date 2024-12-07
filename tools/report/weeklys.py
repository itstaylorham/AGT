import nbformat as nbf
import os
import datetime

# Create a new notebook
nb = nbf.v4.new_notebook()

# Cell 1: Import statements
imports = '''
import pandas as pd
import datetime
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns
'''

# Cell 2: Database connection and data loading
db_connection = '''
# Replace with your database connection details
db_url = "mysql+mysqlconnector://jeremy:Starfish!2345@localhost/AGT_DB"

sql_query = "SELECT * FROM AGT_DB.AGT_2024_SENSOR_READINGS UNION SELECT * FROM AGT_DB.AGT_2023_SENSOR_READINGS"

# Read data from AGT_DB.SENSOR_READINGS to pandas dataframe
df = pd.read_sql(sql_query, create_engine(db_url))

# Convert the TIMECODE column to datetime
df['TIMECODE'] = pd.to_datetime(df['TIMECODE'])
df.set_index('TIMECODE', inplace=True)

# Remove the 'MAC' column
df_without_mac = df.drop(columns=['MAC'])
'''

# Cell 3: Calculate differences
calc_differences = '''
# Calculate the differences
df_without_mac['Temperature_Diff'] = df_without_mac['Temperature'] - df_without_mac['Temperature'].shift(1)
df_without_mac['Moisture_Diff'] = df_without_mac['Moisture'] - df_without_mac['Moisture'].shift(1)
df_without_mac['Light_Diff'] = df_without_mac['Light'] - df_without_mac['Light'].shift(1)
df_without_mac['Conductivity_Diff'] = df_without_mac['Conductivity'] - df_without_mac['Conductivity'].shift(1)

# Display the first few rows of the data
print("Raw Data Sample:")
display(df_without_mac.head())
'''

# Cell 4: Historical summary
historical_summary = '''
# Create monthly historical summary
pivot_table = df_without_mac.resample('M').mean()

print("Monthly Historical Summary:")
display(pivot_table.head())
'''

# Cell 5: Visualization functions
visualization_code = '''
def plot_sensor_data(data, column):
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=data, y=column)
    plt.title(f'Historical {column} Trends')
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    
def plot_sensor_differences(data, column):
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=data, y=f'{column}_Diff')
    plt.title(f'Historical {column} Changes')
    plt.xlabel('Time')
    plt.ylabel('Change in Value')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
'''

# Cell 6: Generate visualizations
generate_plots = '''
# Plot historical trends for each sensor
for column in ['Temperature', 'Moisture', 'Light', 'Conductivity']:
    plot_sensor_data(pivot_table, column)
    plot_sensor_differences(pivot_table, column)
'''

# Add markdown cells and code cells to the notebook
nb.cells.extend([
    nbf.v4.new_markdown_cell('# AGT Sensor Data Analysis Report\n'
                            f'Generated on: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'),
    nbf.v4.new_markdown_cell('## Data Import and Preprocessing'),
    nbf.v4.new_code_cell(imports),
    nbf.v4.new_code_cell(db_connection),
    nbf.v4.new_markdown_cell('## Data Analysis'),
    nbf.v4.new_code_cell(calc_differences),
    nbf.v4.new_markdown_cell('## Historical Summary'),
    nbf.v4.new_code_cell(historical_summary),
    nbf.v4.new_markdown_cell('## Visualizations'),
    nbf.v4.new_code_cell(visualization_code),
    nbf.v4.new_code_cell(generate_plots)
])

# Create the directory if it doesn't exist
dir_path = "/home/jeremy/Documents/AGT/files/reports"
if not os.path.exists(dir_path):
    os.makedirs(dir_path)

# Get the current timestamp
current_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

# Save the notebook
notebook_name = f"AGT_REPORT_{current_timestamp}.ipynb"
notebook_path = os.path.join(dir_path, notebook_name)

with open(notebook_path, 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print(f"Notebook saved successfully as {notebook_path}")