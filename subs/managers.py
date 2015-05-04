from django.db import models

from datetime import date, timedelta


class DailyLinks(models.Manager):
    def today_filter(self):
        today = date.today()
        qs_filter = {
            'parsed_at__year': today.year,
            'parsed_at__month': today.month,
            'parsed_at__day': today.day
        }

        return qs_filter

    def get_queryset(self):
        qs_filter = self.today_filter()
        return super(DailyLinks, self).get_queryset().filter(**qs_filter)


class WeeklyLinks(models.Manager):
    def week_filter(self):
        today = date.today()
        last_week = today - timedelta(days=7)

        qs_filter = {'parsed_at__range': [last_week, today]}
        return qs_filter

    def get_queryset(self):
        qs_filter = self.week_filter()
        return super(WeeklyLinks, self).get_queryset().filter(**qs_filter)
