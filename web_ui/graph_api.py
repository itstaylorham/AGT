import json
import matplotlib.pyplot as plt
import os
from datetime import datetime
import time

# Generate a graph of the sensor data and save it as an image file.

def image_graph():
    # Load the JSON data from the file
    with open('/home/jeremy/Documents/AGT/sesh.json') as f:
        data = json.load(f)

    # Convert timestamp to integer if necessary and filter the data for the last 12 hours
    current_time = time.time() * 1e9  # convert current time to nanoseconds
    twelve_hours_in_nanoseconds = 48 * 60 * 60 * 1e9
    filtered_data = [item for item in data if current_time - item['Timestamp'][0] <= twelve_hours_in_nanoseconds]

    # Extract data from the JSON into separate lists
    timestamps = [i['Timestamp'][0] for i in filtered_data]
    temperatures = [i['Temperature'][0] for i in filtered_data]
    moistures = [i['Moisture'][0] for i in filtered_data]
    lights = [i['Light'][0] for i in filtered_data] 
    conductivities = [i['Conductivity'][0] for i in filtered_data]

    # Create subplots for each sensor value
    fig, axs = plt.subplots(2, 2)

    # Plot the temperature data
    axs[0, 0].plot(timestamps, temperatures, label='Temperature', color='#FF6347', linewidth=0.8)
    axs[0, 0].legend()

    # Plot the moisture data
    axs[0, 1].plot(timestamps, moistures, label='Moisture', color='#00BFFF', linewidth=0.95)
    axs[0, 1].legend()

    # Plot the light data
    axs[1, 0].plot(timestamps, lights, label='Light', color='#FFD700', linewidth=0.95)
    axs[1, 0].legend()

    # Plot the conductivity data
    axs[1, 1].plot(timestamps, conductivities, label='Conductivity', color='#3CB371', linewidth=0.95)
    axs[1, 1].legend()

    # Save the graphs as a single image file
    img_dir = 'image_graphs'
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)

    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    img_filename = f"sensors_{timestamp}.png"
    img_path = os.path.join(img_dir, img_filename)
    fig.savefig(img_path)

    # Print the image URL
    image_url = {'sensors_url': f'/image_graphs/{img_filename}'}
    print('Snapshot saved to', image_url)

if __name__ == "__main__":
    image_graph()