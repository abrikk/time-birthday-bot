def get_date_order(user_lang: str) -> str:
    if user_lang in ["ru", "uz", "uk", "es", "fr"]:
        date_order = "DMY"
    else:
        date_order = "YMD"
    return date_order


def get_locale_date_order(date_order: str):
    if date_order == "DMY":
        date_order = ["%d%m%Y", "%d%m%Y"]
    else:
        date_order = ["%Y%m%d", "%y%m%d"]
    return date_order
