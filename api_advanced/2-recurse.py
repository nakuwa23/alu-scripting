#!/usr/bin/python3
"""
Module that contains a recursive function that queries the Reddit API
and return a list of all hot article titles for a given subreddit.
"""
import requests


def recurse(subreddit, hot_list=[], after=None):

    if subreddit is None or not isinstance(subreddit, str):
        return None

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {"User-Agent": "RedditRecursiveHotArticlesFetcher/1.0"}
    params = {"limit": 100}

    if after:
        params["after"] = after

    try:
        response = requests.get(
            url,
            headers=headers,
            params=params,
            allow_redirects=False
        )

        if response.status_code != 200:
            return None

        data = response.json()
        posts_data = data.get("data", {})
        children = posts_data.get("children", [])

        if not children:
            if not hot_list:
                return None
            return hot_list

        for child in children:
            title = child.get("data", {}).get("title")
            if title:
                hot_list.append(title)

        after_token = posts_data.get("after")

        if after_token:
            return recurse(subreddit, hot_list, after_token)
        else:
            return hot_list

    except Exception:
        return None