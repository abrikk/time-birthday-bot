import asyncio
import logging
import warnings

import pymorphy2
import tzlocal
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz_deprecation_shim import PytzUsageWarning

from tgbot.config import load_config
from tgbot.filters.admin_bot import AdminOfBot
from tgbot.handlers.setup import register_all_handlers
from tgbot.middlewares.db import DbSessionMiddleware
from tgbot.middlewares.lang_middleware import i18n
from tgbot.middlewares.morpholyzer import MorphMiddleware
from tgbot.middlewares.role import RoleMiddleware
from tgbot.middlewares.scheduler import SchedulerMiddleware
from tgbot.misc.notify_admins import on_startup_notify
from tgbot.misc.start_scheduling import add_all_jobs
from tgbot.services.database import create_db_session
from tgbot.services.db_commands import DBCommands

logger = logging.getLogger(__name__)


def register_all_middlewares(dp, scheduler, morpholyzer, sessionmaker):
    dp.setup_middleware(SchedulerMiddleware(scheduler))
    dp.setup_middleware(MorphMiddleware(morpholyzer))
    dp.setup_middleware(DbSessionMiddleware(sessionmaker))
    dp.setup_middleware(RoleMiddleware())
    dp.setup_middleware(i18n)


def register_all_filters(dp):
    dp.filters_factory.bind(AdminOfBot)


# register_all_handlers(dp) imports from tgbot.handlers.setup


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
    morph = pymorphy2.MorphAnalyzer()

    bot['config'] = config

    async with sessionmaker() as session:
        db_commands = DBCommands(session)
        user_ids = await db_commands.get_all_users_with_date()
        add_all_jobs(user_ids, bot, db_commands, scheduler)
        await session.commit()

    await on_startup_notify(bot)

    register_all_middlewares(dp, scheduler, morph, sessionmaker)
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
