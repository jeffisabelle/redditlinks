import pytz
from datetime import time, datetime


def _set_default_date(date=None):
    return datetime.now(pytz.utc) if not date else date


def convert_naive_to_utc(naive_date):
    return naive_date.replace(tzinfo=pytz.utc)


def convert_utc_to_zone(utc_date, zone):
    zone = pytz.timezone(zone)
    return utc_date.astimezone(zone)


def is_morning_at_zone(utc_date, zone):
    new_date = _set_default_date(utc_date)
    new_date = convert_utc_to_zone(utc_date, zone)
    the_time = new_date.time()

    start = time(8, 0, 0)
    end = time(8, 50, 0)
    return start <= the_time <= end


def morning_zones(utc_date, zones=None):
    new_date = _set_default_date(utc_date)
    zones = pytz.all_timezones if not zones else zones
    return [zone for zone in zones if is_morning_at_zone(new_date, zone)]
