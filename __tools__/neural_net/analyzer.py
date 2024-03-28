import os
import json
import pandas as pd

def filter_data_by_timestamp(directory, start_date, end_date):
    # Convert the input dates to Unix timestamps
    start_timestamp = pd.to_datetime(start_date).timestamp()
    end_timestamp = pd.to_datetime(end_date).timestamp()
    
    filtered_data = []
    actual_start_timestamp = float('inf')
    actual_end_timestamp = float('-inf')

    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r') as f:
                data = json.load(f)

            for record in data:
                if 'Timestamp' in record:
                    record_timestamp = record['Timestamp'][0] / 1000000000 # Convert from ns to s

                    if start_timestamp <= record_timestamp <= end_timestamp:
                        filtered_data.append(record)
                        actual_start_timestamp = min(actual_start_timestamp, record_timestamp)
                        actual_end_timestamp = max(actual_end_timestamp, record_timestamp)

    actual_start_date = pd.to_datetime(actual_start_timestamp, unit='s')
    actual_end_date = pd.to_datetime(actual_end_timestamp, unit='s')

    return filtered_data, (start_timestamp, end_timestamp), (actual_start_date, actual_end_date)

filtered_data, requested_range, actual_range = filter_data_by_timestamp('/home/jeremy/Documents/Agrotech/sesh.json', '2023-05-01', '2023-05-20')

print(f"Requested range (Unix time): {requested_range}")
print(f"Actual range found in data: {actual_range}")

