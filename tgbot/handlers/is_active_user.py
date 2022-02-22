from aiogram import Dispatcher, types
from apscheduler.triggers.cron import CronTrigger

from tgbot.misc.start_scheduling import add_all_users_job


async def user_check_active(member: types.ChatMemberUpdated, db_commands, session, scheduler):
    user_id = member.from_user.id
    is_active = member.new_chat_member.is_chat_member()
    user = await db_commands.get_user(user_id=user_id)
    get_user_job = scheduler.get_job(str(user_id))
    if user is not None:
        if is_active is False and get_user_job is not None:
            scheduler.remove_job(str(user_id))
        elif is_active is True and user.user_bd is not None:
            trigger = CronTrigger(hour=13, minute=30, jitter=10800)
            scheduler.add_job(add_all_users_job, trigger,
                              id=str(user_id), replace_existing=False,
                              args=(user_id, member.bot, db_commands))

        await db_commands.update_user_blocked(user_id, is_active)
        await session.commit()


def register_is_active_user(dp: Dispatcher):
    dp.register_my_chat_member_handler(user_check_active)
