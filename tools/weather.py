import requests
import time

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
                'forecast_url': properties['forecast']
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

def get_weather_forecast(zipcode):
    coords = get_coordinates(zipcode)
    grid = get_grid_points(coords['latitude'], coords['longitude'])
    forecast = get_gridpoint_forecast(grid['forecast_url'])
    return {
        'zipcode': zipcode,
        'location': {
            'place_name': coords['place_name'],
            'state': coords['state']
        },
        'grid': grid,
        'forecast': forecast
    }

def print_forecast(forecast_data):
    print(f"Weather Forecast for {forecast_data['location']['place_name']}, "
          f"{forecast_data['location']['state']} ({forecast_data['zipcode']})")
    print(f"NWS Grid: {forecast_data['grid']['office_id']} "
          f"{forecast_data['grid']['grid_x']},{forecast_data['grid']['grid_y']}\n")

    for period in forecast_data['forecast'][:3]:  # Print first 3 periods
        print(f"{period['name']}:")
        print(f"Temperature: {period['temperature']}°{period['temperatureUnit']}")
        print(f"Conditions: {period['shortForecast']}")
        print(f"Wind: {period['windSpeed']} {period['windDirection']}")
        print(f"Details: {period['detailedForecast']}\n")

if __name__ == "__main__":
    try:
        zipcode = input("Enter a ZIP code: ")
        forecast_data = get_weather_forecast(zipcode)
        print_forecast(forecast_data)
    except Exception as e:
        print(f"Error: {str(e)}")