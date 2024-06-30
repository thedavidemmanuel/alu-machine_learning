#!/usr/bin/env python3
"""
Script that displays the number of launches per rocket using the SpaceX API.
"""

import requests

def main():
    launches_url = "https://api.spacexdata.com/v4/launches"
    rockets_url = "https://api.spacexdata.com/v4/rockets"

    launches_response = requests.get(launches_url)
    rockets_response = requests.get(rockets_url)

    if launches_response.status_code != 200 or rockets_response.status_code != 200:
        print("Failed to fetch data from SpaceX API")
        return

    launches = launches_response.json()
    rockets = rockets_response.json()

    rocket_id_to_name = {rocket['id']: rocket['name'] for rocket in rockets}
    rocket_launch_counts = {}

    for launch in launches:
        rocket_id = launch['rocket']
        rocket_name = rocket_id_to_name.get(rocket_id, "Unknown")
        if rocket_name in rocket_launch_counts:
            rocket_launch_counts[rocket_name] += 1
        else:
            rocket_launch_counts[rocket_name] = 1

    sorted_launch_counts = sorted(rocket_launch_counts.items(), key=lambda x: (-x[1], x[0]))

    for rocket_name, count in sorted_launch_counts:
        print("{}: {}".format(rocket_name, count))

if __name__ == "__main__":
    main()
