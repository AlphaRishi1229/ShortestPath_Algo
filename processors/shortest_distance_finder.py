from collections import deque
from copy import deepcopy
from math import ceil
from typing import Deque, Dict, List, Tuple

from helpers.helpers import calculate_distance_from_latlon_in_km


def find_shortest_continent_path(source_city: str, cities_data: Dict, continent_city_map: Dict) -> Deque:
    """This function finds the all the shortest path from source continent to other continents.

    Working:
        Creates a list of continents that has to be visited, first the continent of source city will be added,
        now for every continent we will compare the distance of each cities from source city in all continents and
        select the least possible distance from one continent to other.

    Args:
        source_city (str): The city to be travelled from.
        cities_data (Dict): The data of all the cities (includes lat, lon)
        continent_city_map (Dict): The continent city cross map.

    Returns:
        Deque: The list of continents to be traversed in order to be travelled.
        Eg: ['asia', 'africa', 'europe', 'north-america', 'south-america', 'oceania']
        Means: 'asia' -> 'africa' -> 'europe' -> 'north-america' -> 'south-america' -> 'oceania'
    """
    source_continent = cities_data[source_city]["contId"]
    continent_city_map.pop(source_continent)

    continent_list = deque([source_continent])  # Used a queue which will be required when traversing cities.
    temp_city_list = [source_city]

    while continent_city_map:
        shortest_distance = float("inf")
        nearest_continent = ""
        nearest_city = ""
        current_source = cities_data[temp_city_list[-1]]
        for continent in continent_city_map:
            for city in continent_city_map[continent]:
                temp_destination_data = cities_data[city]
                distance = calculate_distance_from_latlon_in_km(
                    current_source["location"]["lat"], current_source["location"]["lon"],
                    temp_destination_data["location"]["lat"], temp_destination_data["location"]["lon"]
                )
                if distance < shortest_distance:
                    shortest_distance = distance
                    nearest_continent = continent
                    nearest_city = continent_city_map[continent][0]

        continent_list.append(nearest_continent)
        temp_city_list.append(nearest_city)

        continent_city_map.pop(nearest_continent)

    return continent_list


def find_shortest_city_path(
    source_city: str, cities_data: Dict, continent_city_map: Dict, continents_path: Deque
) -> Tuple[int, List]:
    """This function finds the shortest path from source city to other cities.

    Working:
        Compares the source city with each destination city to get the shortest path possible,
        and adds the total distance.

    Args:
        source_city (str): The city to be travelled from.
        cities_data (Dict): The data of all the cities (includes lat, lon)
        continent_city_map (Dict): The continent city cross map.
        continents_path (Deque): The continents list in order to be travelled.

    Returns:
        Tuple[int, List]: The total distance travelled, the cities to visit.
    """
    city_list = [source_city]
    final_distance = 0

    while continents_path:
        shortest_distance = float("inf")
        nearest_city = ""
        current_distance = 0
        destination_continent = continents_path.popleft()
        for city in continent_city_map[destination_continent]:
            # Here we compare source city with each destination city to find the shortest path.
            source_city_data = cities_data[city_list[-1]]
            destination_city_data = cities_data[city]
            distance = calculate_distance_from_latlon_in_km(
                source_city_data["location"]["lat"], source_city_data["location"]["lon"],
                destination_city_data["location"]["lat"], destination_city_data["location"]["lon"]
            )
            if distance < shortest_distance:
                shortest_distance = distance
                nearest_city = city
                current_distance = distance

        city_list.append(nearest_city)
        final_distance += current_distance

    return ceil(final_distance), city_list


def find_shortest_path(source_city: str, cities_data: Dict, continent_city_map: Dict) -> Tuple[int, List]:
    """This function returns the shortest route possible from the mentioned source city.

    Args:
        source_city (str): The city to be travelled from.
        cities_data (Dict): All the data related to cities across the world.
        continent_city_map (Dict): The continent and city map.

    Returns:
        Tuple[int, List]: The total distance travelled, the cities to visit.
    """
    # Deepcopying the city map so as to not affect the original map.
    temp_continent_city_map = deepcopy(continent_city_map)
    continents_path: Deque = find_shortest_continent_path(
        source_city, cities_data, temp_continent_city_map
    )
    # Popping the current city, since it is fixed and not required further.
    continents_path.popleft()
    path_distance, city_path = find_shortest_city_path(
        source_city, cities_data, continent_city_map, continents_path
    )
    # Add source city since return back to source.
    city_path.append(source_city)
    # Creating the final city path with city details.
    final_city_map = [
        (city, cities_data[city]["name"], cities_data[city]["contId"]) for city in city_path
    ]

    return path_distance, final_city_map
