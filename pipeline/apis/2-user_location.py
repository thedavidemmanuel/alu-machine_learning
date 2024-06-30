#!/usr/bin/env python3
"""
Script that prints the location of a specific user.
"""

import requests
import time
import sys


def main(url):
    """
    Prints the location of a specific user based on their GitHub API URL.

    Args:
        url (str): The full GitHub API URL for the user.

    If the user doesn't exist, print "Not found".
    If the status code is 403, print "Reset in X min" where X is the number
    of minutes from now and the value of X-RateLimit-Reset.
    """
    try:
        response = requests.get(url)

        if response.status_code == 404:
            print("Not found")
        elif response.status_code == 403:
            reset_timestamp = int(response.headers.get("X-RateLimit-Reset", 0))
            current_timestamp = int(time.time())
            reset_in_minutes = max(0, (reset_timestamp - current_timestamp) // 60)
            print("Reset in {} min".format(reset_in_minutes))
        else:
            location = response.json().get("location")
            print(location if location else "Not available")
    except requests.RequestException:
        print("An error occurred while making the request")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: ./2-user_location.py <GitHub user API URL>")
        sys.exit(1)

    main(sys.argv[1])