from datetime import datetime

from dateutil.relativedelta import relativedelta

from tgbot.functions.next_holiday_func import get_proper_date
from tgbot.middlewares.lang_middleware import _


async def holiday_days_left(holiday_uid: str, db_commands, morph) -> tuple:
    holiday = await db_commands.get_scpecific_holiday(holiday_uid)
    today = datetime.today()
    holiday_date = get_proper_date(holiday[1].month, holiday[1].day)
    holiday_name = holiday[0]
    # holiday_name = " ".join([morph.parse(conjucted_word)[0].inflect({"gent"}).word.capitalize()
    #                          for conjucted_word in holidays[holiday_id].split()])

    time_left = relativedelta(holiday_date, today)
    return holiday_name, holiday_date, time_left, holiday[2]


def get_time_left(obj: relativedelta, morph) -> str:
    time_dict = {
        "y": morph.parse(_("лет"))[0],
        "m": morph.parse(_("месяц"))[0],
        "d": morph.parse(_("день"))[0],
        "h": morph.parse(_("час"))[0],
        "min": morph.parse(_("минута"))[0],
        "s": morph.parse(_("секунда"))[0],
    }
    text = []
    if obj.years != 0:
        text.append(f"{obj.years} {time_dict['y'].make_agree_with_number(obj.years).word}")
    if obj.months != 0:
        text.append(f"{obj.months} {time_dict['m'].make_agree_with_number(obj.months).word}")
    if obj.days != 0:
        text.append(f"{obj.days} {time_dict['d'].make_agree_with_number(obj.days).word}")
    if obj.hours != 0:
        text.append(f"{obj.hours} {time_dict['h'].make_agree_with_number(obj.hours).word}")
    if obj.minutes != 0:
        text.append(f"{obj.minutes} {time_dict['min'].make_agree_with_number(obj.minutes).word}")

    return ", ".join(text)
