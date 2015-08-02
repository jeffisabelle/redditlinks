"""
last parsed subreddit:
49 : /r/flytying/                   2sfbh      Fly Tying

align after according to this and concat the output file
"""

import requests
import json
import time

total_pages = 50
counter = 0
subreddits = []
after = ""

while counter < total_pages:
    url = "https://www.reddit.com/reddits.json?limit=100" + after
    agent = "User-Agent: redditlinks:v0.1 (by /u/jeffisabelle)"

    headers = {'User-Agent': agent}
    r = requests.get(url, headers=headers)
    response = json.loads(r.text)

    for sub in response['data']['children']:
        data = sub['data']
        title, url, sub_id = data['title'], data['url'], data['id']
        subreddits.append(url)
        after = "&after=t5_%s" % sub_id
        print "%-3s: %-30s %-10s %-50s" % (counter, url, sub_id, title[:50])

    counter = counter + 1
    time.sleep(3)


out = open("subreddits.json", "w+")
out.write(json.dumps(subreddits))
