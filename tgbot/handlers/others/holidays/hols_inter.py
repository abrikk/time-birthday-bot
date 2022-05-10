import math

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from tgbot.functions.holidays_days_left_func import holiday_days_left, get_time_left
from tgbot.handlers.main_menu_keyb.whose_birthday_is_today.whose_birthday_is_today import get_page
from tgbot.handlers.others.holidays.holidays_keyb import change_hol_keyb, inter_holidays_keyb, hol_settings_keyboard, \
    inter_hol_cb, hol_pag_cb, hol_cb
from tgbot.middlewares.lang_middleware import _


# 1.1 LEVEL SECTION
async def show_inter_holidays(call: types.CallbackQuery, db_commands):
    await call.answer()
    all_holidays = await db_commands.get_10_holidays(lang=await db_commands.get_user_language(call.from_user.id))
    number_of_hols = await db_commands.count_all_holidays()

    holidays_name = [hn for hn, dt, cb, hl in all_holidays]
    holidays_cb = [cb for hn, dt, cb, hl in all_holidays]
    buttons = {name: cb for name, cb in zip(holidays_name, holidays_cb)}

    text = _("Популярные праздники в мире. Нажми на кнопку, чтобы узнать сколько дней осталось"
             "до праздника.")
    await call.message.delete()
    await call.message.answer(text, reply_markup=inter_holidays_keyb(
        buttons=buttons,
        max_pages=math.ceil(number_of_hols / 9)
    )
                              )


async def switch_inter_hol(call: types.CallbackQuery, db_commands, callback_data):
    await call.answer()
    number_of_hols = await db_commands.count_all_holidays()
    current_hol_page = int(callback_data.get("page"))

    if current_hol_page > math.ceil(number_of_hols / 9):
        current_hol_page = 1
    elif current_hol_page < 1:
        current_hol_page = math.ceil(number_of_hols / 9)

    offset = (current_hol_page - 1) * 9
    all_holidays = await db_commands.get_10_holidays(lang=await db_commands.get_user_language(call.from_user.id),
                                                     offset=offset)

    holidays_name = [hn for hn, dt, cb, hl in all_holidays]
    holidays_cb = [cb for hn, dt, cb, hl in all_holidays]
    buttons = {name: cb for name, cb in zip(holidays_name, holidays_cb)}

    text = _("Популярные праздники в мире. Нажми на кнопку, чтобы узнать сколько дней осталось"
             "до праздника.")
    await call.message.edit_text(text, reply_markup=inter_holidays_keyb(
        buttons=buttons,
        max_pages=math.ceil(number_of_hols / 9),
        page=current_hol_page)
                                 )


# 1.1.1 LEVEL SECTION
async def show_chosen_holiday(call: types.CallbackQuery, db_commands, morph, callback_data):
    await call.answer()
    user = await db_commands.get_user(user_id=call.from_user.id)
    hol_uid = callback_data.get("hol_uid")
    all_hol_codes = await db_commands.get_all_holidays_uid(user.lang_code)
    current_hol_page = all_hol_codes.index(hol_uid) + 1
    holiday_name, holiday_date, time_left, hide_photo = \
        await holiday_days_left(hol_uid, db_commands)
    text = _("До {hol_name} осталось {time_left}!").format(
        hol_name=holiday_name, time_left=get_time_left(time_left, morph))
    await call.message.delete()
    await call.message.answer_photo(photo=hide_photo, caption=text,
                                    reply_markup=change_hol_keyb(
                                        max_pages=len(all_hol_codes),
                                        page=current_hol_page,
                                        admin=user.role == 'admin'
                                    ))


async def change_hol_page(call: types.CallbackQuery, callback_data: dict, db_commands, morph):
    await call.answer()
    user = await db_commands.get_user(user_id=call.from_user.id)
    all_hol_codes = await db_commands.get_all_holidays_uid(user.lang_code)
    current_hol_page = int(callback_data.get("page"))

    if current_hol_page > len(all_hol_codes):
        current_hol_page = abs(len(all_hol_codes) - current_hol_page)
        print(current_hol_page)
    elif current_hol_page < 1:
        current_hol_page = len(all_hol_codes) - abs(current_hol_page)

    current_hol_code = get_page(all_hol_codes, page=current_hol_page)
    holiday_name, holiday_date, time_left, hide_photo = \
        await holiday_days_left(current_hol_code, db_commands)

    text = _("До {hol_name} осталось {time_left}!").format(
        hol_name=holiday_name, time_left=get_time_left(time_left, morph))

    await call.message.delete()
    await call.message.answer_photo(photo=hide_photo, caption=text,
                                    reply_markup=change_hol_keyb(
                                        max_pages=len(all_hol_codes),
                                        page=current_hol_page,
                                        admin=user.role == 'admin'
                                    ))


async def holiday_settings(call: types.CallbackQuery, db_commands, state: FSMContext):
    await call.answer()
    print("OK")
    await call.message.edit_reply_markup(hol_settings_keyboard())

    await state.set_state("edit_hol_photo")


def register_inter_holidays(dp: Dispatcher):
    dp.register_callback_query_handler(show_inter_holidays, hol_cb.filter(hol_type_name="ih") |
                                       hol_pag_cb.filter(action="back_inter"))
    dp.register_callback_query_handler(switch_inter_hol, inter_hol_cb.filter(action="switch_page"))
    dp.register_callback_query_handler(show_chosen_holiday, inter_hol_cb.filter())
    dp.register_callback_query_handler(holiday_settings, hol_pag_cb.filter(action="settings"))
    dp.register_callback_query_handler(change_hol_page, hol_pag_cb.filter())