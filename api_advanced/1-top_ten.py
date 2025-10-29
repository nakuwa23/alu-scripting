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

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {"User-Agent": "RedditTopTenPostsFetcher/1.0"}
    params = {"limit": 10}

    try:
        response = requests.get(
            url,
            headers=headers,
            params=params,
            allow_redirects=False
        )

        if response.status_code != 200:
            print("None")
            return

        data = response.json()
        posts = data.get("data", {}).get("children", [])

        if not posts:
            print("None")
            return

        for post in posts:
            post_data = post.get("data", {})
            title = post_data.get("title", "")
            print(title)

    except Exception:
        print("None")
