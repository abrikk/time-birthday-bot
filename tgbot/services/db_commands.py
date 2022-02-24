import datetime

from sqlalchemy import select, update, func, delete, and_, extract

from tgbot.models.about_bot import AboutBot
from tgbot.models.bd_statistics import BDStat
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
                       active: bool = True,
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
                    active=active,
                    user_bd=user_bd,
                    lang_code=lang_code,
                    role=role)
        self.session.add(user)
        return user

    async def update_user_blocked(self, user_id: int, active: bool) -> 'User':
        sql = update(User).where(User.user_id == user_id).values(active=active)
        result = await self.session.execute(sql)
        return result

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

    async def update_preferred_date_order(self, user_id, date_order):
        sql = update(User).where(User.user_id == user_id).values(preferred_date_order=date_order)
        result = await self.session.execute(sql)
        return result

    async def get_preferred_date_order(self, user_id):
        sql = select(User.preferred_date_order).where(User.user_id == user_id)
        request = await self.session.execute(sql)
        user = request.scalar()
        return user

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

    async def select_all_users_bd_today(self, user_id: int):
        sql = select(User.user_id).where(
            and_(
                extract('month', User.user_bd) == extract('month', func.current_date()),
                extract('day', User.user_bd) == extract('day', func.current_date()),
                User.user_id != user_id,
                User.active == True
            )
        )
        result = await self.session.execute(sql)
        scalars = result.scalars().unique().all()
        return scalars

    async def get_all_users_with_date(self):
        sql = select(User.user_id).where(
            and_(
                User.user_bd.is_not(None),
                User.active == True,
                User.lang_code.is_not(None)
            )
        ).select_from(User)
        result = await self.session.execute(sql)
        scalars = result.scalars().unique().all()
        return scalars

    async def get_user_is_day_first(self, user_id):
        sql = select(User.day_first).where(User.user_id == user_id)
        request = await self.session.execute(sql)
        user = request.scalar()
        return user

    # async def get_user_lang_code(self, user_id):
    #     sql = select(User.lang_code).where(User.user_id == user_id)
    #     request = await self.session.execute(sql)
    #     user = request.scalar()
    #     return user



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

    # AboutBot commands

    async def add_bot(self,
                      username: str,
                      version: str,
                      languages: int,
                      updated_at: datetime.datetime = None,
                      released_on: datetime.date = None,
                      created_on: datetime.date = None
                      ) -> 'AboutBot':
        about_bot = AboutBot(username=username,
                             version=version,
                             languages=languages,
                             updated_at=updated_at,
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

    async def update_botinfo_date(self, username, date: datetime.datetime):
        sql = update(AboutBot).where(AboutBot.username == username).values(updated_at=date)
        result = await self.session.execute(sql)
        return result

    # BDStat commands

    async def get_user_gratz(self, bd_user_id: int, congo_id: int):
        sql = select(BDStat).where(
            and_(
                BDStat.bd_user_id == bd_user_id,
                BDStat.congo_id == congo_id,
                BDStat.bd_year == extract('year', func.current_date())
            )
        )
        request = await self.session.execute(sql)
        user = request.scalar()
        return user

    async def add_db_stat_user(self,
                               bd_user_id: int,
                               bd_user_name: str,
                               congo_id: int,
                               congo_name: str
                               ):
        bd_user = BDStat(
            bd_user_id=bd_user_id,
            bd_user_name=bd_user_name,
            congo_id=congo_id,
            congo_name=congo_name
        )
        self.session.add(bd_user)
        return bd_user

    async def get_user_gratzed(self, user_id):
        sql = select(func.count("*"), BDStat.bd_year).select_from(BDStat).where(
            BDStat.congo_id == user_id
        ).group_by(BDStat.bd_year)
        result = await self.session.execute(sql)
        scalars = result.all()
        return scalars

    async def get_user_rcvd_gratzed(self, user_id):
        sql = select(func.count("*"), BDStat.bd_year).select_from(BDStat).where(
            BDStat.bd_user_id == user_id
        ).group_by(BDStat.bd_year)
        result = await self.session.execute(sql)
        scalars = result.all()
        return scalars

    async def delete_me_from_bd_stat_r(self, user_id):
        sql = delete(BDStat).where(BDStat.bd_user_id == user_id)
        result = await self.session.execute(sql)
        return result

    async def delete_me_from_bd_stat_g(self, user_id):
        sql = delete(BDStat).where(BDStat.congo_id == user_id)
        result = await self.session.execute(sql)
        return result
