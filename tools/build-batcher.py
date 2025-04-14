import csv
import numpy as np
import os
import json
from datetime import datetime
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def parse_timestamp(timestamp_str):
    """Convert timestamp string to datetime object."""
    return datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')

def seconds_between(t1, t2):
    """Calculate seconds between two datetime objects."""
    delta = t2 - t1
    return abs(delta.total_seconds())

def sine_function(x, baseline, amplitude, period, phase):
    """Sine function for curve fitting."""
    return baseline + amplitude * np.sin(2 * np.pi * x / period + phase)

def analyze_csv(file_path):
    """Analyze sensor data CSV and extract parameters."""
    # Try to read the CSV file with various methods
    data = []
    
    try:
        # First attempt: standard CSV reader
        with open(file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data.append(row)
    except Exception as e:
        print(f"Standard CSV reading failed: {e}")
        
        # Second attempt: try to parse as JSON
        try:
            with open(file_path, 'r') as jsonfile:
                content = jsonfile.read()
                # Check if the content looks like JSON array
                if content.strip().startswith('[') and content.strip().endswith(']'):
                    data = json.loads(content)
                else:
                    print("File appears to be neither a valid CSV nor JSON array.")
                    return
        except Exception as json_error:
            print(f"JSON parsing also failed: {json_error}")
            print("Please provide the data in a valid CSV or JSON format.")
            return
    
    if not data:
        print("Error: No data found in file.")
        return
    
    # Debug: Print the first row to see its structure
    print("Sample data row:")
    print(json.dumps(data[0], indent=2))
    
    # Check if the required keys exist
    required_fields = ['Timestamp', 'Temperature', 'Moisture', 'Light', 'Conductivity']
    
    # Case-insensitive field mapping
    field_mapping = {}
    if data:
        sample_row = data[0]
        for field in required_fields:
            for key in sample_row.keys():
                if key.lower() == field.lower():
                    field_mapping[field] = key
    
    # Verify all required fields are found
    missing_fields = [field for field in required_fields if field not in field_mapping]
    if missing_fields:
        print(f"Error: Missing required fields: {', '.join(missing_fields)}")
        print(f"Available fields: {', '.join(sample_row.keys())}")
        return
    
    # Convert timestamps and calculate interval
    timestamps = [parse_timestamp(row[field_mapping['Timestamp']]) for row in data]
    timestamps.sort()  # Ensure timestamps are in order
    
    # Calculate average interval duration
    intervals = []
    for i in range(len(timestamps) - 1):
        intervals.append(seconds_between(timestamps[i], timestamps[i+1]))
    
    interval_duration = np.mean(intervals) if intervals else 0
    print(f"Detected interval duration: {interval_duration:.2f} seconds")
    
    # Calculate total time span in days
    total_seconds = seconds_between(timestamps[0], timestamps[-1])
    days = total_seconds / (24 * 60 * 60)
    print(f"Data spans approximately {days:.2f} days")
    
    # Extract sensor data using the field mapping
    temp_data = np.array([float(row[field_mapping['Temperature']]) for row in data])
    moisture_data = np.array([float(row[field_mapping['Moisture']]) for row in data])
    light_data = np.array([float(row[field_mapping['Light']]) for row in data])
    cond_data = np.array([float(row[field_mapping['Conductivity']]) for row in data])
    
    # Create time points (normalized to match original script)
    time_points = np.arange(len(data))
    
    # Analyze each sensor type
    sensors = {
        'Temperature': temp_data,
        'Moisture': moisture_data,
        'Light': light_data,
        'Conductivity': cond_data
    }
    
    results = {}
    
    for sensor_name, sensor_values in sensors.items():
        print(f"\nAnalyzing {sensor_name}:")
        
        # Calculate range
        min_val = np.min(sensor_values)
        max_val = np.max(sensor_values)
        print(f"Range: {min_val:.2f} to {max_val:.2f}")
        
        # Attempt to fit a sine curve
        try:
            # Initial parameter guesses
            baseline_guess = np.mean(sensor_values)
            amplitude_guess = (max_val - min_val) / 2
            period_guess = len(sensor_values) / 2  # Guess at half the data length
            
            # Curve fitting
            params, _ = curve_fit(
                sine_function, 
                time_points, 
                sensor_values, 
                p0=[baseline_guess, amplitude_guess, period_guess, 0],
                maxfev=10000
            )
            
            baseline, amplitude, period, phase = params
            print(f"Estimated baseline: {baseline:.2f}")
            print(f"Estimated amplitude: {amplitude:.2f}")
            print(f"Estimated period: {period:.2f} intervals")
            
            # Calculate fitted values
            fitted_values = sine_function(time_points, baseline, amplitude, period, phase)
            
            # Calculate residuals
            residuals = sensor_values - fitted_values
            residual_std = np.std(residuals)
            print(f"Residual standard deviation: {residual_std:.4f}")
            
            # Estimate randomness (higher residuals = more randomness)
            # Scale to 1-10 range based on the amplitude
            norm_residual = residual_std / amplitude if amplitude != 0 else 0
            randomness = 1 + min(9, norm_residual * 9)  # Scale to 1-10
            
            # Store results
            results[sensor_name] = {
                'min': min_val,
                'max': max_val,
                'baseline': baseline,
                'amplitude': amplitude,
                'period': period,
                'randomness_component': randomness
            }
            
            # Optional: Plot for visualization
            plt.figure(figsize=(10, 6))
            plt.plot(time_points, sensor_values, 'b-', label='Data')
            plt.plot(time_points, fitted_values, 'r-', label='Fitted Sine')
            plt.title(f'{sensor_name} Analysis')
            plt.xlabel('Interval Index')
            plt.ylabel('Value')
            plt.legend()
            plt.tight_layout()
            
            # Save plot
            plot_dir = './analysis_plots'
            os.makedirs(plot_dir, exist_ok=True)
            plt.savefig(f'{plot_dir}/{sensor_name.lower()}_analysis.png')
            plt.close()
            
        except Exception as e:
            print(f"Curve fitting failed: {e}")
    
    # Overall randomness estimate (average of individual estimates)
    randomness_values = [results[sensor]['randomness_component'] for sensor in results]
    overall_randomness = np.mean(randomness_values)
    print(f"\nEstimated overall randomness value (1-10): {overall_randomness:.2f}")
    
    # Generate parameter summary
    print("\n--- SUMMARY OF ESTIMATED PARAMETERS ---")
    print("These parameters can be used as inputs to the original generator script:")
    
    print("\nSTAGE 1: Sinusoidal components")
    for sensor in ['Temperature', 'Moisture', 'Light', 'Conductivity']:
        if sensor in results:
            print(f"Baseline {sensor}: {results[sensor]['baseline']:.2f}")
            print(f"Amplitude {sensor}: {results[sensor]['amplitude']:.2f}")
            print(f"Period {sensor}: {results[sensor]['period']:.2f}")
    
    print("\nSTAGE 2: Range components")
    for sensor in ['Temperature', 'Moisture', 'Light', 'Conductivity']:
        if sensor in results:
            print(f"Lowest {sensor}: {results[sensor]['min']:.2f}")
            print(f"Highest {sensor}: {results[sensor]['max']:.2f}")
    
    print(f"\nRandomness value (1-10): {overall_randomness:.2f}")
    
    return results

def main():
    print('-- Sensor Data Parameter Analyzer --')
    print('This script analyzes existing sensor data to estimate the parameters that might have been used to generate it.')
    
    # Check if data is provided directly
    use_direct_data = input("Do you want to input data directly instead of using a file? (y/n): ").lower().strip() == 'y'
    
    if use_direct_data:
        print("Please paste your JSON data below (enter a blank line when finished):")
        lines = []
        while True:
            line = input()
            if not line:
                break
            lines.append(line)
        
        json_data = '\n'.join(lines)
        
        # Write to a temporary file
        temp_file = 'temp_data.json'
        with open(temp_file, 'w') as f:
            f.write(json_data)
        
        file_path = temp_file
    else:
        # Get file path from user
        file_path = input("Enter the path to the CSV or JSON file to analyze: ")
        
        # Ensure the file exists
        if not os.path.isfile(file_path):
            print(f"Error: File '{file_path}' not found.")
            return
    
    # Analyze the data
    analyze_csv(file_path)
    
    # Clean up temporary file if created
    if use_direct_data and os.path.exists(temp_file):
        try:
            os.remove(temp_file)
        except:
            pass
    
    print("\nAnalysis complete! Check the 'analysis_plots' directory for visualizations.")

if __name__ == "__main__":
    main()