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
        temp_data['Timestamp'] = pd.to_datetime(temp_data['Timestamp'])
        data_list.append(temp_data)
    
    # Append all data into a single DataFrame
    data = pd.concat(data_list, ignore_index=True)
    return data

# Timer function to count down and close plots
def countdown_timer(seconds, event):
    for i in tqdm(range(seconds, 0, -1), desc="Time Remaining", leave=True):
        time.sleep(1)  # Sleep for 1 second
    event.set()  # Set the event to signal that time is up

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
    plt.show(block=False)  # Display each figure as it's created

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
        plt.show(block=False)  # Show the plot immediately

    return all_figures

def main():
    # Load all files from the base folder and subfolders
    data = load_all_files()

    if data is not None:
        # Select relevant columns for correlation and clustering
        features = data[['Temperature', 'Moisture', 'Light', 'Conductivity']]

        # Create and display all plots
        print("\nGenerating visualizations...")
        figures = create_and_display_plots(data, features)

        print("\nStarting 30-second display timer...")
        # Create a threading event
        event = threading.Event()
        # Start the timer in a separate thread
        timer_thread = threading.Thread(target=countdown_timer, args=(30, event))
        timer_thread.start()
        
        # Keep GUI active and wait for the event to be set (after the timer finishes)
        while not event.is_set():
            plt.pause(0.5)  # Keep GUI responsive and allow interaction
        
        # Ensure all windows are closed after timer ends
        print("\nClosing all plots...")
        for fig in figures:
            plt.close(fig)

        # Wait for the timer thread to complete
        timer_thread.join()

    else:
        print("No data was found for analysis.")

if __name__ == "__main__":
    main()
