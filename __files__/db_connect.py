import os
import json
import mysql.connector
import datetime
import cursor
try:
    cnx = mysql.connector.connect(
        user="jeremy", 
        password="Starfish!2345", 
        host="localhost", 
        database="AGT_DB",
        auth_plugin='caching_sha2_password'
    )
    if cnx.is_connected():
        print("")
        print("/ / SUCCESSFUL CONNECTION / /")
        print("")
    else:
        print("")
        print("??? NOT CONNECTED: UNKNOWN ERROR ???")
        print("")
except mysql.connector.Error as err:
        print("")
        print("!!!! FAILED TO CONNECT !!!!")
        print("")
        print(f"Error: {err}")

def read_json_files(directory):
    total_files = 0
    all_data = []  # List to store consolidated data from all JSON files

    
    try:
        # Get a list of all the subdirectories in the directory
        subdirectories = next(os.walk(directory))[1]
    except StopIteration:
        print(f"No subdirectories found in {directory}")
        return
    
    # Iterate over each subdirectory
    for subdirectory in subdirectories:
        # Construct the full path to the subdirectory
        subdirectory_path = os.path.join(directory, subdirectory)

        # Get a list of all the files in the subdirectory
        files = os.listdir(subdirectory_path)
        
        # List to store data from JSON files within the current subdirectory
        subdirectory_data = []

        # Iterate over each file
        for file in files:
            # Check if the file is a JSON file
            if file.endswith(".json"):
                # Construct the full path to the file
                file_path = os.path.join(subdirectory_path, file)

                # Open the file and load the JSON data
                with open(file_path, "r") as f:
                    data = json.load(f)

                # Append the data to the list for the current subdirectory
                subdirectory_data.append(data)

                # Increment the total_files counter
                total_files += 1

        # Append the data from the current subdirectory to the all_data list
        all_data.extend(subdirectory_data)
        
    # Flatten the nested list using a nested list comprehension
    all_data = [element for sublist in all_data for element in (sublist if isinstance(sublist, list) else [sublist])]
    
    print("")
    # print(all_data)
    print(f"{len(all_data)} entries found from {len(subdirectories)} days recorded.")
    print("")

    # print(subdirectories)
    
    
def convert_unix_to_timestamp(unix_time):
   # Convert the Unix time to a datetime object
     dt = datetime.datetime.fromtimestamp(unix_time / 1e9)  # Divide by 1e9 to convert nanoseconds to seconds

    # Convert the datetime object to a string in the format 'YYYY-MM-DD HH:MM:SS'
     timestamp = dt.strftime('%Y-%m-%d %H:%M:%S')

     return timestamp

# Call the function
read_json_files("/home/jeremy/Documents/AGT/__files__/read_files")

from __files__.db_insert import insert_check
insert_check("/home/jeremy/Documents/AGT/__files__/read_files")
       
