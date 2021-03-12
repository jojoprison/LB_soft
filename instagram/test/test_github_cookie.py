import pickle
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import http.cookies

from instagram.instagram_bot import get_project_root_path


def login_with_cookies():
    driver = webdriver.Chrome(f'{get_project_root_path()}/drivers/chromedriver.exe')

    driver.get('https://github.com/')
    time.sleep(5)

    for cookie in pickle.load(open('coci', 'rb')):
        driver.add_cookie(cookie)

    time.sleep(5)

    print('load cookies')
    driver.refresh()


def login_parse_cookies():
    driver = webdriver.Chrome(f'{get_project_root_path()}/drivers/chromedriver.exe')

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

    pickle.dump(driver.get_cookies(), open('coci', 'wb'))

    print('got cookies')


def login_livelib_parse():
    driver = webdriver.Chrome(f'{get_project_root_path()}/drivers/chromedriver.exe')

    driver.get('https://www.livelib.ru/')

    login = 'egyabig2@gmail.com'
    passw = '149367139diez'

    time.sleep(5)

    username_input = driver.find_element_by_id('checkin-email-block')
    username_input.clear()
    username_input.send_keys(login)
    btn = username_input.parent
    btn = driver.find_element_by_tag_name('button')
    print(btn)
    btn.click()

    time.sleep(2)

    password_input = driver.find_element_by_name('user[password]')
    password_input.clear()
    password_input.send_keys(passw)

    password_input.send_keys(Keys.ENTER)
    time.sleep(10)

    pickle.dump(driver.get_cookies(), open('coci', 'wb'))

    print('got cookies')


def login_livelib_w_cookies():
    driver = webdriver.Chrome(f'{get_project_root_path()}/drivers/chromedriver.exe')

    driver.get('https://www.livelib.ru/')
    time.sleep(5)

    for cookie in pickle.load(open('coci', 'rb')):
        driver.add_cookie(cookie)

    time.sleep(5)

    print('load cookies')
    driver.refresh()

    time.sleep(15)


if __name__ == '__main__':
    # login_livelib_parse()
    login_livelib_w_cookies()
