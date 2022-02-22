import asyncio
import logging
import warnings

import tzlocal
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz_deprecation_shim import PytzUsageWarning

from tgbot.config import load_config
from tgbot.filters.admin import AdminFilter
from tgbot.handlers.additional_keyboard import register_add_keyb
from tgbot.handlers.admin_commands import register_admin_commands
from tgbot.handlers.birthday import register_my_bd
from tgbot.handlers.botinfo import register_bot_info
from tgbot.handlers.cancel_handler import register_cancel_action
from tgbot.handlers.change_language import register_change_language
from tgbot.handlers.day_number_in_the_year import register_day_num_year
from tgbot.handlers.help import register_help
from tgbot.handlers.how_many_days import register_hmd
from tgbot.handlers.is_active_user import register_is_active_user
from tgbot.handlers.life_counter import register_count_life
from tgbot.handlers.newyear import register_newyear
from tgbot.handlers.profile import register_profile
from tgbot.handlers.show_all_jobs import register_show_all_tasks
from tgbot.handlers.start import register_start
from tgbot.handlers.statistics import register_stat
from tgbot.handlers.test import register_test_1
from tgbot.handlers.update_botinfo import register_update_botinfo
from tgbot.handlers.update_profile import register_update
from tgbot.handlers.whose_birthday_is_today import register_bd_today
from tgbot.keyboards.inline import register_inline_mode
from tgbot.middlewares.db import DbSessionMiddleware
from tgbot.middlewares.lang_middleware import i18n
from tgbot.middlewares.scheduler import SchedulerMiddleware
from tgbot.misc.notify_admins import on_startup_notify
from tgbot.misc.start_scheduling import add_all_jobs
from tgbot.services.database import create_db_session
from tgbot.services.db_commands import DBCommands

logger = logging.getLogger(__name__)


def register_all_middlewares(dp, scheduler, sessionmaker):
    dp.setup_middleware(SchedulerMiddleware(scheduler))
    dp.setup_middleware(DbSessionMiddleware(sessionmaker))
    dp.setup_middleware(i18n)


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp):
    register_inline_mode(dp)
    register_cancel_action(dp)
    register_update(dp)
    register_test_1(dp)
    register_show_all_tasks(dp)
    register_my_bd(dp)
    register_profile(dp)
    register_add_keyb(dp)
    register_stat(dp)
    register_day_num_year(dp)
    register_bd_today(dp)
    register_hmd(dp)
    register_bot_info(dp)
    register_update_botinfo(dp)
    register_newyear(dp)
    register_change_language(dp)
    register_admin_commands(dp)
    register_help(dp)
    register_start(dp)
    register_count_life(dp)
    register_is_active_user(dp)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',

    )
    logger.info("Starting bot")
    config = load_config(".env")

    if config.tg_bot.use_redis:
        storage = RedisStorage()
    else:
        storage = MemoryStorage()

    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)
    sessionmaker = await create_db_session(config)

    warnings.filterwarnings(action="ignore", category=PytzUsageWarning)
    scheduler = AsyncIOScheduler(timezone=str(tzlocal.get_localzone()))

    bot['config'] = config

    async with sessionmaker() as session:
        db_commands = DBCommands(session)
        user_ids = await db_commands.get_all_users_with_date()
        add_all_jobs(user_ids, bot, db_commands, scheduler)
        await session.commit()

    await on_startup_notify(bot)

    register_all_middlewares(dp, scheduler, sessionmaker)
    register_all_filters(dp)
    register_all_handlers(dp)

    # start
    try:
        scheduler.start()
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
