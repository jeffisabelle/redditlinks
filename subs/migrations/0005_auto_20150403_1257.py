# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subs', '0004_auto_20150329_1724'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='redditlink',
            options={'ordering': ['-score']},
        ),
    ]
