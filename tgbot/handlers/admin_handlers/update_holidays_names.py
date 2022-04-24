from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Command
from googletrans import Translator


async def update_hols_trans(message: types.Message, db_commands, session):
    all_holidays = await db_commands.get_holidays_name()
    translator = Translator(user_agent="APIs-Google (+https://developers.google.com/webmasters/APIs-Google.html")
    await message.answer("Начинаю переводить праздники.")
    for uid, name in all_holidays:
        hn_ru = translator.translate(name, src="en", dest="ru").text
        hn_uz = translator.translate(name, src="en", dest="uz").text
        hn_ua = translator.translate(name, src="en", dest="uk").text
        hn_es = translator.translate(name, src="en", dest="es").text
        hn_fr = translator.translate(name, src="en", dest="fr").text
        await db_commands.update_hol_name(uid, hn_ru, hn_uz, hn_ua, hn_es, hn_fr)
        await session.commit()
        await message.answer(f"Перевод праздника {name} завершен.")
    await message.answer("Перевод праздников завершен.")


def register_update_hols(dp: Dispatcher):
    dp.register_message_handler(update_hols_trans, Command("upd_ht"))
