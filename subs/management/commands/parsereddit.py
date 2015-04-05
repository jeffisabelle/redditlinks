from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

import traceback
import requests
import json
import pprint
import time

from subs.models import Subreddit, RedditLink
from subs.signals import parsing_done


class Command(BaseCommand):
    args = '<subreddit1 subreddit2 ...>'
    help = 'Closes the specified poll for voting'

    BASE = "https://www.reddit.com"
    LIST = "/top/"
    FORMAT = ".json"
    AGENT = "User-Agent: redditlinks:v0.1 (by /u/jeffisabelle)"
    PP = pprint.PrettyPrinter(indent=4)

    def _create_parse_url(self, subreddit):
        return "%s%s%s%s" % (self.BASE, subreddit, self.LIST, self.FORMAT)

    def handle(self, *args, **options):

        subs = Subreddit.objects.all()
        for subreddit in subs:
            print subreddit.title

            headers = {'User-Agent': self.AGENT}
            url = self._create_parse_url(subreddit)

            r = requests.get(url, headers=headers)
            response = json.loads(r.text)
            response = response["data"]["children"]

            for item in response[:10]:
                item = item["data"]
                # self.PP.pprint(item)

                permalink = self.BASE + item["permalink"]
                try:
                    obj, created = RedditLink.objects.get_or_create(
                        comments_permalink=permalink, subreddit=subreddit)

                    if created:
                        obj.title = item["title"]
                        obj.url = item["url"]
                        obj.domain = item["domain"]
                        obj.score = item["score"]
                        obj.comments_count = item['num_comments']
                        obj.author = item['author']
                    else:
                        obj.comments_count = item['num_comments']
                        obj.score = item["score"]
                    obj.save()
                except IntegrityError:
                    print traceback.format_exc()

            time.sleep(1)

        parsing_done.send(sender=self.__class__)
