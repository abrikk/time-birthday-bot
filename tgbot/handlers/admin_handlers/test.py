from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.utils.markdown import hide_link


async def test_1(message: types.Message, db_commands):
    bot = message.bot
    config = bot.get('config')
    await bot.send_message(message.chat.id, "ВОТЬ")
    await bot.copy_message(chat_id=message.chat.id, from_chat_id=config.tg_bot.channel_id,
                           message_id=243)
    # await message.bot.edit_message_media(media=types.InputMedia(
    #     type='photo', media='https://i.insider.com/592f4169b74af41b008b5977?width=700'),
    #     chat_id=config.tg_bot.channel_id,
    #     message_id=243)


def register_test_1(dp: Dispatcher):
    dp.register_message_handler(test_1, Command("test_1"))
