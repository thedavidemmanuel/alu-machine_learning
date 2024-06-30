#!/usr/bin/env python3
"""
This script prints the location of a specific GitHub user.
"""

import sys
import requests
from datetime import datetime, timezone

def get_user_location(api_url):
    """
    Retrieve and print the location of a specific GitHub user.

    Args:
        api_url (str): The API URL of the user.

    Returns:
        None
    """
    try:
        response = requests.get(api_url)

        if response.status_code == 200:
            user_data = response.json()
            location = user_data.get("location", "Location not specified")
            print(location)
        elif response.status_code == 404:
            print("Not found")
        elif response.status_code == 403:
            reset_time = int(response.headers.get("X-RateLimit-Reset", 0))
            reset_time = datetime.fromtimestamp(reset_time, timezone.utc)
            current_time = datetime.now(timezone.utc)
            reset_in = (reset_time - current_time).total_seconds() / 60
            print(f"Reset in {int(reset_in)} min")
        else:
            print("An error occurred")
    except requests.RequestException as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: ./2-user_location.py <GitHub user API URL>")
        sys.exit(1)

    api_url = sys.argv[1]
    get_user_location(api_url)
