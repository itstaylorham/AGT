import os
import json
import mysql.connector
import datetime

def convert_unix_to_timestamp(unix_time):
    dt = datetime.datetime.fromtimestamp(unix_time / 1e9)
    timestamp = dt.strftime('%Y-%m-%d %H:%M:%S')
    return timestamp

def main():
    # Step 1: Ask if the user wants to enter data into the database
    answer = input("Do you want to add data to the database? (yes/no): ")
    
    # Step 2: If yes, ask for the type of data
    if answer.lower() == "yes":
        data_type = input("Enter the type of data to insert into the database (read/predict/metric): ")
        
        # Step 3: Check data type and proceed accordingly
        if data_type.lower() == "read":
            directory = "/home/jeremy/Documents/AGT/__files__/read_files"
            insert_read_data(directory)
        elif data_type.lower() == "predict" or data_type.lower() == "metric":
            print("Not implemented for now.")
        else:
            print("Invalid data type entered. Please choose read, predict, or metric.")
    else:
        print("No data will be added to the database.")

def insert_read_data(directory):
    total_files = 0

    # Get the keys from the DB-CONNECT section.
    db_config = config['DB-CONNECT']
    user = db_config.get('user')
    password = db_config.get('password')
    host = db_config.get('host')
    database = db_config.get('database')
    auth_plugin = db_config.get('auth_plugin')

    cnx = mysql.connector.connect(
        user=user, 
        password=password, 
        host=host, 
        database=database,
        auth_plugin=auth_plugin
    )

    all_data = []

    try:
        subdirectories = next(os.walk(directory))[1]
    except StopIteration:
        print(f"No subdirectories found in {directory}")
        return

    for subdirectory in subdirectories:
        subdirectory_path = os.path.join(directory, subdirectory)
        files = os.listdir(subdirectory_path)
        subdirectory_data = []

        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(subdirectory_path, file)
                with open(file_path, "r") as f:
                    data = json.load(f)
                subdirectory_data.append(data)
                total_files += 1

        all_data.extend(subdirectory_data)

    data = [element for sublist in all_data for element in (sublist if isinstance(sublist, list) else [sublist])]
    
    # The block you provided goes here
    answer = input("Do you want to add the data to the database? (yes/no): ")
    if answer.lower() == "yes":
        user_date_input = input("Enter the date for which you want to insert data (e.g., 'today' or 'YYYY-MM-DD'): ")
        if user_date_input.lower() == "today":
            today_date = datetime.datetime.today().strftime('%Y-%m-%d')
            filtered_data = [item for item in data if item['Timestamp'].startswith(today_date)]
        elif user_date_input and len(user_date_input) == 10:
            filtered_data = [item for item in data if item['Timestamp'].startswith(user_date_input)]

        for item in filtered_data:
            item['Timestamp'] = convert_unix_to_timestamp(item['Timestamp'])
    else:
        filtered_data = []  # Or any other appropriate action
    
    try:
        cursor = cnx.cursor()
        query = "INSERT INTO SENSOR_READINGS (TIMESTAMP, MAC, TEMPERATURE, MOISTURE, LIGHT, CONDUCTIVITY) VALUES (%s, %s, %s, %s, %s, %s)"
        for item in filtered_data:
            values = (item['Timestamp'], item['MAC'], item['Temperature'], item['Moisture'], item['Light'], item['Conductivity'])
            cursor.execute(query, values)
        cnx.commit()
        print("Data inserted successfully into the database.")
    except Exception as e:
        print(f"Error: {e}")
        cnx.rollback()
    finally:
        cnx.close()

if __name__ == "__main__":
    main()
