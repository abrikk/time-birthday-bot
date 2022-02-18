from datetime import datetime, date


def newyear_time():
    NEWYEAR = datetime(year=date.today().year, month=12, day=31, hour=23,
                       minute=59, second=59, microsecond=999999)
    today = datetime.today()
    days_left = NEWYEAR - today
    hours_left = NEWYEAR.hour - today.hour
    minutes_left = NEWYEAR.minute - today.minute
    seconds_left = NEWYEAR.second - today.second

    return days_left.days, hours_left, minutes_left, seconds_left
