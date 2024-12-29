import os
import time

import requests


def poll_scraping_tasks(snapshot_ids):
    all_tasks = [None] * len(snapshot_ids)

    while any([task is None for task in all_tasks]):
        for i, snapshot_id in enumerate(snapshot_ids):
            if all_tasks[i] is None:
                print(f"Polling task {snapshot_id}")
                url = f"https://api.brightdata.com/datasets/v3/snapshot/{snapshot_id}?format=json"
                headers = {
                    "Authorization": f'Bearer {os.environ.get("BRIGHTDATA_API_KEY")}'
                }
                response = requests.request("GET", url, headers=headers)
                if response.status_code != 200:
                    # Sleep for 10 seconds as recommended by Bright Data
                    time.sleep(10)
                    continue
                task = response.json()
                all_tasks[i] = task

    return all_tasks
