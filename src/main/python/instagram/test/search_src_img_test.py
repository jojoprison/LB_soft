import pathlib

from bs4 import BeautifulSoup
from selenium import webdriver

from instagram.config import *
from instagram.instagram import InstagramBot
from instagram.instagram import get_resources_path


def find_a(page_source):
    soup = BeautifulSoup(page_source, "html.parser")

    # ass = soup.find_all('a')
    # print(ass)
    # for a in ass:
    #     print(a)

    a_cl = soup.find("img", class_="FFVAD")
    print(a_cl)

    # tree = html.fromstring(page_source)
    # acs = tree.xpath('/html/body/div[1]/section/main/div/div[1]/article/div[2]/'
    #                  'div/div[1]/div[2]/div/div/div/ul/li[2]/div/a')
    # print(acs)

    # gender_label = soup.find('label', {'for': 'pepGender'})
    # div_gender = gender_label.parent.parent
    # gender = div_gender.find('input')
    # print(gender['value'])


if __name__ == '__main__':

    proxy = '188.168.81.158'
    port = '9050'

    profile = webdriver.FirefoxProfile()
    profile.set_preference("network.proxy.type", 1)
    profile.set_preference("network.proxy.http", proxy)
    profile.set_preference("network.proxy.http_port", port)
    profile.set_preference("network.proxy.ssl", proxy)
    profile.set_preference("network.proxy.ssl_port", port)

    driver = webdriver.Firefox(firefox_profile=profile,
                               executable_path=f'{get_resources_path()}/drivers/geckodriver.exe')

    bot = InstagramBot(username=USERNAME_2, password=PASSWORD_2, driver=driver)

    bot.login()

    bot.driver.get('https://www.instagram.com/p/CKOetnuHmro/')

    find_a(bot.driver.page_source)

    # try:
    #     elem = bot.driver.find_element_by_class_name('savefrom-helper--btn')
    #     print(elem.text)
    #     exist = True
    # except NoSuchElementException:
    #     exist = False
    #
    # print(exist)
