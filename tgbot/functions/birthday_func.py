from datetime import date

from dateutil import relativedelta

today = date.today()


async def birthday_btn(user) -> tuple:
    if user.user_bd:
        user_bd = user.user_bd
        user_bd_today = today.replace(month=user_bd.month, day=user_bd.day)
        if today > user_bd_today:
            bd = user_bd_today.replace(year=date.today().year + 1)
            days_left = bd - today
        else:
            days_left = user_bd_today - today
        age = relativedelta.relativedelta(today, user_bd)
        return days_left.days, age.years
    else:
        return None, None


def birthday_cmnd(parsed_dt) -> tuple:
    bd = today.replace(month=parsed_dt.month, day=parsed_dt.day)
    age = relativedelta.relativedelta(today, bd)
    if today > bd:
        bd = bd.replace(year=date.today().year + 1)
        days_left = bd - today
    else:
        days_left = bd - today
    return days_left.days, age.years
