from datetime import datetime

import pytz
from django.test import TestCase

from libs import timelib
from libs.tests.helpers import create_redditlink
from subs.models import RedditLink


class RedditLinkTests(TestCase):
    def test_daily_links_manager(self):
        now = datetime.now(pytz.utc)
        parsing_filter = (now.year, now.month, now.day, 05, 30, 00)
        parsing_time = datetime(*parsing_filter, tzinfo=pytz.utc)

        for _ in range(5):
            create_redditlink(parsed_at=parsing_time)

        for hour in range(0, 24):
            """
            for every utc hours, change the current time
            to the `other` timezones. Filter RedditLink objects
            with the `other` timezones. And see if there is 5 links.
            """
            now = datetime.now(pytz.utc)
            utc_time = datetime(now.year, now.month, now.day, hour, 30, 00)
            utc_time = utc_time.replace(tzinfo=pytz.utc)

            zones = [u'America/Los_Angeles',
                     u'Europe/Istanbul',
                     u'America/New_York']

            for zone in zones:
                if zone in timelib.morning_zones(utc_time, zones):
                    z = pytz.timezone(zone)
                    new_time = utc_time.astimezone(z)

                    qs_filter = {'parsed_at__year': new_time.year,
                                 'parsed_at__month': new_time.month,
                                 'parsed_at__day': new_time.day}
                    qs = RedditLink.objects.filter(**qs_filter)
                    print 'zone: ', zone
                    print utc_time, '- utc date'
                    print new_time, '- zoned date: '
                    print '========================='
                    self.assertEqual(qs.count(), 5)
