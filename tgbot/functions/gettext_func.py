from datetime import date
from statistics import mean
from typing import Union

from aiogram import types
from aiogram.utils.markdown import hcode, quote_html, hbold, hlink
from dateutil import relativedelta

from tgbot.functions.case_conjugation_func import day_conjugation, year_conjuction, left_conjunction
from tgbot.middlewares.lang_middleware import _


def get_profile_text(user) -> str:
    user_date = user.user_bd
    today = date.today()
    age = relativedelta.relativedelta(today, user_date)
    sex = _("Мужской") if user.sex == "1" else _("Женский")

    profile_text = _("Ваш профиль ⚜️\n\n"
                     "ID: {user_id}\n"
                     "Имя: {name}\n"
                     "Дата рождения: {user_date}\n"
                     "Ваш пол: {sex}\n"
                     "Ваш возраст: {years} лет {months} месяцев {days} дней")

    text = profile_text.format(user_id=hcode(user.user_id),
                               name=hbold(quote_html(user.first_name)),
                               user_date=user.user_bd,
                               sex=sex,
                               years=hbold(age.years),
                               months=hbold(age.months),
                               days=hbold(age.days))

    return text


def get_echo_text() -> str:
    echo_text = _("Я могу помочь тебе управлять и работать со временем.\n\n"
                  "/profile - посмотреть свой  профиль\n"
                  "/botinfo - информация о боте\n\n"
                  "{p}\n"
                  "/bday_today - посмотреть у кого сегодня день рождение {b}\n"
                  "/setname - изменить имя\n"
                  "/setdate - изменить дату рождения\n"
                  "/setsex - изменить пол\n\n"
                  "{extra}\n"
                  "/setlanguage - поменять язык бота\n"
                  "/mybd - сколько дней осталось до дня рождения\n"
                  "/newyear - сколько дней осталось нового года\n"
                  "/howmanydays - разница текущей даты с отправленной вами")

    text = echo_text.format(
        p=hbold(_("Изменить профиль")),
        b=hbold(_("[бета]")),
        extra=hbold(_("Дополнительные "
                      "команды")))

    return text


def get_help_text() -> list:
    text = [
        _("🤖 Возможности бота:\n\n"
          "• {my_profile} 📝\n\n"
          "- Зарегистрируйся в профиле нажав по кнопке \n\"<i>Мой профиль 👤</i>\" или отправив команду "
          "/profile, тем самым у тебя появится возможность узнать у кого сегодня день "
          "рождение, а так же поздравить этого человека.").format(my_profile=hbold(_('Мой профиль'))),

        _("🤖 Возможности бота:\n\n"
          "• {second_ability} 🚀\n\n"
          "- Отправь боту свою дату рождения и он пришлет Тебе время твоего существования "
          "(например 22.07.2006).").format(
            second_ability=hbold(_('Вычисление пройденного количества времени с момента '
                                   'вашего дня рождения за считанные секунды'))),

        _("🤖 Возможности бота:\n\n"
          "• {third_ability} ❓\n\n"
          "- Всем интересно сколько дней осталось до дня рождения, но считать дни вручную "
          "слишком долго и не точно. С помощью команды /mybd, Ты сможешь узнать точное "
          "количество дней которое осталось до дня рождения.").format(
            third_ability=hbold(_('Узнай сколько дней осталось до дня рождения'))),

        _("🤖 Возможности бота:\n\n"
          "• {fourth_ability} ❄️\n\n"
          "- По команде /newyear бот отправит оставшееся количество времени до Нового Года с "
          "точностью до минуты!").format(fourth_ability=hbold(_('Узнай сколько дней осталось до '
                                                                'Нового Года'))),

        _("🤖 Возможности бота:\n\n"
          "• {fifth_ability} 📅\n\n"
          "- Если тебе интересно сколько дней прошло после какого-то события или сколько дней осталось"
          " до определенного дня, то отправь команду /howmanydays, затем тебе нужную дату.").format(
            fifth_ability=hbold(_('Нахождение разницы времени отправленной тобой даты с '
                                  'сегодняшним днем')))
    ]

    return text


def get_month_name(number) -> str:
    if number == 1:
        return _("Января")
    elif number == 2:
        return _("Февраля")
    elif number == 3:
        return _("Марта")
    elif number == 4:
        return _("Апреля")
    elif number == 5:
        return _("Мая")
    elif number == 6:
        return _("Июня")
    elif number == 7:
        return _("Июля")
    elif number == 8:
        return _("Августа")
    elif number == 9:
        return _("Сентября")
    elif number == 10:
        return _("Октября")
    elif number == 11:
        return _("Ноября")
    elif number == 12:
        return _("Декабря")


def get_weekday_name(number_or_date: Union[int, date]) -> str:
    if isinstance(number_or_date, int):
        number = number_or_date
    elif isinstance(number_or_date, date):
        number = number_or_date.isoweekday()

    if number == 1:
        return _("понедельник")
    elif number == 2:
        return _("вторник")
    elif number == 3:
        return _("среда")
    elif number == 4:
        return _("четверг")
    elif number == 5:
        return _("пятница")
    elif number == 6:
        return _("суббота")
    elif number == 7:
        return _("воскресенье")


async def get_botinfo_text(message: types, db_commands) -> str:
    ratings = await db_commands.get_all_ratings()
    average_rate = round(mean(ratings), 1) if ratings else 0

    bot_user = await message.bot.me
    bot_info = await db_commands.get_bot_info(bot_user.username)

    updated_date = bot_info.updated_on
    updated_month = get_month_name(updated_date.month)
    updated_day = updated_date.day
    updated_year = updated_date.year
    updated = f"{updated_day} {updated_month} {updated_year}"

    text = _("ℹ Об этом {bot}:\n\n"
             "• Рейтинг бота: <b>{rate} \u2605</b>\n"
             "• Количество отзывов: {num_reviews}\n"
             "• Языки: Русский и еще {lang}\n"
             "• Бета-версия {version}\n"
             "• Обновлено {updated} года\n"
             "• Выпущено 9 Января 2022 года\n"
             "• Создано 25 Декабря 2021 года\n\n"
             "👨‍💻 Разработчик @JustAbrik").format(bot=hlink(_('боте'), url=f't.me/{bot_user.username}'),
                                                    version=hcode(bot_info.version),
                                                    rate=average_rate,
                                                    num_reviews=len(ratings),
                                                    lang=bot_info.languages,
                                                    updated=updated)

    return text


def until_bd(message: types.Message, days_left: int, age: int) -> str:
    day = day_conjugation(days_left)
    left = left_conjunction(days_left)
    if days_left != 0:
        text = _("До вашего дня рождения {left}: {days_left} {day} 💫").format(
            days_left=days_left, day=day, left=left)
    else:
        turned_year = year_conjuction(age)
        message.answer("🎊")
        text = (_("Ура! У Вас сегодня день рождение.\n"
                  "Вам исполнилось {age} {year} 🥳").format(age=age, year=turned_year))
    return text
