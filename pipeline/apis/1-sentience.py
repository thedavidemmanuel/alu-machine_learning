#!/usr/bin/env python3
"""
This module provides a function to get the list of home planets of all sentient species.
"""

import requests


def sentientPlanets():
    """
    Retrieve a list of names of the home planets of all sentient species.

    Returns:
        list: A list of planet names that are home to sentient species.
    """
    species_url = "https://swapi-api.alx-tools.com/api/species/"
    planets = set()

    while species_url:
        response = requests.get(species_url)
        data = response.json()

        for species in data["results"]:
            if species["classification"] in ["sentient", "reptilian", "mammal"]:  # Adjust as per SWAPI data structure
                homeworld = species["homeworld"]
                if homeworld:
                    planet_response = requests.get(homeworld)
                    planet_data = planet_response.json()
                    planets.add(planet_data["name"])

        species_url = data["next"]

    return list(planets)


if __name__ == "__main__":
    planets = sentientPlanets()
    for planet in planets:
        print(planet)
