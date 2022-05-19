from datetime import datetime

from dateutil.relativedelta import relativedelta

from tgbot.functions.next_holiday_func import get_proper_date
from tgbot.middlewares.lang_middleware import _


def get_current_page(current_page: int, total_pages: int) -> int:
    if current_page > total_pages:
        current_page = abs(total_pages - current_page)
    elif current_page < 1:
        current_page = total_pages - abs(current_page)
    return current_page


async def holiday_days_left(holiday_uid: str, db_commands, morph, lang: str = None) -> tuple:
    holiday = await db_commands.get_scpecific_holiday(holiday_uid)
    today = datetime.today()
    holiday_date = get_proper_date(holiday[1].month, holiday[1].day)
    if lang == 'ru':
        word_list = []
        for word in holiday[0].split():
            conj_word = morph.parse(word)[0]
            if all(ltr in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя' for ltr in word.lower()) and \
                    conj_word.tag.POS not in {'PREP', 'CONJ', 'PRCL', 'INTJ'}:
                word_list.append(morph.parse(word)[0].inflect({"gent"}).word.capitalize())
            else:
                word_list.append(word)
        holiday_name = " ".join(word_list)
    else:
        holiday_name = holiday[0]

    # holiday_name = " ".join([morph.parse(conjucted_word)[0].inflect({"gent"}).word.capitalize()
    #                          for conjucted_word in holiday[0].split()]) \
    #     if lang == 'ru' else holiday[0]

    time_left = relativedelta(holiday_date, today)
    photo = holiday[2] if holiday[
        2] else 'https://pharem-project.eu/wp-content/themes/consultix/images/no-image-found-360x250.png'
    return holiday_name, holiday_date, time_left, photo


def get_time_left(obj: relativedelta, morph, lang: str = None) -> str:
    text = []
    time_dict = {
        "y": morph.parse("лет")[0] if lang else _("лет"),
        "m": morph.parse("месяц")[0] if lang else _("месяц"),
        "d": morph.parse("день")[0] if lang else _("день"),
        "h": morph.parse("час")[0] if lang else _("час"),
        "min": morph.parse("минута")[0] if lang else _("минута"),
        "s": morph.parse("секунда")[0] if lang else _("секунда"),
    }
    if lang == 'ru':
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
    else:
        if obj.years != 0:
            text.append(f"{obj.years} {time_dict['y']}")
        if obj.months != 0:
            text.append(f"{obj.months} {time_dict['m']}")
        if obj.days != 0:
            text.append(f"{obj.days} {time_dict['d']}")
        if obj.hours != 0:
            text.append(f"{obj.hours} {time_dict['h']}")
        if obj.minutes != 0:
            text.append(f"{obj.minutes} {time_dict['min']}")
    return ", ".join(text)
