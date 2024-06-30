#!/usr/bin/env python3
"""
Script that displays the number of launches per rocket using the SpaceX API.
"""

import requests
from collections import defaultdict
import sys

def get_rocket_launches():
    """
    Fetches all launches from the SpaceX API and counts launches per rocket.
    """
    url = "https://api.spacexdata.com/v5/launches"
    response = requests.get(url)
    
    if response.status_code != 200:
        print("Failed to fetch data from the API")
        sys.exit(1)

    launches = response.json()
    rocket_counts = defaultdict(int)

    for launch in launches:
        rocket_id = launch['rocket']
        rocket_counts[rocket_id] += 1

    return rocket_counts

def get_rocket_names(rocket_ids):
    """
    Fetches rocket names for given rocket IDs.
    """
    url = "https://api.spacexdata.com/v4/rockets"
    response = requests.get(url)
    
    if response.status_code != 200:
        print("Failed to fetch rocket data from the API")
        sys.exit(1)

    rockets = response.json()
    rocket_names = {rocket['id']: rocket['name'] for rocket in rockets}

    return {rocket_id: rocket_names.get(rocket_id, "Unknown Rocket") for rocket_id in rocket_ids}

def main():
    rocket_counts = get_rocket_launches()
    rocket_names = get_rocket_names(rocket_counts.keys())

    # Create a list of (name, count) tuples and sort it
    sorted_rockets = sorted(
        [(rocket_names[rocket_id], count) for rocket_id, count in rocket_counts.items()],
        key=lambda x: (-x[1], x[0])  # Sort by count (descending) and then by name
    )

    for rocket_name, count in sorted_rockets:
        print(f"{rocket_name}: {count}")

if __name__ == '__main__':
    main()