# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subs', '0002_auto_20150217_2121'),
    ]

    operations = [
        migrations.AddField(
            model_name='redditlink',
            name='author',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='redditlink',
            name='comments_count',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='redditlink',
            name='score',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
