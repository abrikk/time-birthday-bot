from datetime import datetime, date

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from dateutil.parser import parse, ParserError

from tgbot.keyboards.reply import back_keyb, additional_keyb
from tgbot.middlewares.lang_middleware import _, __


async def days_left(message: types.Message, state: FSMContext):
    await message.answer(_("Отправьте дату, чтобы узнать разницу между текущей датой "
                           "и датой отправленной вами (например 10.12.2077 или 28.06.1971):"), reply_markup=back_keyb())

    await state.set_state("hmd")


async def days_left_before_the_date(message: types.Message, state: FSMContext):
    user_date = message.text
    try:
        parsed_user_datetime = parse(user_date)
        parsed_user_date = date(parsed_user_datetime.year, parsed_user_datetime.month,
                                parsed_user_datetime.day)
        today = date.today()

        if parsed_user_date > today:
            difference = parsed_user_date - today
            await message.answer(_("До {parsed_user_date} осталось {difference} дней").format(
                parsed_user_date=parsed_user_date, difference=difference.days),
                reply_markup=additional_keyb())
        elif today > parsed_user_date:
            difference = today - parsed_user_date
            await message.answer(_("С {parsed_user_date} прошло {difference} дней").format(
                parsed_user_date=parsed_user_date, difference=difference.days),
                reply_markup=additional_keyb())

        await state.reset_state()
    except ParserError:
        await message.answer(_("Введите корректно дату."))


def register_hmd(dp: Dispatcher):
    dp.register_message_handler(days_left, Command("howmanydays") | Text(equals=__("⏳ Сколько дней")))
    dp.register_message_handler(days_left_before_the_date, state="hmd")
