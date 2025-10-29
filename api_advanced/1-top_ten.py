#!/usr/bin/python3
"""
Module that contains a function that queries the Reddit API
to print the titles of the first 10 hot posts for a given subreddit.
"""
import requests


def top_ten(subreddit):

    if subreddit is None or not isinstance(subreddit, str):
        print("None")
        return

    url = "https://www.reddit.com/r/{}/hot.json?limit=10".format(subreddit)
    headers = {"User-Agent": "RedditTopTenPostsFetcher/1.0"}

    try:
        response = requests.get(url, headers=headers, allow_redirects=False)

        if response.status_code != 200:
            print("None")
            return

        data = response.json()
        children = data.get("data", {}).get("children", [])

        if not children:
            print("None")
            return

        for child in children:
            title = child.get("data", {}).get("title")
            if title:
                print(title)

    except Exception:
        print("None")
