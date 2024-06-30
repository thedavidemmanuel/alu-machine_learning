#!/usr/bin/env python3
"""
Script that displays the number of launches per rocket using the SpaceX API.
"""

import requests


def main():
    """
    Fetches and displays the number of launches per rocket.
    Orders the results by the number of launches (descending) and alphabetically.
    """
    rockets_url = "https://api.spacexdata.com/v4/rockets"
    launches_url = "https://api.spacexdata.com/v4/launches"

    rockets_response = requests.get(rockets_url)
    launches_response = requests.get(launches_url)

    if rockets_response.status_code != 200 or launches_response.status_code != 200:
        print("Failed to fetch data from SpaceX API")
        return

    rockets = rockets_response.json()
    launches = launches_response.json()

    rocket_launch_counts = {}

    for launch in launches:
        rocket_id = launch['rocket']
        if rocket_id in rocket_launch_counts:
            rocket_launch_counts[rocket_id] += 1
        else:
            rocket_launch_counts[rocket_id] = 1

    rocket_names = {rocket['id']: rocket['name'] for rocket in rockets}

    launch_counts = [(rocket_names[rocket_id], count) for rocket_id, count in rocket_launch_counts.items()]

    sorted_launch_counts = sorted(launch_counts, key=lambda x: (-x[1], x[0]))

    for rocket_name, count in sorted_launch_counts:
        print(f"{rocket_name}: {count}")


if __name__ == "__main__":
    main()

