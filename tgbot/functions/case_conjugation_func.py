from tgbot.middlewares.lang_middleware import _


def day_conjugation(days_left: int) -> str:
    days_left_str = str(days_left)[-1]
    if days_left_str.endswith("1"):
        day = _("день")
    elif days_left_str.endswith(("2", "3", "4")):
        day = _("дня")
    else:
        day = _("дней")
    return day


def year_conjuction(years: int) -> str:
    year_str = str(years)[-1]
    if year_str.endswith("1"):
        year = _("год")
    elif year_str.endswith(("2", "3", "4")):
        year = _("года")
    else:
        year = _("лет")
    return year


def left_conjunction(days_left: int) -> str:
    left = _("остался") if days_left == 1 else _("осталось")
    return left


def whom_conjuction(sex: int) -> str:
    whom = _("Ему") if sex == "1" else _("Ей")
    return whom
