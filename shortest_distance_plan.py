import logging
from typing import Dict, List, Tuple

from constants import CITIES_JSON_LOCATION
from helpers.helpers import convert_json_file_to_dict, get_continent_city_map
from processors.shortest_distance_finder import find_shortest_path


def shortest_distance(source: str) -> Tuple[int, List]:
    """Main handler function to return the shortest travelling plan from source city.

    Args:
        source (str): The source or starting city.

    Returns:
        Tuple[int, List]: The total distance travelled, The List of cities in order to be travelled.
    """
    cities_object: Dict = convert_json_file_to_dict(CITIES_JSON_LOCATION)
    continent_city_map: Dict = get_continent_city_map(cities_object)
    total_distance, path = 0, []
    try:
        total_distance, path = find_shortest_path(source, cities_object, continent_city_map)
    except Exception as e:
        logging.error(f"Failed to find the shortest path: {e}")

    return total_distance, path


user_input_city = input("Enter the city to travel from: ")
total_distance, path = shortest_distance(user_input_city.upper())
print(f"Cities in order to travel: {path}")
print(f"Total Distance to be travelled: {total_distance} KMs")
