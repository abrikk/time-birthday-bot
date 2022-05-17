from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware

from tgbot.services.db_commands import DBCommands


class RoleMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]

    async def pre_process(self, obj, data, *args):
        db: DBCommands = data["db_commands"]
        user_id = obj.from_user.id
        user = await db.get_user(user_id)
        if not user:
            data["role"] = None
        elif user.role == "admin":
            data["role"] = "admin"
        else:
            data["role"] = "user"

    async def post_process(self, obj, data, *args):
        del data["role"]
