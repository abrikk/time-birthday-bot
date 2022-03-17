from datetime import date

from aiogram.utils.markdown import hide_link

from tgbot.functions.next_holiday_func import get_proper_date
from tgbot.middlewares.lang_middleware import _


def get_holiday_name(hol_abbr: str) -> str:
    holidays = {
        "ny": _("Новый Год"),
        "iwd": _("Международный женский день"),
        "nvrz": _("Навруз")
    }
    return holidays[hol_abbr]


def holiday_days_left(holiday: str) -> tuple:
    holidays = {
        "ny": (_("Новый Год"), _("Нового Года"), get_proper_date(month=1, day=1)),  # New Year, January 1
        "iwd": (_("Международный женский день"), _("Международного женского дня") + hide_link(
            "https://timesofindia.indiatimes.com/thumb/msid-81373950,width-1200,height-900,resizemode-4/.jpg"),
                get_proper_date(month=3, day=8)),  # International Women's Day, March 8
        "nvrz": (_("Навруз"), _("праздника Навруз"), get_proper_date(month=3, day=8))  # Navruz, March 21
    }
    today = date.today()
    holiday_name, holiday_namec, holiday_date = holidays[holiday]

    days_left = (holiday_date - today).days
    return holiday_name, holiday_namec, holiday_date, days_left
