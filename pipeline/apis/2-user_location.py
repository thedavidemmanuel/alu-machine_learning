#!/usr/bin/env python3
"""
Script to print the location of a specific GitHub user using the GitHub API.
"""

import sys
import requests
from datetime import datetime


def get_user_location(api_url):
    """
    Fetch and print the location of a GitHub user.

    Args:
        api_url (str): The full GitHub API URL for the user.

    Returns:
        None
    """
    headers = {
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28'
    }

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        user_data = response.json()
        location = user_data.get('location', 'No location provided')
        print(location)
    elif response.status_code == 404:
        print("Not found")
    elif response.status_code == 403:
        reset_time = int(response.headers.get('X-Ratelimit-Reset', 0))
        current_time = int(datetime.now().timestamp())
        minutes_left = (reset_time - current_time) // 60
        print("Reset in {} min".format(minutes_left))
    else:
        print("An error occurred: Status code {}".format(response.status_code))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: ./2-user_location.py <github_api_user_url>")
        sys.exit(1)

    api_url = sys.argv[1]
    get_user_location(api_url)
