from datetime import datetime

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.markdown import hitalic
from dateparser import parse as dp_parse

from tgbot.functions.gettext_func import get_region_date_format
from tgbot.middlewares.lang_middleware import _, __


def choose_dy_keyb():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    buttons = [[_('Текущая дата'), _('Конкретная дата')]]
    for text_1, text_2 in buttons:
        markup.add(KeyboardButton(text_1),
                   KeyboardButton(text_2))
    markup.add(KeyboardButton(text=_("↪️ Назад")))
    return markup


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


async def entering_date_dy(message: types.Message, state: FSMContext, db_commands):
    date_text = message.text
    try:
        user = await db_commands.get_user(user_id=message.from_user.id)
        parsed_date = dp_parse(date_text, languages=[user.lang_code],
                               settings={'DATE_ORDER': user.preferred_date_order}).date()
        yearday = parsed_date.timetuple().tm_yday
        await message.answer(_("{date_only} - это {yearday} день года. 🙇‍♂").format(
            date_only=hitalic(parsed_date.strftime(get_region_date_format(user.lang_code))),
            yearday=yearday))
        await state.reset_state()
    except AttributeError:
        await message.answer(_("Вы некорректно ввели дату. Попробуйте еще раз"))


def register_day_num_year(dp: Dispatcher):
    dp.register_message_handler(day_num_year, Command("day_of_year") | Text(contains=__("🔢 Номер дня в году")))
    dp.register_message_handler(dy_chossing, Text(contains=__("Текущая дата")) | Text(contains=__("Конкретная дата")))
    dp.register_message_handler(entering_date_dy, state="enter_date_dy")
