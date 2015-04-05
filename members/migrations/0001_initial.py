# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=75)),
                ('total_subscription', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MemberSubscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('member', models.ForeignKey(to='members.Member')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subreddit', models.CharField(max_length=200)),
                ('count', models.IntegerField(default=5)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='subscription',
            unique_together=set([('subreddit', 'count')]),
        ),
        migrations.AddField(
            model_name='membersubscription',
            name='subscription',
            field=models.ForeignKey(to='members.Subscription'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='subscription',
            field=models.ManyToManyField(to='members.Subscription', through='members.MemberSubscription'),
            preserve_default=True,
        ),
    ]
