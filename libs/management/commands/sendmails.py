from datetime import datetime

from django.core.management.base import BaseCommand
import pytz

from members.models import Member
from libs.timelib import morning_zones
from libs.maillib import MailLib


class Command(BaseCommand):
    def get_morning_zones(self):
        utc_now = datetime.now(pytz.utc)
        return morning_zones(utc_now)

    def get_members(self, zones):
        return Member.objects.filter(is_active=True, timezone__in=zones)

    def handle(self, *args, **options):
        """
        - get current time
        - convert it to utc
        - check where in the world is at morning
        - filter users based on timezone
        - send mails
        """
        print('sending emails..')

        morning_zones = self.get_morning_zones()
        members = self.get_members(morning_zones)

        ml = MailLib()
        for member in members:
            print('sending mail to: %s' % member)
            ml.process(member)

        print('done..')
        return 'mails-sent'
