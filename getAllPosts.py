import requests
import pandas as pd
from coreUserFollowers import followers_list

def get_posts(actor):
    url = "https://public.api.bsky.app/xrpc/app.bsky.feed.getAuthorFeed"
    cursor = None
    all_posts = [[],[]]

    while True:

        params = {
            "actor": actor,
            "limit": 100,
            "filter": "posts_no_replies",
        }
        if cursor:
            params["cursor"] = cursor

        resp = requests.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()

        for item in data.get("feed", []):
            post = item.get("post", {})
            record = post.get("record", {})
            text = record.get("text", "")
            time = record.get("createdAt", "")

            if text:
                all_posts[0].append(text)
                all_posts[1].append(time)

        cursor = data.get("cursor")
        if not cursor or len(all_posts[0]) > 5000:
            break

    return all_posts

for x in followers_list[3]:
    posts = get_posts(x)
    df = pd.DataFrame(posts).T
    df.columns = ["post", "date"]
    df.to_excel(x + ".xlsx",index=False)
