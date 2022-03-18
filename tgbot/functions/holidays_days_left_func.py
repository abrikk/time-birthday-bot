from datetime import date

from aiogram.utils.markdown import hide_link
from dateutil.relativedelta import relativedelta

from tgbot.functions.next_holiday_func import get_proper_date
from tgbot.middlewares.lang_middleware import _


def get_holiday_name(hol_abbr: str) -> str:
    holidays = {
        "ny": _("Новый Год"),
        "iwd": _("Международный женский день"),
        "nvrz": _("Навруз")
    }
    return holidays[hol_abbr]


async def holiday_days_left(holiday_id: str, db_commands, morph) -> tuple:
    holiday = await db_commands.get_scpecific_holiday(holiday_id)
    print(holiday)
    holidays = {
        "ny": _("Новый Год"),  # New Year, January 1
        "iwd": _("Международный женский день"),  # International Women's Day, March 8
        "nvrz": _("Навруз")  # Navruz, March 21
    }
    today = date.today()
    holiday_date = get_proper_date(holiday[0].month, holiday[1].day)
    holiday_name = " ".join([morph.parse(conjucted_word)[0].inflect({"gent"}).word.capitalize()
                             for conjucted_word in holidays[holiday_id].split()])

    time_left = relativedelta(holiday_date, today)
    return holiday_name, holiday_date, time_left, holiday[1]

def get_time_left(obj: relativedelta):
    text = []
    if obj.months != 0:
        text.append(f"{obj.months} ")
    if obj.days != 0:
        text.append(f"{obj.days} ")
    if obj.years != 0:
        text.append(f"{obj.years} {year_conjuction(obj.years, 'word_year')}")
