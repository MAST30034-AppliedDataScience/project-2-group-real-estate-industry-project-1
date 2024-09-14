import requests
import time
import re
import numpy as np
import pandas as pd
import json
from geopy.distance import geodesic

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


def find_closest_station(property_coords, train_stations):
    """
    Find the closest train station based on latitude and longitude.
    """
    if not property_coords or property_coords == (0.0, 0.0):
        return 0
    property_lat, property_lon = property_coords
    train_stations['distance'] = train_stations.apply(
        lambda row: geodesic((property_lat, property_lon), (row['stop_lat'], row['stop_lon'])).meters, axis=1
    )
    # Return the closest station row
    closest_station = train_stations.loc[train_stations['distance'].idxmin()]
    return closest_station

def find_closest_hospital(property_coords, hospitals):
    """
    Find the closest hospital based on latitude and longitude.
    """
    if not property_coords or property_coords == (0.0, 0.0):
        return 0
    property_lat, property_lon = property_coords
    hospitals['distance'] = hospitals.apply(
        lambda row: geodesic((property_lat, property_lon), (row['NHSD_LAT'], row['NHSD_LONG'])).meters, axis=1
    )
    # Return the closest hospital row
    closest_hospital = hospitals.loc[hospitals['distance'].idxmin()]
    return closest_hospital

def find_closest_park(property_coords, parks):
    """
    Find the closest park based on latitude and longitude.
    """
    if not property_coords or property_coords == (0.0, 0.0):
        return 0
    property_lat, property_lon = property_coords
    parks['distance'] = parks.apply(
        lambda row: geodesic((property_lat, property_lon), (row['latitude'], row['longitude'])).meters, axis=1
    )
    # Return the closest park row
    closest_park = parks.loc[parks['distance'].idxmin()]
    return closest_park

def parse_elec_coord(point_str):
    # Use regex to extract numbers from the POINT string
    match = re.match(r'POINT \(([^ ]+) ([^ ]+)\)', point_str)
    if match:
        lon = float(match.group(1))
        lat = float(match.group(2))
        return pd.Series([lat, lon])
    else:
        return pd.Series([None, None])
        
def find_closest_elec(property_coords, elec):
    """
    Find the closest elec based on latitude and longitude.
    """
    # as same functionality just different name, call previous
    return find_closest_park(property_coords, elec)

def find_closest_tour(property_coords, tour):
    """
    Find the closest tourist attraction based on latitude and longitude.
    """
    # Same deal
    return find_closest_park(property_coords, tour)

def find_closest_lib(property_coords, lib):
    """
    Find the closest library based on latitude and longitude.
    """
    # Same deal
    return find_closest_park(property_coords, lib)

def find_closest_shop(property_coords, shops):
    """
    Find the closest grocery based on latitude and longitude.
    """
    if not property_coords or property_coords == (0.0, 0.0):
        return 0
    property_lat, property_lon = property_coords
    shops['distance'] = shops.apply(
        lambda row: geodesic((property_lat, property_lon), (row['Latitude'], row['Longitude'])).meters, axis=1
    )
    # Return the closest shop row
    closest_shop = shops.loc[shops['distance'].idxmin()]
    return closest_shop