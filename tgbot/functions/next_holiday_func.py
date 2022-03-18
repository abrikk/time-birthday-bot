from datetime import datetime

from tgbot.middlewares.lang_middleware import _

date_today: datetime = datetime.today()


def get_proper_date(month: int, day: int) -> datetime:
    proper_date = datetime(year=datetime.today().year, month=month, day=day)
    if date_today > proper_date:
        proper_date = proper_date.replace(year=datetime.today().year + 1)
    return proper_date


def get_next_holiday() -> dict:
    """
    This function will return the next holiday
    """

    holidays = {
        # New Year, January 1
        get_proper_date(month=1, day=1): _("Новый Год"),
        # International Women's Day, March 8
        get_proper_date(month=3, day=8): _("Международный женский день"),
    }

    next_holiday_name = holidays.get(min(holidays.keys()))
    next_holiday_date = min(holidays.keys())
    next_holiday_dict = {
        'name': next_holiday_name,
        'date': next_holiday_date,
        'left': (next_holiday_date - date_today).days
    }
    return next_holiday_dict
