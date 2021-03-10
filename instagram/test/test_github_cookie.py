import time

import requests
from selenium.webdriver.common.keys import Keys

from instagram.config import USERNAME, PASSWORD
from bs4 import BeautifulSoup
from selenium import webdriver

from instagram.instagram_bot import InstagramBot

if __name__ == '__main__':
    driver = webdriver.Chrome("../../drivers/chromedriver.exe")

    driver.get('https://github.com/login')

    login = 'squalorDf'
    passw = 'ololo149367139Diez'

    username_input = driver.find_element_by_id('login_field')
    username_input.clear()
    username_input.send_keys(login)

    time.sleep(2)

    password_input = driver.find_element_by_id('password')
    password_input.clear()
    password_input.send_keys(passw)

    password_input.send_keys(Keys.ENTER)
    time.sleep(4)

    print(driver.get_cookies())
