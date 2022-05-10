import math

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from tgbot.functions.holidays_days_left_func import holiday_days_left, get_time_left
from tgbot.handlers.main_menu_keyb.whose_birthday_is_today.whose_birthday_is_today import get_page
from tgbot.handlers.others.holidays.holidays_keyb import change_hol_keyb, inter_holidays_keyb, hol_settings_keyboard, \
    inter_hol_cb, hol_pag_cb, hol_cb, sett_cb, confirm_chane
from tgbot.middlewares.lang_middleware import _


# 1.1 LEVEL SECTION
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


async def holiday_settings(call: types.CallbackQuery, callback_data: dict):
    await call.answer()
    print("HOL SETTINGS")
    hol_page = int(callback_data.get("page"))
    await call.message.edit_caption(caption=f"Доброго времени суток, {call.from_user.first_name}!\n"
                                            f"Что будем делать с праздником?")
    await call.message.edit_reply_markup(hol_settings_keyboard(hol_page))


# WAITING FOR AN IMAGE
async def change_hol_photo(call: types.CallbackQuery, callback_data: dict, db_commands, state: FSMContext):
    print("CHANGE HOL PHOTO")
    await call.answer()
    await call.message.answer("Хорошо. Теперь отправьте новую картинку праздника.")
    await state.set_state("edit_hol_photo")


async def confirming_hol_photo(message: types.Message, state: FSMContext):
    photo = message.photo[-1].file_id
    print(photo)
    await state.update_data(photo=photo)
    await message.answer("Подтвердите ваше действие.", reply_markup=confirm_chane())
    await state.set_state("confirm_hol_photo")


async def confirm_photo(call: types.CallbackQuery, state: FSMContext, db_commands, session):
    await call.answer()
    bot = call.bot
    config = bot.get('config')
    if call.data == "confirm_pic_change":
        data = await state.get_data()
        photo = data.get("photo")
        new_pic = await bot.send_photo(chat_id=config.tg_bot.channel_id,
                                       photo=photo)
        print(new_pic.message_id)
        await call.message.delete()
        await bot.send_message(chat_id=call.from_user.id,
                               text="Картинка праздника изменена!",
                               reply_to_message_id=call.message.message_id-1)
        await state.reset_state()
    else:
        await call.message.answer("Хорошо. Жду другую фотографию.")
        await state.set_state('edit_hol_photo')


async def sent_wrong_message(message: types.Message):
    await message.answer("Вы отправили не картинку. Попробуйте еще раз.")


def register_inter_holidays(dp: Dispatcher):
    dp.register_callback_query_handler(switch_inter_hol, inter_hol_cb.filter(action="switch_page"))
    dp.register_callback_query_handler(show_chosen_holiday, inter_hol_cb.filter())
    dp.register_callback_query_handler(holiday_settings, hol_pag_cb.filter(action="settings"))
    dp.register_callback_query_handler(change_hol_page, hol_pag_cb.filter() |
                                       sett_cb.filter(action="back"))
    dp.register_callback_query_handler(change_hol_photo, sett_cb.filter(action="img"))
    dp.register_message_handler(confirming_hol_photo, content_types=types.ContentType.PHOTO, state='edit_hol_photo')
    dp.register_message_handler(sent_wrong_message, content_types=types.ContentType.ANY, state='edit_hol_photo')
    dp.register_callback_query_handler(confirm_photo, state='confirm_hol_photo')
