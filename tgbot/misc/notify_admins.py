import logging

from aiogram import Bot


async def on_startup_notify(bot: Bot):
    config = bot.get('config')
    for admin in config.tg_bot.admin_ids:
        try:
            await bot.send_message(admin, "Бот Запущен")

        except Exception as err:
            logging.exception(err)
