import os
import json
import glob
import configparser
from datetime import datetime
from Flask import Flask, jsonify, render_template
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
    main_directory = '/home/jeremy/Documents/AGT/files/read_files'
    files = [f for f in glob.glob(main_directory + "/**/*.json", recursive=True)]
    files.sort(key=os.path.getmtime, reverse=True)

    sensor_data_list = []
    for file in files:
        try:
            with open(file, 'r') as f:
                content = f.read().strip()
                if not content:
                    continue

                raw_sensor_data = json.loads(content)
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
                    sensor_data_list.append(new_entry)

        except FileNotFoundError:
            print(f"File not found: {file}")
        except json.JSONDecodeError:
            print(f"Invalid JSON in file: {file}")

    return jsonify(sensor_data_list)

# Additional API routes...

if __name__ == "__main__":
    app.run(host=HOST, port=PORT)
