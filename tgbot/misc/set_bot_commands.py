from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeChat
from tgbot.middlewares.lang_middleware import _


async def set_default_commands(bot: Bot):
    config = bot.get('config')
    usercommands = [
        BotCommand(command="start", description=_("Запустить бота")),
        BotCommand(command="help", description=_("Помощь")),
        BotCommand(command="profile", description=_("Профиль")),
        BotCommand(command="setlanguage", description=_("Поменять язык")),
        BotCommand(command="others", description=_("Дополнительное меню")),
        BotCommand(command="botinfo", description=_("Информация о боте")),
        BotCommand(command="cancel", description=_("Отменить текущую операцию"))
    ]
    await bot.set_my_commands(usercommands, scope=BotCommandScopeDefault())

    admin_commands = [
        BotCommand(command="start", description=_("Запустить бота")),
        BotCommand(command="help", description=_("Помощь")),
        BotCommand(command="profile", description=_("Профиль")),
        BotCommand(command="setlanguage", description=_("Поменять язык")),
        BotCommand(command="others", description=_("Дополнительное меню")),
        BotCommand(command="statistics", description=_("Статистика")),
        BotCommand(command="botinfo", description=_("Информация о боте")),
        BotCommand(command="cancel", description=_("Отменить текущую операцию")),
        BotCommand(command="delete_me", description="delete_me"),
        BotCommand(command="delete_keyboard", description="delete_keyboard"),
        BotCommand(command="show_tasks", description="show jobs"),
    ]
    for admin in config.tg_bot.admin_ids:
        await bot.set_my_commands(admin_commands, scope=BotCommandScopeChat(chat_id=admin))
