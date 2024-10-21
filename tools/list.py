import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from datetime import datetime
import glob
import os
import time
import threading
from tqdm import tqdm

# Function to load all .json files from the main folder and subfolders
def load_all_files():
    base_dir = "files/read_files/"
    
    # Collect all JSON files from the base directory and all subdirectories
    files = glob.glob(os.path.join(base_dir, '**', '*.json'), recursive=True)
    
    if not files:
        print("No JSON files found in the specified directories.")
        return None

    data_list = []
    print("Files being analyzed:")
    for file in files:
        print(f" - {file}")  # Print the file name
        temp_data = pd.read_json(file)

        # Convert 'Timestamp' column to datetime if it isn't already
        temp_data['Timestamp'] = pd.to_datetime(temp_data['Timestamp'])

        # Replace the 'Timestamp' column with the desired format: 'YYYY:MM:DD:hh:mm:ss:SSS'
        temp_data['Timestamp'] = temp_data['Timestamp'].dt.strftime('%Y:%m:%d:%H:%M:%S')[:-3]
        
        data_list.append(temp_data)
    
    # Append all data into a single DataFrame
    data = pd.concat(data_list, ignore_index=True)
    return data

# Function to display data 50 rows at a time
def display_data_in_chunks(data):
    chunk_size = 50
    num_rows = len(data)
    start = 0
    
    # Change pandas print settings to show all rows in each chunk
    pd.set_option('display.max_rows', chunk_size)
    
    # While loop to keep displaying chunks of data
    while start < num_rows:
        end = min(start + chunk_size, num_rows)  # Get the next 50 rows or whatever is left
        print(data[start:end])  # Display the chunk of data

        start += chunk_size  # Move to the next chunk

        # Wait for user input before continuing
        user_input = input("\nPress Enter to continue, or type 'Ctrl + F' to stop: ")
        if user_input.lower() == 'ctrl + f':
            print("Exiting...")
            break

def main():
    # Load all files from the base folder and subfolders
    data = load_all_files()

    if data is not None:
        print("\nData from all JSON files with formatted timestamps:")
        display_data_in_chunks(data)
    else:
        print("No data was found for analysis.")

if __name__ == "__main__":
    main()
