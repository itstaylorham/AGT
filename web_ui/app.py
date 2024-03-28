import os
import json
import glob
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import pytz
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, url_for, send_file
import app

# PREPROCESSING

app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id\


# AGROTECH.LIVE ROUTES


@app.route('/')
def base():
    return render_template('base.html')


@app.route('/reports')
def reports():
    return render_template('reports.html')


@app.route('/analysis')
def analysis():
    return render_template('analysis.html')


@app.route('/api')
def api():
    return render_template('api.html')

@app.route('/api/sensor_data', methods=['GET'])
def get_sensor_data():
    main_directory = '/home/jeremy/Documents/AGT/__files__/read_files'

    # Get list of all json files in directory and subdirectories and sort by modification time
    files = [f for f in glob.glob(main_directory + "/**/*.json", recursive=True)]
    files.sort(key=os.path.getmtime, reverse=True)

    sensor_data_list = []  # Create empty list to later store sensor data dicts

    # Read JSON files
    for file in files:
        with open(file, 'r') as f:
            if f.read().strip():  # Check if file is not empty
                f.seek(0)  # Move read cursor to the start of the file
                try:
                    raw_sensor_data = json.load(f)
                except json.JSONDecodeError:
                    print(f"File {file} is not a valid JSON document.")
                    continue  # Skip to the next file
            else:
                continue  # Skip this iteration if the file is empty

            # Parse every line in JSON
            for data in raw_sensor_data:
                timestamp = datetime.strptime(data.get('Timestamp'), '%Y-%m-%d %H:%M:%S')
                new_entry = {
                    'timestamp': timestamp,
                    'mac_address': data.get('MAC'),
                    'temperature': data.get('Temperature'),
                    'light': data.get('Light'),
                    'moisture': data.get('Moisture'),
                    'conductivity': data.get('Conductivity')
                }
                sensor_data_list.append(new_entry)  # Add the new entry to the list

    return jsonify(sensor_data_list)  # Return the list as JSON


@app.route('/api/graph_data', methods=['GET'])
def get_graph_data():
    with open('sesh.json', 'r') as f:
        graph_data = json.load(f)

    # Only keep the last 144 entries
    graph_data = graph_data[-144:]
    
    return jsonify(graph_data)

from flask import jsonify
import json
from datetime import datetime

@app.route('/api/metric_data', methods=['GET'])
def get_metric_data():
    main_directory = '/home/jeremy/Documents/AGT/__files__/metrics'

    # Get the most recent date-titled folder
    date_folders = [d for d in os.listdir(main_directory) if os.path.isdir(os.path.join(main_directory, d))]
    date_folders.sort(reverse=True)
    if not date_folders:
        return jsonify([])  # Return an empty list if no date-titled folders are found

    most_recent_folder = date_folders[0]
    folder_path = os.path.join(main_directory, most_recent_folder)

    files = [f for f in glob.glob(folder_path + "/*.json")]
    files.sort(key=os.path.getmtime, reverse=True)

    metric_data_list = []

    for file in files:
        with open(file, 'r') as f:
            content = f.read().strip()  # Read and strip the file content
            if content:
                try:
                    raw_sensor_data = json.loads(content)  # Parse the JSON data
                    if not isinstance(raw_sensor_data, list):  # Check if raw_sensor_data is not a list
                        print(f"Data in file {file} is not a list.")
                        continue
                except json.JSONDecodeError:
                    print(f"File {file} is not a valid JSON document.")
                    continue
            else:
                continue

            for data in raw_sensor_data:
                if not isinstance(data, dict):
                    print(f"Expected a dictionary but got a {type(data)} in file {file}")
                    continue
                
                timestamp_str = data.get('timestamp')  # Match key to JSON structure
                if not timestamp_str:
                    print(f"Missing or empty 'timestamp' in file {file}")
                    continue

                try:
                    timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
                    new_entry = {
                        'timestamp': timestamp,
                        'temperature': data.get('temperature_r2'),  # Match key to JSON structure
                        'moisture': data.get('moisture_r2'),       # Match key to JSON structure
                        'light': data.get('light_r2'),             # Match key to JSON structure
                        'conductivity': data.get('conductivity_r2'),  # Match key to JSON structure
                        'health_score': data.get('health_score')   # Include additional field from JSON
                    }
                    metric_data_list.append(new_entry)
                except (TypeError, ValueError) as e:
                    print(f"Error processing data in file {file}: {e}")

    return jsonify(metric_data_list)


if __name__ == "__main__":
    app.run(host='192.168.68.113', port=3000)

