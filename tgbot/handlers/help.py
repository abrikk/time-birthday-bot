from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import CommandHelp, Text

from tgbot.functions.gettext_func import get_help_text, get_botinfo_text, get_echo_text, get_available_formats_text, \
    get_date_order_text
from tgbot.handlers.whose_birthday_is_today import get_page
from tgbot.keyboards.reply import help_manual, manual_data, help_ability, ability_data, \
    help_back_manual, help_rate, rate_data, update_bot_info, date_order_cb
from tgbot.middlewares.lang_middleware import __, _


# MANUAL

async def bot_help(message: types.Message):
    await message.answer(_("🔰 <b>Руководство:</b> "), reply_markup=help_manual())


# BACK TO MANUAL

async def help_bot_back(call: types.CallbackQuery):
    await call.answer()
    await call.message.edit_text(_("🔰 <b>Руководство:</b> "), reply_markup=help_manual())


# BOT FEATURES

async def help_bot_ability(call: types.CallbackQuery):
    await call.answer()
    help_text = get_help_text()
    page_index = get_page(help_text)

    await call.message.edit_text(page_index, reply_markup=help_ability(max_pages=len(help_text)))


async def help_bot_ability_show_chosen_page(call: types.CallbackQuery, callback_data: dict):
    await call.answer()
    help_text = get_help_text()
    current_page = int(callback_data.get("page"))
    if current_page > len(help_text):
        current_page = 1
    elif current_page < 1:
        current_page = len(help_text)
    page_index = get_page(help_text, page=current_page)
    markup = help_ability(max_pages=len(help_text), page=current_page)
    await call.message.edit_text(text=page_index, reply_markup=markup)


async def help_current_page_ability_btn(call: types.CallbackQuery):
    await call.answer(cache_time=86400)


# BOT INFORMATION

async def help_bot_information(call: types.CallbackQuery, db_commands, session):
    user = await db_commands.get_user(user_id=call.from_user.id)
    await call.answer()
    await call.message.edit_text(await get_botinfo_text(call, db_commands, session),
                                 disable_web_page_preview=True,
                                 reply_markup=help_back_manual() if user.role != 'admin'
                                 else update_bot_info())


# BOT COMMAND LIST

async def help_bot_commands(call: types.CallbackQuery):
    await call.answer()
    await call.message.edit_text(get_echo_text(), reply_markup=help_back_manual())


# BOT RATING

async def help_bot_rate(call: types.CallbackQuery):
    await call.answer()
    text = _("Оцените бота по 5-бальной шкале 🌟")
    await call.message.edit_text(text, reply_markup=help_rate())


async def help_bot_user_rating(call: types.CallbackQuery, callback_data: dict, db_commands, session):
    await call.answer()
    user_rating = int(callback_data.get("rate"))
    await db_commands.update_user_rating(call.from_user.id, user_rating)
    await session.commit()

    await call.message.edit_text(_("🔰 <b>Руководство:</b> "), reply_markup=help_manual())
    await call.message.answer(_("Спасибо за ваш отзыв!"))


# BOT AVAILABLE DATE FORMATS
avl_date_orders = ["DMY", "MDY", "YMD"]


async def help_bot_formats(call: types.CallbackQuery, db_commands):
    await call.answer()
    date_order: str = await db_commands.get_prefered_date_order(call.from_user.id)
    date_order_index = avl_date_orders.index(date_order)
    print(date_order_index)
    date_order_name = get_date_order_text(date_order)
    await call.message.edit_text(get_available_formats_text(),
                                 reply_markup=help_back_manual(where="avl_formats",
                                 prefered_date_order=date_order_name, page=date_order_index+1))


async def change_date_order(call: types.CallbackQuery, db_commands, session, callback_data):
    await call.answer()
    current_order = int(callback_data.get("order"))
    if current_order >= len(avl_date_orders):
        page = 1
    else:
        page = current_order+1
    page_index = get_page(avl_date_orders, page=page)
    await db_commands.update_user_date_order(call.from_user.id, page_index)
    await session.commit()
    date_order_name = get_date_order_text(page_index)
    markup = help_back_manual(where="avl_formats", prefered_date_order=date_order_name,
                              page=page)
    await call.message.edit_text(get_available_formats_text(),
                                 reply_markup=markup)


def register_help(dp: Dispatcher):
    dp.register_message_handler(bot_help, CommandHelp() | Text(contains=__("❔ Помощь"),
                                                               ignore_case=True))
    dp.register_callback_query_handler(help_bot_ability, manual_data.filter(button="ability"))
    dp.register_callback_query_handler(help_bot_information, manual_data.filter(button="botinfo"))
    dp.register_callback_query_handler(help_bot_rate, manual_data.filter(button="rate"))
    dp.register_callback_query_handler(help_bot_commands, manual_data.filter(button="commands"))
    dp.register_callback_query_handler(help_bot_formats, manual_data.filter(button="formats"))
    dp.register_callback_query_handler(help_bot_back, Text(contains="back_manual"))
    dp.register_callback_query_handler(help_current_page_ability_btn, ability_data.filter(action="current_page"))
    dp.register_callback_query_handler(help_bot_ability_show_chosen_page, ability_data.filter())
    dp.register_callback_query_handler(help_bot_user_rating, rate_data.filter())
    dp.register_callback_query_handler(change_date_order, date_order_cb.filter())
