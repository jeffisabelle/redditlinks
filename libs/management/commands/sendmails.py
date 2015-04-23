from django.core.management.base import BaseCommand

from members.models import Member
from subs.signals import send_mails


class Command(BaseCommand):
    def _get_members(self):
        return Member.objects.filter(is_active=True)

    def handle(self, *args, **options):
        print self._get_members()
