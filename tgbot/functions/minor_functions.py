def get_date_order(user_lang: str) -> str:
    if user_lang in ["ru", "uz", "uk", "es", "fr"]:
        date_order = "DMY"
    else:
        date_order = "YMD"
    return date_order
