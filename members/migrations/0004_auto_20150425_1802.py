# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0003_member_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='subscription_type',
            field=models.CharField(default=b'freemium', max_length=10, choices=[(b'freemium', b'Freemium'), (b'premium', b'Premium'), (b'special', b'Special')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='timezone',
            field=models.CharField(max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
    ]
