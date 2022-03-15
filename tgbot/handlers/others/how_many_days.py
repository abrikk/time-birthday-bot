from datetime import date

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from dateparser import parse as dp_parse

from tgbot.functions.gettext_func import get_region_date_format
from tgbot.keyboards.reply import back_keyb, additional_keyb
from tgbot.middlewares.lang_middleware import _, __


async def days_left(message: types.Message, state: FSMContext, db_commands):
    user = await db_commands.get_user(user_id=message.from_user.id)
    date_1 = date(2077, 12, 10).strftime(get_region_date_format(user.lang_code))
    date_2 = date(1971, 6, 28).strftime(get_region_date_format(user.lang_code))
    await message.answer(_("Отправьте дату, чтобы узнать разницу между текущей датой "
                           "и датой отправленной вами (например {date_1} или {date_2}):")
                         .format(date_1=date_1, date_2=date_2),
                         reply_markup=back_keyb())

    await state.set_state("hmd")


async def days_left_before_the_date(message: types.Message, state: FSMContext, db_commands):
    user_date = message.text
    try:
        user = await db_commands.get_user(user_id=message.from_user.id)
        parsed_date = dp_parse(user_date, languages=[user.lang_code],
                               settings={'DATE_ORDER': user.preferred_date_order}).date()
        # parsed_user_date = parse(user_date).date()
        today = date.today()

        if parsed_date > today:
            difference = parsed_date - today
            await message.answer(_("До {parsed_user_date} осталось {difference} дней").format(
                parsed_user_date=parsed_date.strftime(get_region_date_format(user.lang_code)),
                difference=difference.days),
                reply_markup=additional_keyb())
        elif today > parsed_date:
            difference = today - parsed_date
            await message.answer(_("С {parsed_user_date} прошло {difference} дней").format(
                parsed_user_date=parsed_date.strftime(get_region_date_format(user.lang_code)),
                difference=difference.days),
                reply_markup=additional_keyb())
        else:
            raise AttributeError

        await state.reset_state()
    except AttributeError:
        await message.answer(_("Введите корректно дату."))


def register_hmd(dp: Dispatcher):
    dp.register_message_handler(days_left, Command("howmanydays") | Text(equals=__("⏳ Сколько дней")))
    dp.register_message_handler(days_left_before_the_date, state="hmd")
