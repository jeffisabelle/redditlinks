# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='redditlink',
            name='comments_permalink',
            field=models.URLField(unique=True, max_length=500),
            preserve_default=True,
        ),
    ]
