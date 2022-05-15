import logging
import random
import time

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Command
from aiogram.types import InputFile
from aiogram.utils.markdown import hcode
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


async def update_hide_link(message: types.Message, db_commands, session):
    bot = message.bot
    config = bot.get('config')
    # "--headless",
    options = Options()
    list_of_options = [
        "--headless", "user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0",
        "--disable-blink-features=AutomationControlled", "start-maximized",
        "disable-infobars", "--disable-extensions"]
    for option in list_of_options:
        options.add_argument(option)

    s = Service(executable_path='/home/abror/chromedriver')
    driver = webdriver.Chrome(service=s, options=options)

    all_holidays = await db_commands.get_holidays_en_name()
    driver.get("https://www.yandex.com/images/")
    driver.set_page_load_timeout(10)
    try:
        for hol, uid in all_holidays:
            box = driver.find_element(By.TAG_NAME, 'input')
            box.clear()
            box.send_keys(hol + " holiday")
            box.send_keys(Keys.ENTER)

            driver.implicitly_wait(10)
            driver.refresh()
            while True:
                try:
                    await message.answer(f"Started doing -- {hol}")
                    driver.refresh()
                    driver.find_elements(By.CLASS_NAME, "serp-item__thumb")[random.randint(1, 11)].click()
                    driver.find_element(By.CLASS_NAME, "MMButton-Text").click()

                    driver.switch_to.window(driver.window_handles[1])
                    driver.implicitly_wait(5)
                    photo_url = driver.current_url
                    print(photo_url)
                    photo = await bot.send_photo(chat_id=config.tg_bot.channel_id, photo=InputFile.from_url(photo_url),
                                                 caption=f"{hol} - {hcode(uid)}")
                    break
                except Exception as e:
                    logging.info(e)
                    time.sleep(5)
                    driver.close()
                    time.sleep(5)
                    driver.implicitly_wait(5)
                    time.sleep(5)
                    driver.switch_to.window(driver.window_handles[0])
                    time.sleep(5)
                    driver.back()
                    driver.implicitly_wait(5)
                    continue

            await db_commands.update_hol_hide_link(uid, photo.photo[-1].file_id)
            await session.commit()

            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            driver.back()
    except Exception as ex:
        print(ex)
    finally:
        print("I WILL BE CLOSED IN 10 SECONDS")
        time.sleep(10)
        driver.quit()
        print("CLOSED")



    # link = 'https://i.dailymail.co.uk/1s/2019/12/06/10/21866488-7760367-People_buy_television_sets_at_a_supermarket_during_a_discount_ca-a-59_1575629125894.jpg'
    # await bot.send_photo(chat_id=config.tg_bot.channel_id, photo=link)
    # print(type(pic))
    # print(pic)
    # print(pic.photo[-1])
    # print(pic.photo[-1].file_id)


async def edited_hide_link(message: types.Message):
    await message.answer("EDITED MESSAGE")


def register_upd_hide_links(dp: Dispatcher):
    dp.register_message_handler(update_hide_link, Command("upd_hide_link"))
    dp.register_edited_message_handler(edited_hide_link)
