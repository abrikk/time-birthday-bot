from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.utils.markdown import hide_link


async def update_hide_link(message: types.Message):
    bot = message.bot
    config = bot.get('config')
    # x = await bot.send_message(chat_id=config.tg_bot.channel_id, text="OK")
    m = await bot.copy_message(chat_id=message.chat.id, from_chat_id=config.tg_bot.channel_id,
                               message_id=2)
    print(m)
    # print(x.message_id)


async def edited_hide_link(message: types.Message):
    await message.answer("EDITED MESSAGE")


def register_upd_hide_links(dp: Dispatcher):
    dp.register_message_handler(update_hide_link, Command("upd_hide_link"))
    dp.register_edited_message_handler(edited_hide_link)
