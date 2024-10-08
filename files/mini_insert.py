import json
import mysql.connector
from datetime import datetime
import os
import glob
import configparser

# Read configuration
config = configparser.ConfigParser()
config.read('setup.cfg')

# Base directory for JSON files
base_dir = '/home/jeremy/Documents/AGT/files/read_files'

# Connect to MySQL database using configuration
db = mysql.connector.connect(
    host='127.0.0.1',
    user='jeremy',
    password='Starfish!2345',
    database='AGT_DB',
    auth_plugin='auth_plugin'
)
cursor = db.cursor()

# Function to check if a record already exists
def record_exists(timestamp, mac):
    sql = "SELECT COUNT(*) FROM AGT_2024_SENSOR_READINGS WHERE TIMECODE = %s AND MAC = %s"
    cursor.execute(sql, (timestamp, mac))
    count = cursor.fetchone()[0]
    return count > 0

# Function to process a single JSON file
def process_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    records_inserted = 0
    for reading in data:
        timestamp = datetime.strptime(reading['Timestamp'], '%Y-%m-%d %H:%M:%S')
        mac = reading['MAC']
        
        if not record_exists(timestamp, mac):
            sql = """
            INSERT INTO AGT_2024_SENSOR_READINGS 
            (TIMECODE, MAC, Temperature, Moisture, Light, Conductivity) 
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (
                timestamp,
                mac,
                reading['Temperature'],
                reading['Moisture'],
                reading['Light'],
                reading['Conductivity']
            )
            cursor.execute(sql, values)
            records_inserted += 1
    
    db.commit()
    return records_inserted

# Find and process all JSON files
total_records = 0
for date_dir in glob.glob(os.path.join(base_dir, '*')):
    if os.path.isdir(date_dir):
        date = os.path.basename(date_dir)
        json_file = os.path.join(date_dir, f'AGT-{date}.json')
        if os.path.exists(json_file):
            records_inserted = process_json_file(json_file)
            total_records += records_inserted
            print(f"Processed {json_file}: {records_inserted} records inserted")

cursor.close()
db.close()

if total_records > 0:
    print(f"Total records inserted: {total_records}")
else:
    print("There are no updates at this time.")