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
    print("AGT Rec")
    answer = input("Do you want to add data to the database? (yes/no): \n>>> ")
    
    # Step 2: If yes, ask for the type of data
    if answer.lower() == "yes":
        print("")
        print("[ INSERTING DATA ]")
        # Define data types collecetd from read files sets.
        data_types = {1: "read", 2: "predict", 3: "metric"}

        print("Enter the type of data:")
        # Loop through the dictionary and display the options
        for number, data_type in data_types.items():
            print(f"[{number}]: {data_type}")

        # Get the user input as an integer
        data_type = int(input())
        

        
        
        # Validation
        if data_type in data_types:

            data_type = data_types[data_type]
            # Proceed with the rest of the code
        directory = "/home/jeremy/Documents/AGT/__files__/read_files"
        filtered_data = get_filtered_data(directory)
        
        user_date_input = input("Enter the date for which you want to insert data (e.g., 'today' or 'YYYY-MM-DD'): ")
        if user_date_input.lower() == "today":
            today_date = datetime.datetime.today().strftime('%Y-%m-%d')
            filtered_data = [item for item in filtered_data if item['Timestamp'].startswith(today_date)]
        
        filtered_data = [item for item in filtered_data if item['Timestamp'].startswith(user_date_input)]

#       elif user_date_input and len(user_date_input) == 10:
#            filtered_data = [item for item in filtered_data if item['Timestamp'].startswith(user_date_input)]
#        print("User Entered Date:", user_date_input)
#        print("Filtered Data After Date Filtering:", filtered_data)


def get_filtered_data(directory):
    total_files = 0
    all_data = []

    try:
        subdirectories = next(os.walk(directory))[1]
    except StopIteration:
        print(f"No subdirectories found in {directory}")
        return []

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
    # print(data)
    filtered_data = [item for item in data if str(item['Timestamp']).startswith(datetime.datetime.today().strftime('%Y-%m-%d'))]
    for item in filtered_data:
        item['Timestamp'] = convert_unix_to_timestamp(item['Timestamp'])
    print(filtered_data)
    #print(data)
        
           #  print("Timestamp in Data:", item['Timestamp'])
            # print(filtered_data)

    return filtered_data
get_filtered_data("/home/jeremy/Documents/AGT/__files__/read_files")


try:
    cnx = mysql.connector.connect(
        user="jeremy", 
        password="Starfish!2345", 
        host="localhost", 
        database="AGT_DB",
        auth_plugin='caching_sha2_password'
    )

    if cnx.is_connected():
        print("Connected to the database")

        try:
            cursor = cnx.cursor()
            query = "INSERT INTO SENSOR_READINGS (TIMESTAMP, MAC, TEMPERATURE, MOISTURE, LIGHT, CONDUCTIVITY) VALUES (%s, %s, %s, %s, %s, %s)"
            
            for item in data:
                values = (item['Timestamp'], item['MAC'], item['Temperature'], item['Moisture'], item['Light'], item['Conductivity'])
                cursor.execute(query, values)

            cnx.commit()
            print("Data inserted successfully into the database.")
            
        except Exception as e:
            print(f"Error during insertion: {e}")
            cnx.rollback()
            
        finally:
            cursor.close()

    else:
        print("Not connected. Unknown error.")

except mysql.connector.Error as err:
    print("Failed to connect to the database. Check credentials.")
    print(f"Error: {err}")

finally:
    if cnx.is_connected():
        cnx.close()
            

    if __name__ == "__main__":
        main()