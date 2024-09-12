import requests
import time
import re
import numpy as np
import pandas as pd
import json

def parse_coordinate(coord_str):
    # Remove the brackets and split the string by comma
    coord_str = coord_str.strip('[]')
    lat, lon = map(float, coord_str.split(','))
    return lat, lon

def calculate_distance_car(row, des_coords):
    """Calculate routing distance from property to destination using OSRM API."""
    house_coords = parse_coordinate(row['Coordinates'])
    
    # Try the OSRM route API URL
    url = (
        f"http://router.project-osrm.org/route/v1/driving/"
        f"{house_coords[1]},{house_coords[0]};{des_coords[1]},{des_coords[0]}"
        f"?overview=false&alternatives=false&steps=false&annotations=distance"
    )
    
    try:
        # Make sure they don't blacklist me
        time.sleep(0.5)
        
        # Make the API call to get the route details
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError if the response code is not 200
        
        # Extract distance from the response
        data = response.json()
        if data.get('code') == 'Ok' and 'routes' in data:
            distance_meters = data['routes'][0]['legs'][0]['distance']
        else:
            distance_meters = None
    except (requests.RequestException, KeyError, IndexError, json.JSONDecodeError) as e:
        # Log the exception if needed and return None for error cases
        print(f"Error fetching route data: {e}")
        distance_meters = None

    if distance_meters:
        return distance_meters/1000
    else:
        return -1
