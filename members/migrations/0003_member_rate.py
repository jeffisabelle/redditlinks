# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_member_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='rate',
            field=models.CharField(default=b'd', max_length=1, null=True, choices=[(b'd', b'Daily'), (b'w', b'Weekly')]),
            preserve_default=True,
        ),
    ]
