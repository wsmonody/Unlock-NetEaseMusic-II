# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00202FCDDC5E1112AB11D5D6BF07419F3021E1D397823E9F59AF0802B22873E9FF64141A21EF3012EE02485D65C88EDF304B4048E07F5F0E5D2BBEBBA4ACCD8C709EE070491E1998460D498EED049AE807A522AEAED3EE7D1689A3A596A5DEB3B1905A84941A7E6B8B36A0A3D9F7314CAEDBB274E0E469A00CCFA87CA373E37BDED93B17C97231A35D35C6AE88110FE01C8F75D92B28A0AED86BCF84C3309FAE947BB127DEDAD1A42833D903D43F1B62109D0BEEBF102C84BE099FDD24E5BDC3C49F0B975FC8D782D102BB5FF730104BE09D7070BFD32710D6F45C807B30E6FCE8F5A74D1839856B44C7FA7D8080B62F0918E4A2813E4AF613C0D2384706768853C2555E1D84D256A0093B43BA393EB2DD37B840CC61170A0E4C6BF0B0512DEB8CDE724795700B1C69BB176EA468CE5A4E0D3AD4F4705ED6560337D4CD81EAD235374795C0802173B7CD65C3D339197FD47DE6BF80A3D975B5BB3C986C07C60E11"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
