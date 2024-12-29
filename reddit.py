import json
import os
from pathlib import Path

import requests

from common import poll_scraping_tasks


def create_reddit_scraping_task_using_subreddit(subreddit):
    url = "https://api.brightdata.com/datasets/v3/trigger?dataset_id=gd_lvz8ah06191smkebj4&include_errors=true&type=discover_new&discover_by=subreddit_url"

    payload = json.dumps(
        [{"url": f"https://www.reddit.com/r/{subreddit}/", "sort_by": "Top"}]
    )
    headers = {
        "Authorization": f'Bearer {os.environ.get("BRIGHTDATA_API_KEY")}',
        "Content-Type": "application/json",
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    # {"snapshot_id": "s_m58h54x6bixb4rgx9"}
    return response.json()


def create_reddit_scraping_tasks(subreddit):
    responses = []
    try:
        response = create_reddit_scraping_task_using_subreddit(subreddit)
        responses.append(response)
    except Exception as e:
        print(e)
    return responses


def get_reddit_scraping_tasks(subreddit):
    if os.environ.get("DEV_MODE") == "True":
        cwd = Path(__file__).resolve().parent
        with open(f"{cwd}/mock_data/reddit.json") as f:
            return json.load(f)
    snapshot_ids = [
        task["snapshot_id"] for task in create_reddit_scraping_tasks(subreddit)
    ]
    return poll_scraping_tasks(snapshot_ids)


if __name__ == "__main__":
    subreddits = ["singularity", "LocalLLaMA", "homeautomation"]
    response = get_reddit_scraping_tasks(subreddits[0])
    for post in response:
        url, title, description = post["url"], post["title"], post["description"]
        print("========================================")
        print(f"Title: {title}\n")
        print(f"Description: {description}")
    print(
        f"Total number of posts scraped: {len(response)}"
        if response
        else "No posts scraped"
    )
