from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeChat

from loader import bot


async def set_default_commands(dp):
    usercommands = [
        BotCommand(command="start", description="Запустить бота"),
        BotCommand(command="help", description="Помощь"),
        BotCommand(command="mybd", description="Сколько дней осталось до дня рождения"),
        BotCommand(command="newyear", description="Сколько дней осталось до Нового Года"),
        BotCommand(command="howmanydays", description="Разница между текущей и заданной датой"),
        BotCommand(command="botinfo", description="Information")
    ]
    await bot.set_my_commands(usercommands, scope=BotCommandScopeDefault())

    admin_commands = [
        BotCommand(command="start", description="Запустить бота"),
        BotCommand(command="help", description="Помощь"),
        BotCommand(command="mybd", description="Сколько дней осталось до дня рождения"),
        BotCommand(command="newyear", description="Сколько дней осталось до Нового Года"),
        BotCommand(command="howmanydays", description="Разница между текущей и заданной датой"),
        BotCommand(command="statistics", description="Статистику бота"),
        BotCommand(command="show_state", description="Показать текущее состояние"),
        BotCommand(command="botinfo", description="Information")
    ]
    await bot.set_my_commands(admin_commands, scope=BotCommandScopeChat(chat_id=569356638))
