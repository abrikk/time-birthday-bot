from datetime import date
from pathlib import Path
from statistics import mean
from typing import Union

import toml
from aiogram import types
from aiogram.utils.markdown import hcode, quote_html, hbold, hlink
from dateutil import relativedelta

from tgbot.functions.case_conjugation_func import day_conjugation, year_conjuction, left_conjunction, month_conjuction
from tgbot.functions.newyear_func import newyear_time
from tgbot.middlewares.lang_middleware import _


# START TEXT

def get_start_text(full_name) -> str:
    text = _("Привет, {full_name}!\n\n"
             "Этот бот считает количество прожитых дней с момента твоего "
             "дня рождения. Просто отправь дату рождения (например: 22.07.2006)\n\n"
             "За подробной информацией отправьте команду /help").format(
        full_name=full_name)
    return text


def get_profile_text(user) -> str:
    user_date = user.user_bd
    today = date.today()
    age = relativedelta.relativedelta(today, user_date)
    sex = _("Мужской") if user.sex == "1" else _("Женский")

    text = []
    if age.years != 0:
        text.append(f"{age.years} {year_conjuction(age.years, 'word_year')}")
    if age.months != 0:
        text.append(f"{age.months} {month_conjuction(age.months, 'word_month')}")
    if age.days != 0:
        text.append(f"{age.days} {day_conjugation(age.days, 'word_day')}")

    if len(text) != 0:
        age_text = ", ".join(text)
    else:
        age_text = _("Я родился! 👼")

    profile_text = _("Ваш профиль ⚜️\n\n"
                     "ID: {user_id}\n"
                     "Имя: {name}\n"
                     "Дата рождения: {user_date}\n"
                     "Ваш пол: {sex}\n"
                     "Ваш возраст: {age_text}")

    text = profile_text.format(user_id=hcode(user.user_id),
                               name=hbold(quote_html(user.first_name)),
                               user_date=user.user_bd,
                               sex=sex,
                               age_text=age_text)

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
    month_name = {
        1: _("Января"),
        2: _("Февраля"),
        3: _("Марта"),
        4: _("Апреля"),
        5: _("Мая"),
        6: _("Июня"),
        7: _("Июля"),
        8: _("Августа"),
        9: _("Сентября"),
        10: _("Октября"),
        11: _("Ноября"),
        12: _("Декабря"),
    }
    return month_name[number]


def get_weekday_name(number_or_date: Union[int, date]) -> str:
    weekday = {
        1: _("понедельник"),
        2: _("вторник"),
        3: _("среда"),
        4: _("четверг"),
        5: _("пятница"),
        6: _("суббота"),
        7: _("воскресенье")
    }
    if isinstance(number_or_date, int):
        return weekday[number_or_date]
    elif isinstance(number_or_date, date):
        number = number_or_date.isoweekday()
        return weekday[number]


async def get_botinfo_text(call: Union[types.Message, types.CallbackQuery], db_commands, session) -> str:
    bot_user = await call.bot.me
    bot_info = await db_commands.get_bot_info(bot_user.username)
    data = toml.load(Path("pyproject.toml").absolute())
    if bot_info is None:
        bot_version: str = data["tool"]["poetry"]["VERSION"]
        num_dirs_lang = Path('C:\\Users\\abror\\PycharmProjects\\tbday-project\\locales')
        num_languages = [x for x in num_dirs_lang.iterdir() if x.is_dir()]
        await db_commands.add_bot(
            username=bot_user.username,
            version=bot_version,
            languages=len(num_languages)
        )
        await session.commit()
        bot_info = await db_commands.get_bot_info(bot_user.username)

    ratings = await db_commands.get_all_ratings()
    average_rate = round(mean(ratings), 1) if ratings else 0

    updated_date = bot_info.updated_at
    updated_month = get_month_name(updated_date.month)
    updated_day = updated_date.day
    updated_year = updated_date.year
    updated = f"{updated_day} {updated_month} {updated_year}"

    bot_version: str = data["tool"]["poetry"]["VERSION"]

    text = _("ℹ Об этом {bot}:\n\n"
             "• Рейтинг бота: <b>{rate} \u2605</b>\n"
             "• Количество отзывов: {num_reviews}\n"
             "• Языки: Русский и еще {lang}\n"
             "• Бета-версия {version}\n"
             "• Обновлено {updated} года\n"
             "• Выпущено 9 Января 2022 года\n"
             "• Создано 25 Декабря 2021 года\n\n"
             "👨‍💻 Разработчик @JustAbrik").format(bot=hlink(_('боте'),
                                                              url=f't.me/{bot_user.username}'),
                                                    version=hcode(bot_version),
                                                    rate=average_rate,
                                                    num_reviews=len(ratings),
                                                    lang=bot_info.languages - 1,
                                                    updated=updated)

    return text


async def until_bd(days_left: int, age: int, where: str, message: types.Message = None, user_bd=None) -> str:
    day = day_conjugation(days_left)
    left = left_conjunction(days_left)
    turned_year = year_conjuction(age)
    if where == "btn":
        if days_left != 0:
            text = _("До вашего дня рождения {left}: {days_left} {day} 💫").format(
                days_left=days_left, day=day, left=left)
        else:
            turned_year = year_conjuction(age)
            await message.answer("🎊")
            text = (_("Ура! У Вас сегодня день рождение.\n"
                      "Вам исполнилось {age} {year} 🥳").format(age=age, year=turned_year))
        return text
    elif where == "btn_born_today":
        await message.answer("🎊")
        text = (_("Ух ты! Сегодня Вы впервые появились на свет! 👶🥳"))
        return text
    elif where == "cmnd":
        if days_left != 0:
            text = _("До дня рождения {left}: {days_left} {day} 💫").format(
                days_left=days_left, day=day, left=left)
        else:
            await message.answer("🎊")
            text = (_("Ура! У кого-то сегодня день рождение.\n"
                      "Тебе исполнилось {age} {year} 🥳").format(age=age, year=turned_year))
        return text
    elif where == "title":
        if days_left != 0:
            text = _("До вашего дня рождения {left}: {days_left} {day}").format(
                days_left=days_left, day=day, left=left)
        else:
            if user_bd == date.today():
                text = _("Поздравляем! Вы сегодня родилсь!")
            else:
                text = _("У Вас сегодня день рождение. Вам исполнилось {age} {year}.").format(
                    age=age, year=turned_year)
        return text
    elif where == "inline_text":
        if days_left != 0:
            text = _("До моего дня рождения {left} {days_left} {day} 😏").format(
                days_left=days_left, day=day, left=left)
        else:
            if user_bd == date.today():
                text = _("Я сегодня родился!!! 🥳🥳")
            else:
                text = _("Мне сегодня исполнилось {age} {year}!!! 🥳🥳").format(age=age,
                                                                                year=turned_year)
        return text


def get_newyear_time() -> str:
    days_left, hours_left, minutes_left, seconds_left = newyear_time()

    text = _("До Нового Года осталось {d} дней, {h} "
             "часов, {m} минут и {s} секунд! ☃").format(
        d=hbold(days_left),
        h=hbold(hours_left),
        m=hbold(minutes_left),
        s=hbold(seconds_left))

    return text


async def get_profile_stat_text(user_id, db_commands) -> str:
    user = await db_commands.get_user(user_id)
    created_at = user.created_at.strftime("%Y-%m-%d %H:%M:%S")
    user_received_gratzed = await db_commands.get_user_rcvd_gratzed(user_id)
    user_gratzed = await db_commands.get_user_gratzed(user_id)

    gratzed_text = "".join("- В {year[1]} году: {year[0]}\n".format(year=year)
                           for year in user_gratzed)

    rcvd_gratz_text = "".join("- В {year[1]} году: {year[0]}\n".format(year=year)
                              for year in user_received_gratzed)

    # The number of congratulations sent by the user in a given year
    gratzed = gratzed_text if len(user_gratzed) != 0 else "<i>- Пусто</i>"
    # The number of congratulations that the user received in a certain year
    rcvd_gratz = rcvd_gratz_text if len(user_received_gratzed) != 0 else "<i>- Пусто</i>"

    stat_text = ("📊 Статистика:\n\n"
                 "📤 <b>Отправлено поздравлений</b>:\n"
                 "{gratzed}\n\n"
                 "📥 <b>Получено поздравлений:</b>\n"
                 "{rcvd_gratz}\n\n"
                 "📝 Дата регистрации: {created_at}UTC+0").format(gratzed=gratzed,
                                                                  rcvd_gratz=rcvd_gratz,
                                                                  created_at=created_at)

    return stat_text


def get_available_formats_text(is_day_first: bool) -> str:
    if is_day_first:
        text = _("Бот поддерживает множество форматов дат, а так же все Международные "
                 "форматы даты ISO 8601.\n\n"
                 "Доступные форматы:\n"
                 "Формат - Пример записи даты \"28 июня 2018 года\"\n"
                 "- гггг.дд.мм → 2018.28.06\n"
                 "- д.м.гггг → 28.6.2018\n"
                 "- д-м-гггг → 28-6-2018\n"
                 "- д/м/гггг →  28/6/2018\n"
                 "- дд.мм.гггг → 28.06.2018\n"
                 "- дд-мм-гггг → 28-06-2018\n"
                 "- дд/мм/гггг → 28/06/2018\n"
                 "ISO 8601:\n"
                 "- ггггддмм → 20182806"
                 )

        # text = _("Бот поддерживает множество форматов дат, а так же все Международные "
        #          "форматы даты ISO 8601.\n\n"
        #          "Доступные форматы:\n"
        #          "- гггг.мм.дд → 2018.06.28\n"
        #          "- гггг-мм-дд → 2018-06-28\n"
        #          "- гггг/мм/дд → 2018/06/28\n"
        #          "- гггг-м-д → 2018-6-28\n"
        #          "- гггг/м/д → 2018/6/28\n"
        #          # "- гггг.дд.мм → 2018.28.06\n"
        #          # "- д.м.гггг → 22.6.2018\n"
        #          # "- д-м-гггг → 22-6-2018\n"
        #          # "- д/м/гггг →  22/6/2018\n"
        #          # "- дд.мм.гггг → 28.06.2018\n"
        #          # "- дд-мм-гггг → 28-06-2018\n"
        #          # "- дд/мм/гггг → 28/06/2018\n"
        #          "- м/д/гггг → 28/6/2018\n"
        #          "ISO 8601:\n\n"
        #          "")
    else:
        text = _("Бот поддерживает множество форматов дат, а так же все Международные "
                 "форматы даты ISO 8601.\n\n"
                 "Доступные форматы:\n"
                 "Формат - Пример записи даты \"28 июня 2018 года\"\n"
                 "- гггг.мм.дд → 2018.06.28\n"
                 "- гггг-мм-дд → 2018-06-28\n"
                 "- гггг/мм/дд → 2018/06/28\n"
                 "- гггг-м-д → 2018-6-28\n"
                 "- гггг/м/д → 2018/6/28\n"
                 "- м/д/гггг → 28/6/2018\n")
    return text


async def get_user_turned_day_text(user_id: int, db_commands) -> str:
    user = await db_commands.get_user(user_id)

    today = date.today()
    days = (today - user.user_bd).days

    text = _("Сегодня Вам исполнилось: \n\n"
             "{days} дней\n"
             "или\n"
             "{hours} часов").format(days=days, hours=days * 24)
    return text
