import pandas as pd
import json

# Function to get user input for each subject's data
def get_subject_data():
    subjects = []
    while True:
        # Prompt the user to enter a subject or press 'Q' to quit
        subject = input("Enter subject name (or 'Q' to finish): ").strip()
        if subject.lower() == 'q':
            break

        # Get high and low values for the subject
        temp_high = float(input(f"Enter {subject}'s high temperature: "))
        temp_low = float(input(f"Enter {subject}'s low temperature: "))
        
        moist_high = float(input(f"Enter {subject}'s high moisture: "))
        moist_low = float(input(f"Enter {subject}'s low moisture: "))
        
        light_high = float(input(f"Enter {subject}'s high light level: "))
        light_low = float(input(f"Enter {subject}'s low light level: "))
        
        cond_high = float(input(f"Enter {subject}'s high conductivity: "))
        cond_low = float(input(f"Enter {subject}'s low conductivity: "))

        # Generate subject ID (e.g., "S001", "S002", etc.)
        subject_id = f"S{len(subjects) + 1:03}"

        # Append all data as a dictionary to the subjects list
        subjects.append({
            'SUBJECT_ID': subject_id,
            'SUBJECT_NME': subject,
            'TEMP_HIGH': temp_high,
            'TEMP_LOW': temp_low,
            'MOIST_HIGH': moist_high,
            'MOIST_LOW': moist_low,
            'LIGHT_HIGH': light_high,
            'LIGHT_LOW': light_low,
            'COND_HIGH': cond_high,
            'COND_LOW': cond_low
        })

    return subjects

# Main function to handle session and subject inputs
def main():
    # Get session name and location
    session_name = input("Enter session name: ").strip()
    session_location = input("Enter session location: ").strip()

    # Get subjects and their respective data
    subjects = get_subject_data()

    if not subjects:
        print("No subjects entered. Exiting.")
        return

    # Create a DataFrame from the subject data
    sesh_data = pd.DataFrame(subjects)

    # Add session name and location to each row
    sesh_data['SESH_NAME'] = session_name
    sesh_data['SESH_LOCATION'] = session_location

    # Convert the DataFrame to JSON format
    json_data = sesh_data.to_json(orient='records', indent=4)

    # Write the JSON data to a file
    with open("session_data.json", "w") as json_file:
        json_file.write(json_data)

    print("Session data saved to 'session_data.json'.")

# Call the main function to start the program
if __name__ == "__main__":
    main()
