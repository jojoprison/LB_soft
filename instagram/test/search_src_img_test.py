from bs4 import BeautifulSoup
from selenium import webdriver

from instagram.config import *

from instagram.instagram_bot import InstagramBot

import requests
from os import system


def test(page_source):
    soup = BeautifulSoup(page_source, "html.parser")

    ass = soup.find_all('a')
    print(ass)

    # for a in ass:
        # print(a)

    # gender_label = soup.find('label', {'for': 'pepGender'})
    # div_gender = gender_label.parent.parent
    # gender = div_gender.find('input')
    # print(gender['value'])


if __name__ == '__main__':

    # driver = webdriver.Chrome("../../drivers/chromedriver.exe")

    proxy = '188.168.81.158'
    port = '9050'

    profile = webdriver.FirefoxProfile()
    profile.set_preference("network.proxy.type", 1)
    profile.set_preference("network.proxy.http", proxy)
    profile.set_preference("network.proxy.http_port", port)
    profile.set_preference("network.proxy.ssl", proxy)
    profile.set_preference("network.proxy.ssl_port", port)

    driver = webdriver.Firefox(firefox_profile=profile, executable_path='../../drivers/geckodriver.exe')

    bot = InstagramBot(driver=driver, username=USERNAME_2, password=PASSWORD_2)

    bot.login()

    bot.driver.get('https://www.instagram.com/p/CHScg64ncRs/')

    test(bot.driver.page_source)

    # try:
    #     elem = bot.driver.find_element_by_class_name('savefrom-helper--btn')
    #     print(elem.text)
    #     exist = True
    # except NoSuchElementException:
    #     exist = False

    # print(exist)
