import datetime

from sqlalchemy import select, update, func, delete, and_, extract

from tgbot.models.about_bot import AboutBot
from tgbot.models.users import User


class DBCommands:
    def __init__(self, session):
        self.session = session

    # User commands

    async def get_user(self, user_id: int):
        sql = select(User).where(User.user_id == user_id)
        request = await self.session.execute(sql)
        user = request.scalar()
        return user

    async def add_user(self,
                       user_id: int,
                       first_name: str,
                       last_name: str = None,
                       username: str = None,
                       user_bd=None,
                       lang_code: str = None,
                       role: str = None
                       ) -> 'User':
        user = User(user_id=user_id,
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    user_bd=user_bd,
                    lang_code=lang_code,
                    role=role)
        self.session.add(user)
        return user

    async def update_user_name(self, user_id, new_name) -> 'User':
        sql = update(User).where(User.user_id == user_id).values(first_name=new_name)
        result = await self.session.execute(sql)
        return result

    async def update_user_rating(self, user_id, rating):
        sql = update(User).where(User.user_id == user_id).values(rating=rating)
        result = await self.session.execute(sql)
        return result

    async def count_users(self):
        sql = select(func.count("*")).select_from(User)
        result = await self.session.execute(sql)
        return result.scalar()

    async def set_admins(self, user_id):
        sql = update(User).where(User.user_id == user_id).values(role='admin')
        result = await self.session.execute(sql)
        return result

    async def update_language(self, user_id, lang):
        sql = update(User).where(User.user_id == user_id).values(lang_code=lang)
        result = await self.session.execute(sql)
        return result

    async def get_user_language(self, user_id):
        sql = select(User.lang_code).where(User.user_id == user_id)
        request = await self.session.execute(sql)
        user = request.scalar()
        return user

    async def update_user_date(self, user_id, date):
        sql = update(User).where(User.user_id == user_id).values(user_bd=date)
        result = await self.session.execute(sql)
        return result

    async def update_user_sex(self, user_id: int, sex: int):
        sql = update(User).where(User.user_id == user_id).values(sex=sex)
        result = await self.session.execute(sql)
        return result

    async def delete_me_from_db(self, user_id):
        sql = delete(User).where(User.user_id == user_id)
        result = await self.session.execute(sql)
        return result

    async def select_all_users_bd_today(self):
        sql = select(User.user_id).where(
            and_(
                extract('month', User.user_bd) == extract('month', func.current_date()),
                extract('day', User.user_bd) == extract('day', func.current_date())
            )
        )
        result = await self.session.execute(sql)
        scalars = result.scalars().unique().all()
        return scalars

    async def get_all_ratings(self):
        sql = select(User.rating).where(User.rating.is_not(None))
        result = await self.session.execute(sql)
        scalars = result.scalars().all()
        return scalars

    # async def count_bd_users(self):
    #     sql = select(func.count()).where(
    #         and_(
    #             extract('month', User.user_bd) == extract('month', func.current_date()),
    #             extract('day', User.user_bd) == extract('day', func.current_date())
    #         )
    #     ).select_from(User)
    #     result = await self.session.execute(sql)
    #     return result.scalar()

    # IS NOT USING
    # AboutBot commands

    async def add_bot(self,
                         username: str,
                         version: str = None,
                         languages: int = None,
                         updated_at: datetime.datetime = None,
                         updated_on: datetime.date = None,
                         released_on: datetime.date = None,
                         created_on: datetime.date = None
                         ) -> 'AboutBot':
        about_bot = AboutBot(username=username,
                             version=version,
                             languages=languages,
                             updated_at=updated_at,
                             updated_on=updated_on,
                             released_on=released_on,
                             created_on=created_on
                             )
        self.session.add(about_bot)
        return about_bot

    async def get_bot_info(self, username: str):
        sql = select(AboutBot).where(AboutBot.username == username)
        request = await self.session.execute(sql)
        user = request.scalar()
        return user

    async def update_botinfo_date(self, username, date):
        sql = update(AboutBot).where(AboutBot.username == username).values(updated_on=date)
        result = await self.session.execute(sql)
        return result

    async def update_botinfo_version(self, username, version):
        sql = update(AboutBot).where(AboutBot.username == username).values(version=version)
        result = await self.session.execute(sql)
        return result

    async def update_botinfo_lang(self, username, lang):
        sql = update(AboutBot).where(AboutBot.username == username).values(languages=lang)
        result = await self.session.execute(sql)
        return result
