from datetime import date

from tgbot.functions.next_holiday_func import get_proper_date
from tgbot.middlewares.lang_middleware import _, __


def holiday_days_left(holiday: str) -> tuple:
    holidays = {
        __("🌹 Международный женский день"): (get_proper_date(month=3, day=8),
                                              _("Международного женского дня")),
        __("🌱 Навруз"): (get_proper_date(month=3, day=21), _("Навруза"))
    }
    today = date.today()
    holiday_date, holiday_name = holidays[holiday]

    days_left = (holiday_date - today).days
    return holiday_name, days_left

