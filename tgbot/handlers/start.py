from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.utils.markdown import hcode

from tgbot.functions.gettext_func import get_start_text
from tgbot.keyboards.reply import lang_cb, main_keyb, lang_keyb
from tgbot.middlewares.lang_middleware import _, i18n
from tgbot.misc.set_bot_commands import set_default_commands


async def bot_start(message: types.Message, state: FSMContext, session, db_commands):
    user = await db_commands.get_user(user_id=message.from_user.id)

    if user is None:
        config = message.bot.get('config')
        text = f"New user: \n" \
               f"Full name: {message.from_user.get_mention(as_html=True)}\n" \
               f"Username: @{message.from_user.username}\n" \
               f"ID: {hcode(message.from_user.id)}"
        await message.bot.send_message(chat_id=config.tg_bot.chat_id, text=text)

        await db_commands.add_user(user_id=message.from_user.id,
                                   first_name=message.from_user.first_name,
                                   last_name=message.from_user.last_name,
                                   username=message.from_user.username,
                                   lang_code=message.from_user.language_code,
                                   role='user'
                                   )
        if str(message.from_user.id) in config.tg_bot.admin_ids:
            await db_commands.set_admins(message.from_user.id)

        await session.commit()

        await message.answer(_("🌐 Выберите язык:"), reply_markup=lang_keyb)
        await state.set_state("choosing_lang_start")

    else:
        await message.answer(get_start_text(message.from_user.full_name))


async def choosing_language_start(call: types.CallbackQuery, state: FSMContext, callback_data: dict, db_commands,
                                  session):
    lang = callback_data.get("name")
    i18n.ctx_locale.set(lang)
    await call.answer(text=_("🇷🇺 Вы выбрали русский язык").format(lang=lang))
    await call.message.delete()
    await call.message.answer(get_start_text(call.from_user.full_name), reply_markup=main_keyb())
    await set_default_commands(call.bot)

    await db_commands.update_language(user_id=call.from_user.id, lang=lang)
    await session.commit()

    await state.reset_state()


async def choosing_language_start_state(message: types.Message):
    await message.answer(_("🌐 Выберите язык:"), reply_markup=lang_keyb)


def register_start(dp: Dispatcher):
    dp.register_message_handler(bot_start, CommandStart())
    dp.register_callback_query_handler(choosing_language_start, lang_cb.filter(), state="choosing_lang_start")
    dp.register_message_handler(choosing_language_start_state, state="choosing_lang_start")
