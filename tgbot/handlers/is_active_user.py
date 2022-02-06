from aiogram import Dispatcher, types


async def user_check_active(member: types.ChatMemberUpdated, db_commands, session):
    is_active = member.new_chat_member.is_chat_member()
    print(is_active)
    await db_commands.update_user_blocked(member.from_user.id, is_active)
    await session.commit()


def register_is_active_user(dp: Dispatcher):
    dp.register_my_chat_member_handler(user_check_active)
