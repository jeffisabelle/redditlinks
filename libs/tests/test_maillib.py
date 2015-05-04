from datetime import datetime

import pytz
from django.test import TestCase
from django.core.management import call_command
from StringIO import StringIO

from libs import timelib
from libs.tests.helpers import create_members_different_timezones
from members.models import Member


class TestMaillib(TestCase):
    utc = pytz.utc
    ist_morning_as_utc = datetime(2015, 04, 17, 05, 30, 00, tzinfo=utc)
    sf_morning_as_utc = datetime(2015, 04, 17, 15, 30, 00, tzinfo=utc)
    nyc_morning_as_utc = datetime(2015, 04, 17, 12, 30, 00, tzinfo=utc)

    def setUp(self):
        zones = [u'America/Los_Angeles',
                 u'Europe/Istanbul',
                 u'America/New_York']
        create_members_different_timezones(zones)

    def test_sendmail_command(self):
        out = StringIO()
        call_command('sendmails', stdout=out)
        self.assertIn('mails-sent', out.getvalue())
        self.assertIsNotNone(out.getvalue())

    def test_member_morning_timezones(self):
        zones = Member.objects.all().values('timezone').distinct()
        zones = [z['timezone'] for z in zones]

        for hour in range(0, 24):
            utc = pytz.utc
            new_utc_date = datetime(2015, 04, 17, hour, 30, 00, tzinfo=utc)
            morning_zones = timelib.morning_zones(new_utc_date, zones)
            print 'utc: %s - morning zones: %s' % (new_utc_date, morning_zones)

            if 'US/Pacific-new' in morning_zones:
                self.assertEqual(self.sf_morning_as_utc, new_utc_date)
            if 'Europe/Istanbul' in morning_zones:
                self.assertEqual(self.ist_morning_as_utc, new_utc_date)
            if 'US/Michigan' in morning_zones:
                self.assertEqual(self.nyc_morning_as_utc, new_utc_date)
