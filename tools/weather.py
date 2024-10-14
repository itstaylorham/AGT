import requests
import time
from datetime import datetime

def get_coordinates(zipcode):
    url = f"https://api.zippopotam.us/us/{zipcode}"
    response = requests.get(url)
    if response.status_code == 404:
        raise ValueError("Invalid ZIP code or location not found")
    data = response.json()
    if not data.get('places'):
        raise ValueError("Invalid ZIP code or location not found")
    place = data['places'][0]
    return {
        'latitude': place['latitude'],
        'longitude': place['longitude'],
        'place_name': place['place name'],
        'state': place['state']
    }

def get_grid_points(latitude, longitude, retries=3):
    url = f"https://api.weather.gov/points/{latitude},{longitude}"
    headers = {
        'User-Agent': '(weather-app, contact@example.com)',
        'Accept': 'application/json'
    }
    for _ in range(retries):
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            properties = data['properties']
            return {
                'office_id': properties['gridId'],
                'grid_x': properties['gridX'],
                'grid_y': properties['gridY'],
                'forecast_url': properties['forecast'],
                'observation_stations_url': properties['observationStations']
            }
        time.sleep(1)
    raise Exception("Failed to get grid points after multiple attempts")

def get_gridpoint_forecast(forecast_url, retries=3):
    headers = {
        'User-Agent': '(weather-app, contact@example.com)',
        'Accept': 'application/json'
    }
    for _ in range(retries):
        response = requests.get(forecast_url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if 'properties' in data and 'periods' in data['properties']:
                return data['properties']['periods']
        time.sleep(1)
    raise Exception("Failed to get forecast after multiple attempts")

def get_current_conditions(observation_stations_url, retries=3):
    headers = {
        'User-Agent': '(weather-app, contact@example.com)',
        'Accept': 'application/json'
    }
    for _ in range(retries):
        # Get the first observation station
        stations_response = requests.get(observation_stations_url, headers=headers)
        if stations_response.status_code == 200:
            stations_data = stations_response.json()
            if 'features' in stations_data and len(stations_data['features']) > 0:
                station_url = stations_data['features'][0]['id'] + '/observations/latest'
                
                # Get the current conditions from the station
                conditions_response = requests.get(station_url, headers=headers)
                if conditions_response.status_code == 200:
                    conditions_data = conditions_response.json()
                    return conditions_data
        time.sleep(1)
    raise Exception("Failed to get current conditions after multiple attempts")

def get_weather_forecast(zipcode):
    coords = get_coordinates(zipcode)
    grid = get_grid_points(coords['latitude'], coords['longitude'])
    forecast = get_gridpoint_forecast(grid['forecast_url'])
    current_conditions = get_current_conditions(grid['observation_stations_url'])
    return {
        'zipcode': zipcode,
        'location': {
            'place_name': coords['place_name'],
            'state': coords['state']
        },
        'grid': grid,
        'forecast': forecast,
        'current_conditions': current_conditions
    }

def print_forecast(forecast_data):
    print(f"Weather for {forecast_data['location']['place_name']}, "
          f"{forecast_data['location']['state']} ({forecast_data['zipcode']})")
    print(f"NWS Grid: {forecast_data['grid']['office_id']} "
          f"{forecast_data['grid']['grid_x']},{forecast_data['grid']['grid_y']}\n")


    print("Forecast:")
    for period in reversed(forecast_data['forecast'][:2]):  # Print first 3 periods
        print(f"{period['name']}:")
        print(f"Temperature: {period['temperature']}°{period['temperatureUnit']}")
        print(f"Conditions: {period['shortForecast']}")
        print(f"Wind: {period['windSpeed']} {period['windDirection']}")
        print(f"Details: {period['detailedForecast']}\n")

        # Print current conditions
    current = forecast_data['current_conditions']
    if 'properties' in current:
        props = current['properties']
        timestamp = datetime.fromisoformat(props['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
        print("Current Conditions:")
        print(f"As of: {timestamp}")
        print(f"Temperature: {props['temperature']['value']:.1f}°C / {(props['temperature']['value'] * 9/5 + 32):.1f}°F")
        print(f"Humidity: {props['relativeHumidity']['value']:.1f}%")
        print(f"Wind: {props['windSpeed']['value']} {props['windDirection']['value']}")
        print(f"Conditions: {props['textDescription']}\n")

if __name__ == "__main__":
    try:
        zipcode = input("Enter a ZIP code: ")
        forecast_data = get_weather_forecast(zipcode)
        print_forecast(forecast_data)
    except Exception as e:
        print(f"Error: {str(e)}")