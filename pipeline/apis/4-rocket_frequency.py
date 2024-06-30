#!/usr/bin/env python3
"""
Script that displays the number of launches per rocket using the SpaceX API.
"""

import requests
from collections import Counter


def get_launch_count_by_rocket():
    """
    Fetches launch and rocket data from SpaceX API, counts the number of launches per rocket,
    and displays the results sorted by the number of launches in descending order.
    If multiple rockets have the same amount of launches, they are sorted alphabetically.
    """
    launches_url = "https://api.spacexdata.com/v4/launches"
    rockets_url = "https://api.spacexdata.com/v4/rockets"

    launches_response = requests.get(launches_url)
    rockets_response = requests.get(rockets_url)

    if (launches_response.status_code != 200 or
            rockets_response.status_code != 200):
        print("Failed to fetch data from SpaceX API")
        return []

    launches = launches_response.json()
    rockets = rockets_response.json()

    rocket_id_to_name = {
        rocket['id']: rocket['name']
        for rocket in rockets
    }
    rocket_launch_counts = Counter(
        launch['rocket']
        for launch in launches
    )

    rocket_launch_counts_sorted = sorted(
        (
            (rocket_id_to_name[rocket_id], count)
            for rocket_id, count in rocket_launch_counts.items()
        ),
        key=lambda x: (-x[1], x[0])
    )

    return rocket_launch_counts_sorted


if __name__ == "__main__":
    rocket_launch_counts = get_launch_count_by_rocket()
    for rocket_name, count in rocket_launch_counts:
        print("{}: {}".format(rocket_name, count))
