#!/usr/bin/env python3
"""
Script that displays the number of launches per rocket using the SpaceX API.
"""

import requests
from collections import defaultdict

def get_rocket_launches():
    """
    Fetches all launches from the SpaceX API and counts launches per rocket.
    """
    url = "https://api.spacexdata.com/v5/launches"
    try:
        response = requests.get(url)
        response.raise_for_status()
        launches = response.json()
        
        rocket_counts = defaultdict(int)
        for launch in launches:
            rocket_id = launch.get('rocket')
            if rocket_id:
                rocket_counts[rocket_id] += 1
        
        return rocket_counts
    except requests.RequestException as e:
        print(f"Error fetching launch data: {e}")
        return {}

def get_rocket_names():
    """
    Fetches all rocket names from the SpaceX API.
    """
    url = "https://api.spacexdata.com/v4/rockets"
    try:
        response = requests.get(url)
        response.raise_for_status()
        rockets = response.json()
        
        return {rocket['id']: rocket['name'] for rocket in rockets}
    except requests.RequestException as e:
        print(f"Error fetching rocket data: {e}")
        return {}

def main():
    rocket_counts = get_rocket_launches()
    rocket_names = get_rocket_names()

    # Combine rocket names with their launch counts
    rocket_launch_counts = {
        rocket_names.get(rocket_id, "Unknown Rocket"): count
        for rocket_id, count in rocket_counts.items()
    }

    # Sort rockets by launch count (descending) and then by name
    sorted_rockets = sorted(
        rocket_launch_counts.items(),
        key=lambda x: (-x[1], x[0])
    )

    # Print results
    for rocket_name, count in sorted_rockets:
        print(f"{rocket_name}: {count}")

if __name__ == '__main__':
    main()