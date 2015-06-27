# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0005_auto_20150505_0643'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='member_token',
            field=models.UUIDField(default=uuid.uuid4),
        ),
        migrations.AddField(
            model_name='member',
            name='member_uuid',
            field=models.UUIDField(default=uuid.uuid4),
        ),
        migrations.AlterField(
            model_name='member',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]
