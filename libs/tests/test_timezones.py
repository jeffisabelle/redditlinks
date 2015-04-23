import os
import sys

project_folder = "redditlinks"
os.environ['DJANGO_SETTINGS_MODULE'] = 'redditlinks.settings'

if project_folder not in sys.path:
    sys.path.append("/Users/muhammetcan/projects/tahta/django/redditlinks")

"""
Above code is for running tests within emacs.

Tam olarak yapmak istedigim:
* Her saat cron calisacak. (utc-zone set edili)
* Cron management komutunu calistiracak. (send-mails)
* current-time utc yapilip, is_morning fonksiyonuna target zone ile gonderilecek
* is_morning == True olanlar liste olarak donecek.

"""
from datetime import datetime

from django.test import TestCase
import pytz

from libs import timelib


class TimelibTests(TestCase):
    utc = pytz.utc
    ist_morning_as_utc = datetime(2015, 04, 17, 05, 30, 00, tzinfo=utc)
    sf_morning_as_utc = datetime(2015, 04, 17, 15, 30, 00, tzinfo=utc)
    nyc_morning_as_utc = datetime(2015, 04, 17, 12, 30, 00, tzinfo=utc)

    def test_convert_naive_to_utc(self):
        naive_date = datetime.now()
        utc_date = timelib.convert_naive_to_utc(naive_date)
        self.assertTrue(hasattr(utc_date, 'tzinfo'))

    def test_convert_utc_to_zone(self):
        date = self.ist_morning_as_utc
        date = timelib.convert_utc_to_zone(date, 'Europe/Istanbul')
        self.assertEqual('Europe/Istanbul', date.tzinfo.zone)

    def test_is_morning(self):
        date = self.ist_morning_as_utc
        zone = 'Europe/Istanbul'
        self.assertTrue(timelib.is_morning_at_zone(date, zone))

    def test_morning_zones(self):
        date = self.ist_morning_as_utc
        morning_zones = timelib.morning_zones(date)
        self.assertIn('Europe/Istanbul', morning_zones)

    def test_morning_zones_with_zones(self):
        date = self.ist_morning_as_utc
        zones = ['Europe/Istanbul', 'Turkey', 'Europe/Berlin']
        morning_zones = timelib.morning_zones(date, zones)
        self.assertIn('Europe/Istanbul', morning_zones)
        self.assertIn('Turkey', morning_zones)
        self.assertNotIn('Europe/Berlin', morning_zones)