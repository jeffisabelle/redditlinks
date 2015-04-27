from django.test import TestCase
from django.core.management import call_command
from StringIO import StringIO

from libs.tests.helpers import create_redditlink
from subs.models import RedditLink


class TestMaillib(TestCase):
    def test_sendmail_command(self):
        out = StringIO()
        call_command('sendmails', stdout=out)
        self.assertIn('mails-sent', out.getvalue())
        self.assertIsNotNone(out.getvalue())

    def test_timezones(self):
        for i in range(5):
            create_redditlink()

        redditlinks = RedditLink.objects.all()
        self.assertEqual(len(redditlinks), 5)
