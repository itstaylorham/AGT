import os
import json
import configparser
from datetime import datetime, timedelta
from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app and database
app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

# Read configuration
config = configparser.ConfigParser()
config.read('setup.cfg')
HOST = config.get('FLASK', 'host', fallback='127.0.0.1')
PORT = config.getint('FLASK', 'port', fallback=5000)

# Define your database model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

# Define routes
@app.route('/')
def base():
    return render_template('base.html')

@app.route('/journal')
def journal():
    return render_template('journal.html')

@app.route('/analysis')
def analysis():
    return render_template('analysis.html')

@app.route('/api')
def api():
    return render_template('api.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')
    
@app.route('/api/sensor_data', methods=['GET'])
def get_sensor_data():
    # Define the full path to the sesh.json file
    file_path = os.path.join('sesh.json')

    sensor_data_list = []
    
    try:
        with open(file_path, 'r') as f:
            content = f.read().strip()
            if not content:
                return jsonify([])  # Return an empty list if the file is empty

            raw_sensor_data = json.loads(content)
            
            # Calculate the time 24 hours ago
            twenty_four_hours_ago = datetime.now() - timedelta(hours=999999)
            
            # Iterate over the sensor data entries and filter
            for data in raw_sensor_data:
                timestamp = datetime.strptime(data.get('Timestamp'), '%Y-%m-%d %H:%M:%S')
                
                # Only include entries from the last 24 hours
                if timestamp >= twenty_four_hours_ago:
                    new_entry = {
                        'timestamp': timestamp,
                        'mac_address': data.get('MAC'),
                        'temperature': data.get('Temperature'),
                        'light': data.get('Light'),
                        'moisture': data.get('Moisture'),
                        'conductivity': data.get('Conductivity')
                    }
                    sensor_data_list.append(new_entry)

    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return jsonify([])  # Return an empty list if the file doesn't exist
    except json.JSONDecodeError:
        print(f"Invalid JSON in file: {file_path}")
        return jsonify([])  # Return an empty list if the JSON is invalid

    # Return the sensor data as a JSON response
    return jsonify(sensor_data_list)


if __name__ == "__main__":
    app.run(host=HOST, port=PORT)