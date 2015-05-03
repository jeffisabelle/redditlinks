import uuid
from datetime import datetime

import pytz

from subs.models import RedditLink, Subreddit
from members.models import Member


def create_redditlink(subreddit=None, parsed_at=None):
    """

    Arguments:
    - `subreddit`:
    - `parsed_at`:
    """
    if not subreddit:
        item, created = Subreddit.objects.get_or_create(title='test_sub1')
        subreddit = item

    if not parsed_at:
        d = datetime.now(pytz.utc)
        parsed_at = d

    comments_permalink = uuid.uuid4()

    options = {
        'subreddit': subreddit,
        'parsed_at': parsed_at,
        'comments_permalink': comments_permalink}

    rl = RedditLink.objects.create(**options)
    rl.parsed_at = parsed_at
    rl.save()
    return True


def create_member(**kwargs):
    member = {
        'email': 'test@test.com',
        'timezone': 'Europe/Istanbul',
        'is_active': True,
        'rate': 'd',
    }

    for key, value in kwargs.iteritems():
        if key in member.keys():
            member[key] = value

    Member.objects.create(**member)


def create_members_different_timezones(zones=None):
    """create users for every timezone"""
    if not zones:
        zones = [
            'Europe/London', 'Europe/Berlin', 'Europe/Madrid',
            'Europe/Istanbul', 'America/New_York', 'America/Los_Angeles',
            'UTC',
        ]

    for zone in zones:
        create_member(timezone=zone)
