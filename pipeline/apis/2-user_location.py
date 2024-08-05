#!/usr/bin/env python3
"""
Module to print the location of a specific GitHub user using the GitHub API.
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
        str: The location of the user or an error message.
    """
    headers = {
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28'
    }

    try:
        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            user_data = response.json()
            return user_data.get('location', 'No location provided')
        elif response.status_code == 404:
            return "Not found"
        elif response.status_code == 403:
            reset_time = int(response.headers.get('X-Ratelimit-Reset', 0))
            current_time = int(datetime.now().timestamp())
            minutes_left = (reset_time - current_time) // 60
            return "Reset in {} min".format(minutes_left)
        else:
            return "An error occurred: Status code {}".format(response.status_code)
    except requests.RequestException as e:
        return "An error occurred: {}".format(str(e))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 2-user_location.py <github_api_user_url>")
        sys.exit(1)

    api_url = sys.argv[1]
    result = get_user_location(api_url)
    print(result)