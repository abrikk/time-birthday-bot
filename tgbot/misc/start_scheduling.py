from aiogram import Bot
from apscheduler.triggers.cron import CronTrigger

from tgbot.functions.gettext_func import get_user_turned_day_text


async def add_all_users_job(chat_id, bot: Bot, db_commands):
    await bot.send_message(chat_id, await get_user_turned_day_text(chat_id, db_commands))


def add_all_jobs(user_ids: list, bot, db_commands, scheduler):
    trigger = CronTrigger(hour=13, minute=30, jitter=10800)
    # trigger = IntervalTrigger(seconds=5)
    for user_id in user_ids:
        scheduler.add_job(add_all_users_job, trigger,
                          id=str(user_id), replace_existing=True,
                          args=(user_id, bot, db_commands))


