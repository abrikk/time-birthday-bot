import logging

from aiogram import Bot
from aiogram.utils.exceptions import BotBlocked


async def on_startup_notify(bot: Bot):
    config = bot.get('config')
    for admin in config.tg_bot.admin_ids:
        try:
            await bot.send_message(admin, "Бот Запущен на ветке Docker+Alembic")
        except BotBlocked:
            logging.warning("Forbidden: bot was blocked by the user")
        except Exception as err:
            logging.exception(err)
