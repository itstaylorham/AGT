#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import subprocess
from datetime import datetime
import os
import pandas as pd

class CommandManager:
    """Handles command validation and execution."""
    VALID_COMMANDS = [
        "scan", "read", "find", "trend", "update", "sesh", "train", "testing model", "push", 
        "live", "new sesh", "avg", "cluster", "full anal", "fcast", "fcast 3d", 
        "build", "summary", "corr", "pred", "cleaner", "nn", "export", "export csv", 
        "export xl", "dbconn"
    ]

    def validate_command(self, command):
        """Check if the command is valid."""
        return command in self.VALID_COMMANDS

class DataManager:
    """Handles data operations, including cleaning and exporting."""
    
    @staticmethod
    def clean_data(data):
        data['Timestamp'] = pd.to_datetime(data['Timestamp'].str[0]).dt.strftime('%Y-%m-%d %H:%M:%S')
        data['MAC'] = data['MAC'].str[0]
        data['Moisture'] = data['Moisture'].str[0]
        data['Light'] = data['Light'].str[0]
        data['Temperature'] = data['Temperature'].str[0]
        data['Conductivity'] = data['Conductivity'].str[0]
        return data

    @staticmethod
    def export_data(data, file_format, timestamp):
        """Export cleaned data to the specified format."""
        if not os.path.exists("files/export"):
            os.makedirs("files/export")

        if file_format == 'json':
            data.to_json(f'files/export/{timestamp}.json')
            print('Current session saved as JSON in exports folder.')
        elif file_format == 'csv':
            data.to_csv(f'files/export/{timestamp}.csv')
            print('Current session saved as CSV in exports folder.')
        elif file_format == 'excel':
            data.to_excel(f'files/export/{timestamp}.xlsx')
            print('Current session saved as Excel in exports folder.')

class Session:
    """Manages read sessions and counter for auto-clustering."""

    def __init__(self):
        self.read_counter = 0
        self.ping_counter = 0  # Counter for number of pings before clustering
        self.session_time = 300  # Time between read sessions in seconds
        self.auto_cluster_time = 150  # Time for the auto-cluster after pings

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

    def display_timers(self, next_ping_seconds, cluster_seconds):
        """Displays the countdown times for the next ping and cluster."""
        while next_ping_seconds > 0 or cluster_seconds > 0:
            
            if cluster_seconds > 0:
                print(f"\rNEXT CLUSTER: {cluster_seconds // 60:02d}:{cluster_seconds % 60:02d}    ", end='', flush=True)
                time.sleep(1)
                cluster_seconds -= 1
            
            if next_ping_seconds > 0:
                print(f"\rNEXT PING: {next_ping_seconds // 60:02d}:{next_ping_seconds % 60:02d}    ", end='', flush=True)
                time.sleep(1)
                next_ping_seconds -= 1

    def start_read_session(self):
        """Starts a read session and manages the read counter."""
        while True:
            print("Starting read session...")
            start_time = time.time()  # Record the start time of the read session
            subprocess.run(["python", "read.py"])  # Execute read.py
            self.read_counter += 1

            # Calculate time taken for the read session
            time_taken = time.time() - start_time
            print(f"Read session completed in {time_taken:.2f} seconds.")

            # Calculate time until the next ping
            time_until_next_ping = self.session_time - time_taken  # Time until the next ping
            if time_until_next_ping > 0:
                next_ping_seconds = int(time_until_next_ping)  # Remaining time for ping
            else:
                next_ping_seconds = 0  # No waiting time if the session took longer than the defined time

            self.ping_counter += 1  # Increment the ping counter after each read

            if self.read_counter >= 5:
                print("2 read sessions completed, running auto-cluster...")
                subprocess.run(["python", "tools/auto-cluster.py", "--from_main"])

                # Create countdown for auto-cluster based on the number of pings
                cluster_seconds = self.auto_cluster_time - (self.ping_counter * self.session_time)
                self.ping_counter = 0  # Reset the ping counter after clustering
                self.read_counter = 0  # Reset read session counter

                # Start displaying timers
                self.display_timers(next_ping_seconds, cluster_seconds)
            else:
                # Just wait for the next read session
                print(f"Waiting for the next read session for {self.session_time} seconds...")
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
        """Exports the current session data in the specified format."""
        data = pd.read_json("sesh.json")
        cleaned_data = self.data_manager.clean_data(data)
        timestamp = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")

        if command == "export":
            self.data_manager.export_data(cleaned_data, 'json', timestamp)
        elif command == "export csv":
            self.data_manager.export_data(cleaned_data, 'csv', timestamp)
        elif command == "export xl":
            self.data_manager.export_data(cleaned_data, 'excel', timestamp)


if __name__ == "__main__":
    app = App()
    app.run()