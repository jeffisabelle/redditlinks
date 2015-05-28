import traceback
import requests
import json
import time
import logging

from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from django.utils import timezone

from subs.models import Subreddit, RedditLink

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    args = '<subreddit1 subreddit2 ...>'
    help = 'Closes the specified poll for voting'

    BASE = "https://www.reddit.com"
    LIST = "/top/"
    FORMAT = ".json"
    AGENT = "User-Agent: redditlinks:v0.1 (by /u/jeffisabelle)"

    def _create_parse_url(self, subreddit):
        return "%s%s%s%s" % (self.BASE, subreddit, self.LIST, self.FORMAT)

    def _parse_links(self):
        subs = Subreddit.objects.all()
        parsed_at = timezone.now()
        for subreddit in subs:
            print subreddit.title
            try:
                logger.debug('Parsing Now: [%s]', subreddit.title)
                headers = {'User-Agent': self.AGENT}
                url = self._create_parse_url(subreddit)

                r = requests.get(url, headers=headers)
                response = json.loads(r.text)
                response = response["data"]["children"]

                for item in response[:10]:
                    item = item["data"]
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

                        obj.parsed_at = parsed_at
                        obj.save()
                    except IntegrityError as e:
                        logger.error(
                            'Error While Saving Parsed Links: %s - %s',
                            subreddit.title, e)
                        print traceback.format_exc()
                time.sleep(2)
            except Exception as e:
                logger.error('Error While Iterating for Parsing: %s', e)
                # todo, check rate-limits
                pass

    def handle(self, *args, **options):
        rate = 'daily' if len(args) == 0 else args[0]
        if rate == 'daily':
            self._parse_links()
