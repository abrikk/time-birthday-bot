from datetime import datetime, date

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.utils.markdown import hitalic
from dateutil.parser import parse, ParserError

from tgbot.keyboards.reply import choose_dy_keyb
from tgbot.middlewares.lang_middleware import _, __


async def day_num_year(message: types.Message):
    await message.answer(_("Выберите в какой день хотите узнать порядковый номер дня в году:"),
                         reply_markup=choose_dy_keyb())


async def dy_chossing(message: types.Message, state: FSMContext):
    if message.text == __("Текущая дата"):
        yearday = datetime.now().timetuple().tm_yday
        await message.answer(_("Сегодня {yearday} день года. 🙇‍♂").format(yearday=yearday))
    else:
        await message.answer(_("Введите дату."))
        await state.set_state("enter_date_dy")


async def entering_date_dy(message: types.Message, state: FSMContext):
    date_text = message.text
    try:
        parsed_date = parse(date_text, dayfirst=True)
        date_only = date(parsed_date.year, parsed_date.month, parsed_date.day)
        yearday = parsed_date.timetuple().tm_yday
        await message.answer(_("{date_only} - это {yearday} день года. 🙇‍♂").format(
            date_only=hitalic(date_only), yearday=yearday))
        await state.reset_state()
    except ParserError:
        await message.answer(_("Вы некорректно ввели дату. Попробуйте еще раз"))


def register_day_num_year(dp: Dispatcher):
    dp.register_message_handler(day_num_year, Command("day_of_year") | Text(contains=__("🔢 Номер дня в году")))
    dp.register_message_handler(dy_chossing, Text(contains=__("Текущая дата")) | Text(contains=__("Конкретная дата")))
    dp.register_message_handler(entering_date_dy, state="enter_date_dy")
