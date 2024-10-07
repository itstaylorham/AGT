import os
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import json
import sys
from datetime import datetime

def load_json_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: The file {file_path} is not a valid JSON.")
        sys.exit(1)

def kmeans_clustering_from_json(json_data, n_clusters=3):
    df = pd.DataFrame(json_data)
    X = df[['Temperature', 'Moisture', 'Light', 'Conductivity']]
    
    kmeans = KMeans(n_clusters=n_clusters)
    df['Cluster'] = kmeans.fit_predict(X)
    
    output_file = 'clustered_data.xlsx'
    df.to_excel(output_file, index=False)
    print(f"Clustered data saved to {output_file}")
    
    # Interpretation guide
    print("""
    Interpretation Guide:
    ---------------------
    1. Light vs Temperature: 
       ...
    2. Moisture vs Light:
       ...
    3. Temperature vs Moisture:
       ...
    """)

    fig, axs = plt.subplots(1, 3, figsize=(18, 5))
    axs[0].scatter(df['Light'], df['Temperature'], c=df['Cluster'], cmap='viridis')
    axs[0].set_title('Light vs Temperature')
    axs[0].set_xlabel('Light')
    axs[0].set_ylabel('Temperature')

    axs[1].scatter(df['Moisture'], df['Light'], c=df['Cluster'], cmap='viridis')
    axs[1].set_title('Moisture vs Light')
    axs[1].set_xlabel('Moisture')
    axs[1].set_ylabel('Light')

    axs[2].scatter(df['Temperature'], df['Moisture'], c=df['Cluster'], cmap='viridis')
    axs[2].set_title('Temperature vs Moisture')
    axs[2].set_xlabel('Temperature')
    axs[2].set_ylabel('Moisture')

    plt.tight_layout()
    plt.show()

def main(file_path):
    json_data = load_json_from_file(file_path)
    clustered_df = kmeans_clustering_from_json(json_data, n_clusters=3)

if __name__ == "__main__":
    # Check if the script is being run as a subprocess
    if len(sys.argv) > 1:
        # Assume the first argument is the file path
        file_path = sys.argv[1]
    else:
        # Use today's date as default
        today = datetime.now().strftime('%Y-%m-%d')
        default_path = os.path.join('files', 'read_files', today, f'AGT-{today}.json')
        
        if os.path.exists(default_path):
            file_path = default_path
        else:
            user_date = input("Enter the date of the file you want to analyze (YYYY-MM-DD): ")
            file_path = os.path.join('files', 'read_files', user_date, f'AGT-{user_date}.json')

    main(file_path)
