import math
from datetime import datetime

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageToDeleteNotFound

from tgbot.functions.gettext_func import get_region_date_format
from tgbot.functions.holidays_func import holiday_days_left, get_time_left, get_current_page
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
async def show_chosen_holiday(call: types.CallbackQuery, db_commands, morph, callback_data,
                              state: FSMContext):
    await call.answer()
    user = await db_commands.get_user(user_id=call.from_user.id)
    hol_uid = callback_data.get("hol_uid")
    all_hol_codes = await db_commands.get_all_holidays_uid(user.lang_code)
    current_hol_page = all_hol_codes.index(hol_uid) + 1
    holiday = await db_commands.get_scpecific_holiday(hol_uid)
    holiday_name, holiday_date, time_left, photo_id = \
        await holiday_days_left(holiday=holiday,
                                morph=morph,
                                lang=user.lang_code)
    if user.role == "admin":
        sett_data = {"uid": hol_uid, "holiday_name": holiday[0],
                     "holiday_date": holiday_date}
        await state.update_data(sett_data=sett_data)
    text = _("До {hol_name} осталось {time_left}!\n\n"
             "🎊 Праздник: {hol_inf_name}\n"
             "🗓 Дата: {hol_date}\n"
             "⏳ Осталось времени: {time_left}").format(
        hol_name=holiday_name, time_left=get_time_left(time_left, morph, user.lang_code),
        hol_inf_name=holiday[0],
        hol_date=holiday_date.strftime(get_region_date_format(user.lang_code)))
    await call.message.delete()
    await call.message.answer_photo(photo=photo_id, caption=text,
                                    reply_markup=change_hol_keyb(
                                        max_pages=len(all_hol_codes),
                                        page=current_hol_page,
                                        admin=user.role == 'admin'
                                    ))


async def change_hol_page(call: types.CallbackQuery, callback_data: dict, db_commands, morph,
                          state: FSMContext):
    await call.answer()

    user = await db_commands.get_user(user_id=call.from_user.id)
    all_hol_codes = await db_commands.get_all_holidays_uid(user.lang_code)
    current_hol_page = int(callback_data.get("page"))
    current_page = get_current_page(current_hol_page, len(all_hol_codes))

    current_hol_code = get_page(all_hol_codes, page=current_page)
    holiday = await db_commands.get_scpecific_holiday(current_hol_code)
    holiday_name, holiday_date, time_left, hide_photo = \
        await holiday_days_left(holiday=holiday,
                                morph=morph,
                                lang=user.lang_code)

    if user.role == "admin":
        data = await state.get_data()
        msg_to_delete = data.get("msg_to_delete")
        if msg_to_delete:
            await call.bot.delete_message(call.message.chat.id, msg_to_delete)
            await state.reset_state()
        sett_data = {"uid": current_hol_code, "holiday_name": holiday[0],
                     "holiday_date": holiday_date}
        await state.update_data(sett_data=sett_data)
    text = _("До {hol_name} осталось {time_left}!\n\n"
             "🎊 Праздник: {hol_inf_name}\n"
             "🗓 Дата: {hol_date}\n"
             "⏳ Осталось времени: {time_left}").format(
        hol_name=holiday_name, time_left=get_time_left(time_left, morph, user.lang_code),
        hol_inf_name=holiday[0],
        hol_date=holiday_date.strftime(get_region_date_format(user.lang_code)))

    await call.message.delete()
    await call.message.answer_photo(photo=hide_photo, caption=text,
                                    reply_markup=change_hol_keyb(
                                        max_pages=len(all_hol_codes),
                                        page=current_page,
                                        admin=user.role == 'admin'
                                    ))


async def holiday_settings(call: types.CallbackQuery, callback_data: dict, db_commands):
    print(call.data)
    await call.answer()
    user = await db_commands.get_user(user_id=call.from_user.id)
    hol_page = int(callback_data.get("page"))
    print(hol_page)
    all_hol_codes = await db_commands.get_all_holidays_uid(user.lang_code)
    current_hol_code = get_page(all_hol_codes, page=hol_page)
    holiday = await db_commands.get_scpecific_holiday(current_hol_code)
    hol_en_name = await db_commands.get_holidays_en_name(current_hol_code)
    await call.message.edit_caption(caption=f"Доброго времени суток, {call.from_user.first_name}!\n"
                                            f"Что будем делать с праздником?\n\n"
                                            f"Праздник ru: <code>{holiday[0]}</code>\n\n"
                                            f"Праздник en: <code>{hol_en_name}</code>\n"
                                            f"Дата: {holiday[1]}\n")
    await call.message.edit_reply_markup(hol_settings_keyboard(hol_page))


# WAITING FOR AN IMAGE
async def change_hol_photo(call: types.CallbackQuery, state: FSMContext):
    print(call.data)
    await call.answer()
    msg = await call.message.answer("Хорошо. Теперь отправьте новую картинку праздника.")
    await state.update_data(msg_to_delete=msg.message_id)
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
        print(data)
        sett_data = data.get("sett_data")
        photo = data.get("photo")
        hol_msg_id = await db_commands.get_scpecific_hol_msg_id(sett_data.get("uid"))

        if not hol_msg_id:
            new_pic = await bot.send_photo(chat_id=config.tg_bot.channel_id,
                                           photo=photo)

        else:
            new_pic = await bot.edit_message_media(chat_id=config.tg_bot.channel_id,
                                                   media=types.InputMedia(type='photo',
                                                                          media=photo),
                                                   message_id=hol_msg_id)

        pic_id = new_pic.photo[-1].file_id
        pic_msg_id = new_pic.message_id

        caption = ("• Holiday name: {hol_name}\n"
                   "• Holiday date: {hol_date}\n"
                   "• Holiday uid: <code>{hol_uid}</code>\n"
                   "• Holiday message_id: <code>{pic_msg_id}</code>\n"
                   "• Holiday photo_id: <code>{pic_id}...</code>\n"
                   "• Last update: {last_update}\n"
                   "• Updated by: {updated_by}").format(
            hol_name=sett_data.get("holiday_name"),
            hol_date=sett_data.get("holiday_date").strftime("%d.%m.%Y"),
            hol_uid=sett_data.get("uid"),
            pic_msg_id=pic_msg_id,
            pic_id=pic_id[:30],
            last_update=datetime.now().strftime("%d.%m.%Y - %H:%M"),
            updated_by=call.from_user.full_name
        )

        await bot.edit_message_caption(chat_id=config.tg_bot.channel_id,
                                       message_id=pic_msg_id,
                                       caption=caption)

        await db_commands.update_holiday_pic_and_msg_id(sett_data.get("uid"), pic_id, pic_msg_id)
        await session.commit()
        await call.message.delete()
        await bot.send_message(chat_id=call.from_user.id,
                               text="Картинка праздника изменена!",
                               reply_to_message_id=call.message.message_id - 1)
        await state.reset_state()
    else:
        await call.message.answer("Хорошо. Жду другую фотографию.")
        await state.set_state('edit_hol_photo')


async def sent_wrong_message(message: types.Message):
    await message.answer("Вы отправили не картинку. Попробуйте еще раз. Если вы хотите отменить"
                         " изменение картинки отправьте команду /cancel.")


async def share_with_holiday(call: types.CallbackQuery):
    await call.answer(text="ФУНКЦИЯ ЕЩЁ НЕ ГОТОВА", show_alert=True)


# SWITCH TO GIVEN PAGE
async def switch_to_page(call: types.CallbackQuery, state: FSMContext, ):
    await call.answer()
    await call.message.answer(_("Введите номер страницы на которую вы хотите перейти."))
    await state.set_state('switch_to_page')


async def switching_to_page(message: types.Message, state: FSMContext, db_commands, morph):
    if message.text.isdigit():
        user = await db_commands.get_user(user_id=message.from_user.id)
        all_hol_codes = await db_commands.get_all_holidays_uid(user.lang_code)
        current_hol_page = int(message.text)
        current_page = get_current_page(current_hol_page, len(all_hol_codes))

        current_hol_code = get_page(all_hol_codes, page=current_page)
        holiday = await db_commands.get_scpecific_holiday(current_hol_code)
        holiday_name, holiday_date, time_left, hide_photo = \
            await holiday_days_left(holiday=holiday,
                                    morph=morph,
                                    lang=user.lang_code)

        if user.role == "admin":
            sett_data = {"uid": current_hol_code, "holiday_name": holiday_name,
                         "holiday_date": holiday_date}
            await state.update_data(sett_data=sett_data)
        text = _("До {hol_name} осталось {time_left}!\n\n"
                 "🎊 Праздник: {hol_inf_name}\n"
                 "🗓 Дата: {hol_date}\n"
                 "⏳ Осталось времени: {time_left}").format(
            hol_name=holiday_name, time_left=get_time_left(time_left, morph, user.lang_code),
            hol_inf_name=holiday[0],
            hol_date=holiday_date.strftime(get_region_date_format(user.lang_code)))

        await message.delete()
        await message.bot.delete_message(chat_id=message.from_user.id,
                                         message_id=message.message_id - 1)
        await message.bot.delete_message(chat_id=message.from_user.id,
                                         message_id=message.message_id - 2)
        await message.answer_photo(photo=hide_photo, caption=text,
                                   reply_markup=change_hol_keyb(
                                       max_pages=len(all_hol_codes),
                                       page=current_page,
                                       admin=user.role == 'admin'
                                   ))
        await state.reset_state(with_data=False)
    else:
        await message.bot.delete_message(chat_id=message.from_user.id,
                                         message_id=message.message_id - 1)
        await state.reset_state()


def register_inter_holidays(dp: Dispatcher):
    dp.register_callback_query_handler(switch_inter_hol, inter_hol_cb.filter(action="switch_page"))
    dp.register_callback_query_handler(show_chosen_holiday, inter_hol_cb.filter())
    dp.register_callback_query_handler(holiday_settings, hol_pag_cb.filter(action="settings"))
    dp.register_callback_query_handler(share_with_holiday, hol_pag_cb.filter(action="share_message"))
    dp.register_callback_query_handler(switch_to_page, hol_pag_cb.filter(action="switch_page"))

    dp.register_callback_query_handler(change_hol_page, hol_pag_cb.filter() |
                                       sett_cb.filter(action="back"), state="*")
    dp.register_callback_query_handler(change_hol_photo, sett_cb.filter(action="img"))
    dp.register_message_handler(confirming_hol_photo, content_types=types.ContentType.PHOTO, state='edit_hol_photo')
    dp.register_message_handler(sent_wrong_message, content_types=types.ContentType.ANY, state='edit_hol_photo')
    dp.register_callback_query_handler(confirm_photo, state='confirm_hol_photo')
    dp.register_message_handler(switching_to_page, state='switch_to_page')
