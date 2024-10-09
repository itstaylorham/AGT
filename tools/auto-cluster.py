import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from datetime import datetime
import glob
import os

# Function to prompt the user for date or date range
def get_date_range():
    start_date_str = input("Enter start date (YYYY-MM-DD) or press Enter for no start date: ")
    end_date_str = input("Enter end date (YYYY-MM-DD) or press Enter for no end date: ")

    if start_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    else:
        start_date = None

    if end_date_str:
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    else:
        end_date = None

    return start_date, end_date

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
        temp_data['Timestamp'] = pd.to_datetime(temp_data['Timestamp'])
        data_list.append(temp_data)
    
    # Append all data into a single DataFrame
    data = pd.concat(data_list, ignore_index=True)
    return data

# Function to filter data by date range if provided
def filter_data_by_date(data, start_date, end_date):
    if start_date:
        data = data[data['Timestamp'] >= start_date]
    if end_date:
        data = data[data['Timestamp'] <= end_date]
    return data

# Get the date range from the user
start_date, end_date = get_date_range()

# Load all files from the base folder and subfolders
data = load_all_files()

if data is not None:
    # Filter data based on the provided date range
    data = filter_data_by_date(data, start_date, end_date)

    # Select relevant columns for correlation and clustering (Temperature, Moisture, Light, Conductivity)
    features = data[['Temperature', 'Moisture', 'Light', 'Conductivity']]

    # Step 1: Correlation Analysis
    # Calculate the correlation matrix
    correlation_matrix = features.corr()

    # Plot the correlation matrix in a separate window
    plt.figure(figsize=(6, 4))
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm")
    plt.title("Correlation Matrix")

    # Step 2: Clustering with K-Means
    # Initialize KMeans model (using 3 clusters as an example)
    kmeans = KMeans(n_clusters=3)

    # Fit the model and predict the cluster for each data point
    data['Cluster'] = kmeans.fit_predict(features)

    # Plot clustering results in a separate window
    plt.figure(figsize=(6, 4))
    plt.scatter(data['Temperature'], data['Light'], c=data['Cluster'], cmap='viridis')

    # Add total sample count to the plot
    total_samples = len(data)
    plt.title(f"K-Means Clustering\nTotal Samples: {total_samples}")
    plt.xlabel("Temperature")
    plt.ylabel("Light")

    # Display both figures (correlation matrix and clustering)
    plt.show()

else:
    print("No data was found for analysis.")
