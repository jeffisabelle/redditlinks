# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('subs', '0003_auto_20150218_1953'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='redditlink',
            options={'ordering': ['parsed_at']},
        ),
        migrations.AddField(
            model_name='redditlink',
            name='parsed_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 29, 17, 24, 16, 208739, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
