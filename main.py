#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import subprocess
import configparser
import json  # Use this for safer loading of JSON data
from datetime import datetime
import os
import pandas as pd

class CommandManager:
    """Handles command validation and execution."""
    VALID_COMMANDS = [
        "scan", "read", "find", "trend", "update", "sesh", "train", "testing model", "push", 
        "live", "new sesh", "report", "avg", "cluster", "weather", "full anal", "fcast", "fcast 3d", 
        "build", "summary", "corr", "pred", "cleaner", "nn", "export", "export csv", 
        "export xl", "dbconn", "batch"
    ]

    def validate_command(self, command):
        """Check if the command is valid."""
        return command in self.VALID_COMMANDS

class DataManager:
    """Handles data operations, including cleaning and exporting."""
    
    @staticmethod
    def clean_data(data):
        """Clean and prepare data for export while preserving precision."""
        # Convert timestamp to consistent format
        data['Timestamp'] = pd.to_datetime(data['Timestamp'], errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')
        
        # Handle missing columns but preserve actual values
        required_columns = ['MAC', 'Moisture', 'Light', 'Temperature', 'Conductivity']
        for col in required_columns:
            if col not in data.columns:
                print(f"Warning: {col} column missing. Adding empty values.")
                data[col] = ""
                
        # Handle null values but keep the data types appropriate
        data['MAC'] = data['MAC'].fillna("")
        data['Moisture'] = pd.to_numeric(data['Moisture'], errors='coerce').fillna(0)
        data['Light'] = pd.to_numeric(data['Light'], errors='coerce').fillna(0)
        data['Temperature'] = pd.to_numeric(data['Temperature'], errors='coerce').fillna(0)
        data['Conductivity'] = pd.to_numeric(data['Conductivity'], errors='coerce').fillna(0)
        
        return data
        
    @staticmethod
    def run_report():
        rmd_path = "journal/R-Journals/weekly_summary_testing.Rmd"
        output_format = "html_document"  # Could be "pdf_document" if LaTeX is set up
        command = [
            "Rscript", "-e",
            f"rmarkdown::render('{rmd_path}', output_format = '{output_format}')"
        ]
        
        try:
            print("Generating report...")
            subprocess.run(command, check=True)
            print("Report generated successfully.")
        except subprocess.CalledProcessError as e:
            print("Error generating report:", e)
    

    @staticmethod
    def export_data(data, file_format, timestamp):
        """Export cleaned data to the specified format with filtering by days and sorting options."""
        if not os.path.exists("files/export"):
            os.makedirs("files/export")
        
        # Convert Timestamp column to datetime for filtering
        data['Timestamp'] = pd.to_datetime(data['Timestamp'])
        
        # Ask user for how many days of data to export
        try:
            days = int(input("How many days of data would you like to export? (Enter 0 for all data): "))
            if days < 0:
                print("Invalid input. Using all available data.")
                days = 0
        except ValueError:
            print("Invalid input. Using all available data.")
            days = 0
        
        # Filter data by days if specified
        if days > 0:
            current_date = datetime.now()
            filter_date = current_date - pd.Timedelta(days=days)
            data = data[data['Timestamp'] >= filter_date]
            if data.empty:
                print(f"No data found within the last {days} days.")
                return
        
        # Ask user for sorting order
        sort_order = input("Sort by timestamp in ascending (ASC) or descending (DESC) order? ").strip().upper()
        if sort_order == "ASC":
            data = data.sort_values('Timestamp', ascending=True)
        elif sort_order == "DESC":
            data = data.sort_values('Timestamp', ascending=False)
        else:
            print("Invalid sort order. Using ascending order by default.")
            data = data.sort_values('Timestamp', ascending=True)
        
        # Convert Timestamp back to string format for export
        data['Timestamp'] = data['Timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
        
        # Export data in the specified format
        if file_format == 'json':
            data.to_json(f'files/export/{timestamp}.json', orient='records')
            print(f'Data for the last {days if days > 0 else "all"} days saved as JSON in /AGT/files/export')
        elif file_format == 'csv':
            data.to_csv(f'files/export/{timestamp}.csv', index=False)
            print(f'Data for the last {days if days > 0 else "all"} days saved as CSV in /AGT/files/export')
        elif file_format == 'excel':
            data.to_excel(f'files/export/{timestamp}.xlsx', index=False)
            print(f'Data for the last {days if days > 0 else "all"} days saved as Excel in /AGT/files/export')

class Session:
    """Manages read sessions and counter for auto-clustering."""
    
    def __init__(self):
        self.read_counter = 0
        self.ping_counter = 0
        self.session_time = 600
        self.weather_counter = 0
        self.devices = self.load_devices()  # Load devices from setup.cfg

    def load_devices(self):
        """Load devices from the setup.cfg file."""
        config = configparser.ConfigParser()
        config.read('setup.cfg')
        macs_str = config.get('DEVICE', 'macs')
        macs_list = json.loads(macs_str)  # Use json.loads for safer parsing
        return macs_list

    def display_devices(self):
        """Displays the current devices for scanning."""
        print("Current devices available for scanning:")
        for idx, device in enumerate(self.devices, start=1):
            print(f"{idx}: {device}")

    def configure_session(self):
        """Configure the session based on user input."""
        print("< Display the current devices > These are the devices that will be scanned.")
        self.display_devices()
        if input("Continue? (Y/N) >>> ").strip().upper() != "Y":
            print("Session setup canceled.")
            return False

        # Get the time interval between pings
        try:
            self.session_time = int(input("\nPlease enter time between pings (in seconds)\n>>> ").strip())
        except ValueError:
            print("Invalid input. Using default session time of 300 seconds.")

        if input("\nGo live? (Y/N) \n>>> ").strip().upper() == "Y":
            print("Starting live monitoring session...")
            subprocess.run(["python", "backend/app.py"])

        print("Session configured with applied settings.")
        return True

    def countdown(self, seconds, message):
        """Displays a countdown timer in HH:MM:SS format."""
        print(message)
        while seconds > 0:
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            secs = seconds % 60
            timer = f'\rTime remaining: {hours:02d}:{minutes:02d}:{secs:02d}'
            print(timer, end='', flush=True)
            time.sleep(1)
            seconds -= 1
        print('\nCompleted!')

    def start_read_session(self):
        """Starts a read session and manages the read counter based on user-defined settings."""
        if not self.configure_session():
            return  # Exit if session setup is canceled

        while True:
            print("Starting read session...")
            start_time = time.time()
            subprocess.run(["python", "read.py"])
            self.read_counter += 1
            self.weather_counter += 1

            # Calculate time taken for the read session
            time_taken = time.time() - start_time
            print(f"\nRead session completed in {time_taken:.2f} seconds.\n")

            time_until_next_ping = self.session_time - time_taken
            next_ping_seconds = max(0, int(time_until_next_ping))
            self.ping_counter += 1

            self.countdown(self.session_time, "Waiting for the next read session to start...")

class App:
    """Main application class to handle user input and command execution."""
    
    def __init__(self):
        self.command_manager = CommandManager()
        self.data_manager = DataManager()
        self.session = Session()

    def run(self):
        """Main application loop for user input."""
        print("\nAGT Live\nv0.1.3\n")
        print("ctrl+z to quit\n")

        while True:
            usrinpt = input(">>> ")

            if self.command_manager.validate_command(usrinpt):
                self.execute_command(usrinpt)
            else:
                print("Invalid command!")

    def execute_command(self, command):
        """Executes the command based on user input."""
        if command == "scan":
            from scan import stats
            print(stats)
        elif command == "read":
            subprocess.run(["python", "read.py"])
        elif command == "sesh":
            self.session.start_read_session()
        elif command == "update":
            subprocess.run(["python", "files/mini_insert.py"])
        elif command == "train":
            subprocess.run(["python", "tools/neural_net/modular/model.py", "--from_main"])
        elif command == "cluster":
            subprocess.run(["python", "tools/auto-cluster.py", "--from_main"])
        elif command == "weather":
            subprocess.run(["python", "tools/weather.py", "--from_main"])
        elif command == "push":
            subprocess.run(["python", "read.py"])
            subprocess.run(["python", "tools/neural_net/modular/model.py", "--from_main"])
        elif command == "live":
            subprocess.run(["python", "web_ui/app.py"])
            time.sleep(600)
        elif command == "new sesh":
            self.start_new_session()
        elif command in ["avg", "trend", "fcast", "fcast 3d", "summary", "corr", "pred", "cleaner", "nn"]:
            subprocess.run([f"python", f"tools/plot/{command}.py"])
        elif command == "batch":
            subprocess.run(["python", "tools/batch-builder.py"])
        elif command == "report":
            run_report()
        elif command in ["export", "export csv", "export xl"]:
            self.export_session_data(command)
        elif command == "build":
            subprocess.run(["python", "/home/jeremy/Documents/AGT/tools/report/build_report.py"])
        elif command == "dbconn":
            subprocess.run(["python", "files/db_connect.py"])

    def start_new_session(self):
        """Starts a new session after confirmation."""
        confirm = input("Are you sure you want to start a new session? This will clear any current session data. (Y/N)? ")
        if confirm == "Y":
            print("Deleting previous session data...")
            subprocess.run(["rm", "-rf", "sesh.json"])
            self.session.start_read_session()
        else:
            print("New session cancelled.")

    def export_session_data(self, command):
        """Exports the current session data in the specified format with filtering options."""
        try:
            data = pd.read_json("sesh.json")
            if data.empty:
                print("No data available to export.")
                return
                
            # Ask user which devices to filter on by MAC address
            mac_input = input("Enter the MAC address(es) you want to filter by (separate multiple with space): ").strip()
            if mac_input:
                macs_to_filter = mac_input.split()
                if all(self.is_valid_mac(mac) for mac in macs_to_filter):
                    # Filter data by MAC addresses
                    data = data[data['MAC'].isin(macs_to_filter)]
                else:
                    print("Invalid MAC address format. No filter applied.")
            
            cleaned_data = self.data_manager.clean_data(data)
            timestamp = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")

            if command == "export":
                self.data_manager.export_data(cleaned_data, 'json', timestamp)
            elif command == "export csv":
                self.data_manager.export_data(cleaned_data, 'csv', timestamp)
            elif command == "export xl":
                self.data_manager.export_data(cleaned_data, 'excel', timestamp)
        except Exception as e:
            print(f"Error exporting data: {e}")

    @staticmethod
    def is_valid_mac(mac):
        """Validates the MAC address format (basic validation)."""
        # MAC addresses are usually in format XX:XX:XX:XX:XX:XX
        return len(mac) == 17 and all(part.isalnum() and len(part) == 2 for part in mac.split(":"))
        
# Running the app
if __name__ == "__main__":
    app = App()
    app.run()
