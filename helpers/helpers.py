from collections import defaultdict
import logging
import math
from typing import Dict

import ujson

from constants import RADIUS_OF_EARTH


def convert_json_file_to_dict(file_location: str) -> Dict:
    """The following function convert the input json file to a python dictionary object.

    Args:
        file_location (str): The .json file location.

    Returns:
        Dict: Python Dictionary object.
    """
    try:
        with open(file_location) as json_file:
            converted_data: Dict = ujson.load(json_file)

    except Exception as e:
        logging.error(f"Failed to convert json to dict, error: {e}")

    return converted_data


def get_continent_city_map(cities_data: Dict) -> Dict:
    """Creates a continent <> list of cities mapping.

    Eg: {
        "asia": ["JRH", "BOM"]
    }

    Args:
        cities_data (Dict): A dictionary of all the cities.

    Returns:
        Dict: The continent and cities map.
    """
    continent_city_map: Dict = defaultdict(list)
    for city in cities_data:
        continent_city_map[cities_data[city]["contId"]].append(city)

    return continent_city_map


def deg_to_rad_conveter(deg: float) -> float:
    """Converts a given degree to radians.

    Args:
        deg (float): The degree to convert.

    Returns:
        float: The converted radian float.
    """
    return deg * (math.pi/180)


def calculate_distance_from_latlon_in_km(
    source_lat: float, source_lon: float, destination_lat: float, destination_lon: float
) -> float:
    """Calculates the distance between two points in kms.

    Args:
        source_lat (float): Latitude of source.
        source_lon (float): Longitude of source.
        destination_lat (float): Latitude of destination.
        destination_lon (float): Longitude of destination.

    Returns:
        float: The total distance in kilometers.
    """
    latitude_difference = deg_to_rad_conveter(destination_lat - source_lat)
    longitutde_difference = deg_to_rad_conveter(destination_lon - source_lon)

    a = (math.sin(latitude_difference/2) ** 2) + \
        (math.cos(deg_to_rad_conveter(source_lat)) * math.cos(deg_to_rad_conveter(destination_lat))) * \
        (math.sin(longitutde_difference/2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance_in_km = RADIUS_OF_EARTH * c

    return distance_in_km
