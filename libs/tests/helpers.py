import random
import uuid
from datetime import datetime

import pytz

from subs.models import RedditLink, Subreddit


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

    RedditLink.objects.create(**options)
    return True
