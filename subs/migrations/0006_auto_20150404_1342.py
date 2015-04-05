# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subs', '0005_auto_20150403_1257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='redditlink',
            name='author',
            field=models.CharField(max_length=200, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='redditlink',
            name='comments_count',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='redditlink',
            name='domain',
            field=models.CharField(max_length=200, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='redditlink',
            name='score',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='redditlink',
            name='title',
            field=models.CharField(max_length=500, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='redditlink',
            name='url',
            field=models.URLField(max_length=500, null=True),
            preserve_default=True,
        ),
    ]
