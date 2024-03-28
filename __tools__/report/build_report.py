import os
import pandas as pd
import datetime
from sqlalchemy import create_engine
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.chart import LineChart, Reference

# Replace with your database connection details
db_url = "mysql+mysqlconnector://jeremy:Starfish!2345@localhost/AGT_DB"

sql_query = "SELECT * FROM AGT_DB.SENSOR_READINGS WHERE Timestamp LIKE '2023%'"

# Read data from AGT_DB.SENSOR_READINGS to pandas dataframe
df = pd.read_sql(sql_query, create_engine(db_url))

# Convert the timestamp column to string format
df['Timestamp'] = pd.to_datetime(df['Timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S')

# Set Timestamp column as the index
df.set_index('Timestamp', inplace=True)

# Explicitly convert the index to DatetimeIndex
df.index = pd.to_datetime(df.index)

# Remove the 'MAC' column before resampling and aggregating
df_without_mac = df.drop(columns=['MAC'])

# Calculate the differences
df_without_mac['Temperature_Diff'] = df_without_mac['Temperature'] - df_without_mac['Temperature'].shift(1)
df_without_mac['Moisture_Diff'] = df_without_mac['Moisture'] - df_without_mac['Moisture'].shift(1)
df_without_mac['Light_Diff'] = df_without_mac['Light'] - df_without_mac['Light'].shift(1)
df_without_mac['Conductivity_Diff'] = df_without_mac['Conductivity'] - df_without_mac['Conductivity'].shift(1)

# Save data to reports folder
dir_path = "/home/jeremy/Documents/AGT/__files__/reports"

if not os.path.exists(dir_path):
    os.makedirs(dir_path)

# Create a new workbook
wb = Workbook()

# Select the active sheet (or create a new one)
sheet = wb.active
sheet.title = "Summary"

# Set the column headers
column_headers = ['Timestamp', 'Temperature', 'Moisture', 'Light', 'Conductivity',
                  'Δ Temperature', 'Δ Moisture', 'Δ Light', 'Δ Conductivity']
sheet.append(column_headers)

# Write the DataFrame data to the sheet, converting timestamp to string
for row in dataframe_to_rows(df_without_mac.reset_index(), index=False, header=False):
    # Convert the timestamp to string format before appending
    row = [str(cell) if isinstance(cell, pd.Timestamp) else cell for cell in row]
    sheet.append(row)


# Write the DataFrame data to the sheet
for row in dataframe_to_rows(df_without_mac.reset_index(), index=False, header=False):
    sheet.append(row)

# Historical summary
pivot_table = df_without_mac.resample('M').mean()

# Add historical summary sheet
historical_sheet = wb.create_sheet(title="Historical Summary")

# Drop the existing 'Timestamp' column if it exists
if 'Timestamp' in pivot_table.columns:
    pivot_table = pivot_table.drop(columns=['Timestamp'])

# Convert the Timestamp column to string format in the pivot_table
pivot_table.index = pivot_table.index.strftime('%Y-%m-%d %H:%M:%S')

# Reset the index in the pivot_table
pivot_table.reset_index(inplace=True)

# Write pivot table data to the Historical Summary sheet
for row in dataframe_to_rows(pivot_table, index=False, header=True):
    historical_sheet.append(row)

# Add graphs for each sensor reading
for col in ['Temperature', 'Moisture', 'Light', 'Conductivity']:
    chart = LineChart()
    chart.title = f'Historical {col} Trends'
    chart.x_axis.title = 'Timestamp'
    chart.y_axis.title = 'Value'

    data = Reference(historical_sheet, min_col=2, min_row=2, max_row=pivot_table.shape[0] + 1, max_col=2)
    categories = Reference(historical_sheet, min_col=1, min_row=2, max_row=pivot_table.shape[0] + 1)
    values = Reference(historical_sheet, min_col=pivot_table.columns.get_loc(col) + 2, min_row=1, max_row=pivot_table.shape[0] + 1)
    chart.add_data(values, titles_from_data=True)
    chart.set_categories(categories)
    historical_sheet.add_chart(chart, f"E{(pivot_table.shape[0] // 10) * 10 + 4}")

# Get the current timestamp
current_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

# Create the filename
file_name = f"AGT_REPORT_{current_timestamp}.xlsx"

# Save the workbook to the directory
wb.save(os.path.join(dir_path, file_name))

# Check if the workbook is saved in the directory
if os.path.isfile(os.path.join(dir_path, file_name)):
    print(f"Workbook saved successfully in {dir_path}")
else:
    print(f"Workbook not saved in {dir_path}")
