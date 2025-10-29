#!/usr/bin/python3
"""
Module that contains a recursive function that queries the Reddit API,
parse hot article titles, and print a sorted count of given keywords.
"""
import requests


def count_words(subreddit, word_list, word_count=None, after=None):

    if word_count is None:
        word_count = {}
        for word in word_list:
            word_lower = word.lower()
            word_count[word_lower] = word_count.get(word_lower, 0)

    if subreddit is None or not isinstance(subreddit, str):
        return

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {"User-Agent": "RedditKeywordCounter/1.0"}
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
            return

        data = response.json()
        posts_data = data.get("data", {})
        children = posts_data.get("children", [])

        if not children:
            if after is None:
                return
            print_results(word_count)
            return

        for child in children:
            title = child.get("data", {}).get("title", "")
            title_words = title.lower().split()

            for word in title_words:
                if word in word_count:
                    word_count[word] += 1

        after_token = posts_data.get("after")

        if after_token:
            count_words(subreddit, word_list, word_count, after_token)
        else:
            print_results(word_count)

    except Exception:
        return


def print_results(word_count):
    """
    Prints the word count results in descending order by count,
    then alphabetically for words with the same count.

    Args:
        word_count (dict): Dictionary of word counts
    """
    filtered_counts = {word: count for word, count in word_count.items()
                       if count > 0}

    if not filtered_counts:
        return

    sorted_words = sorted(filtered_counts.items(),
                          key=lambda x: (-x[1], x[0]))

    for word, count in sorted_words:
        print("{}: {}".format(word, count))
