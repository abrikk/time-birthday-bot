from datetime import date

from tgbot.functions.next_holiday_func import get_proper_date
from tgbot.middlewares.lang_middleware import _


def holiday_days_left(holiday: str) -> tuple:
    # holidays_dates = {
    #     1: get_proper_date(month=1, day=1),  # New Year, January 1
    #     2: get_proper_date(month=3, day=8),  # International Women's Day, March 8
    #     3: get_proper_date(month=3, day=21)  # Navruz, March 21
    # }
    holidays = {
        "ny": (_("Новый Год"), _("Нового Года"), get_proper_date(month=1, day=1)),  # New Year, January 1
        "iwd": (_("Международный женский день"), _("Международного женского дня"),  # International Women's Day, March 8
                get_proper_date(month=3, day=8)),
        "navruz": (_("Навруз"), _("праздника Навруз"), get_proper_date(month=3, day=8))  # Navruz, March 21
    }
    today = date.today()
    holiday_name, holiday_namec, holiday_date = holidays[holiday]

    days_left = (holiday_date - today).days
    return holiday_name, holiday_namec, holiday_date, days_left
