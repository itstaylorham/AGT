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

# Timer function to count down and close plots
def countdown_timer(seconds):
    for i in tqdm(range(seconds, 0, -1), desc="Time Remaining", leave=False):
        time.sleep(1)
    # Force close all windows
    plt.close('all')

def create_and_display_plots(data, features):
    # Initialize KMeans model first since it's needed for all plots
    kmeans = KMeans(n_clusters=3)
    data['Cluster'] = kmeans.fit_predict(features)
    
    # List to store all figures for proper cleanup
    all_figures = []

    # 1. Create pair plot first
    print("Creating pair plot...")
    pair_plot = sns.pairplot(data, 
                            vars=['Temperature', 'Moisture', 'Light', 'Conductivity'],
                            hue='Cluster', 
                            palette='viridis')
    pair_plot.fig.canvas.manager.set_window_title('Feature Correlations Overview')
    all_figures.append(pair_plot.fig)
    plt.show(block=False)

    # 2. Create correlation matrix
    print("Creating correlation matrix...")
    correlation_matrix = features.corr()
    fig_corr = plt.figure(figsize=(6, 4))
    all_figures.append(fig_corr)
    fig_corr.canvas.manager.set_window_title('Correlation Analysis')
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm")
    plt.title("Correlation Matrix")
    plt.xticks(rotation=45)
    plt.show(block=False)

    # 3. Create individual clustering plots
    feature_combinations = [
        ('Temperature', 'Moisture'),
        ('Temperature', 'Light'),
        ('Temperature', 'Conductivity'),
        ('Moisture', 'Light'),
        ('Moisture', 'Conductivity'),
        ('Light', 'Conductivity')
    ]

    print("Creating clustering plots...")
    for feature_x, feature_y in feature_combinations:
        fig_cluster = plt.figure(figsize=(6, 4))
        all_figures.append(fig_cluster)
        fig_cluster.canvas.manager.set_window_title(f'{feature_x}-{feature_y} Clustering')
        plt.scatter(data[feature_x], data[feature_y], c=data['Cluster'], cmap='viridis')
        plt.title(f"K-Means Clustering: {feature_x} vs {feature_y}")
        plt.xlabel(feature_x)
        plt.ylabel(feature_y)
        plt.show(block=False)

    return all_figures

def main():
    # Get the date range from the user
    start_date, end_date = get_date_range()

    # Load all files from the base folder and subfolders
    data = load_all_files()

    if data is not None:
        # Filter data based on the provided date range
        data = filter_data_by_date(data, start_date, end_date)

        # Select relevant columns for correlation and clustering
        features = data[['Temperature', 'Moisture', 'Light', 'Conductivity']]

        # Create and display all plots
        print("\nGenerating visualizations...")
        figures = create_and_display_plots(data, features)

        print("\nStarting 30-second display timer...")
        # Start the timer in a separate thread
        timer_thread = threading.Thread(target=countdown_timer, args=(30,))
        timer_thread.start()
        
        # Keep the main thread alive until the timer finishes
        plt.pause(30)  # This keeps the plots visible for 30 seconds
        
        # Wait for the timer thread to complete
        timer_thread.join()
        
        # Ensure all windows are closed
        for fig in figures:
            plt.close(fig)
    else:
        print("No data was found for analysis.")

if __name__ == "__main__":
    main()