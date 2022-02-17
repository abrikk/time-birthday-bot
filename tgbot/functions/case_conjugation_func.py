from tgbot.middlewares.lang_middleware import _


def day_conjugation(days_left: int, what: str = "default") -> str:
    conjugated_words = {
        1: _("день"),
        2: _("дня"),
        3: _("дней")
    }
    if what == "default":
        days_left_str = str(days_left)[-1]
        if days_left_str.endswith("1"):
            day = conjugated_words[1]
        elif days_left_str.endswith(("2", "3", "4")):
            day = conjugated_words[2]
        else:
            day = conjugated_words[3]
        return day
    elif what == "word_day":
        if days_left == 1:
            day = conjugated_words[1]
        elif days_left in (2, 3, 4):
            day = conjugated_words[2]
        else:
            day = conjugated_words[3]
        return day


def year_conjuction(years: int, what: str = "default") -> str:
    conjugated_words = {
        1: _("год"),
        2: _("года"),
        3: _("лет")
    }
    if what == "default":
        year_str = str(years)[-1]
        if year_str.endswith("1"):
            year = conjugated_words[1]
        elif year_str.endswith(("2", "3", "4")):
            year = conjugated_words[2]
        else:
            year = conjugated_words[3]
        return year
    elif what == "word_year":
        if years == 1:
            year = conjugated_words[1]
        elif years in (2, 3, 4):
            year = conjugated_words[2]
        else:
            year = conjugated_words[3]
        return year


def month_conjuction(months: int, what: str = "default") -> str:
    conjugated_words = {
        1: _("месяц"),
        2: _("месяца"),
        3: _("месяцев")
    }
    if what == "default":
        month_str = str(months)[-1]
        if month_str.endswith("1"):
            month = conjugated_words[1]
        elif month_str.endswith(("2", "3", "4")):
            month = conjugated_words[2]
        else:
            month = conjugated_words[3]
        return month
    elif what == "word_month":
        if months == 1:
            month = conjugated_words[1]
        elif months in (2, 3, 4):
            month = conjugated_words[2]
        else:
            month = conjugated_words[3]
        return month


def left_conjunction(days_left: int) -> str:
    left = _("остался") if days_left == 1 else _("осталось")
    return left


def whom_conjuction(sex: int) -> str:
    whom = _("Ему") if sex == "1" else _("Ей")
    return whom
