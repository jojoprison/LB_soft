import json
import pickle
import random
import sys
import time
from pathlib import Path
import traceback

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
# TODO заменить селеинум на это, если нужна авторизация через прокси
# from seleniumwire import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from instagram.config import users_settings_dict, sms_activate_api
from instagram.util.paths import *
from instagram.util.urls import generate_user_url, parse_username

from smsactivateru import Sms, SmsTypes, SmsService, GetNumber, SetStatus, GetStatus

second_user_dict = list(users_settings_dict.values())[1]
USERNAME = second_user_dict['login']
PASSWORD = second_user_dict['password']
WINDOW_SIZE = second_user_dict['window_size']


class InstagramBot:
    username = None
    password = None
    window_size = None
    driver = None
    proxy = None
    user_agent = None

    def __init__(self, username=None, password=None, window_size=None, driver=None):
        if not username:
            username = USERNAME
        if not password:
            password = PASSWORD

        if not window_size:
            window_size = WINDOW_SIZE

        if not driver:

            driver_name_list = ['chrome', 'firefox']
            # выбираем браузер из списка
            driver_name = random.choice(driver_name_list)

            # user_agent
            # print('get user_agent...')
            # self.user_agent = user_agent = UserAgent(cache=False, use_cache_server=False).random
            # print('user_agent: ', user_agent)

            # proxy
            # print('get proxy...')
            # self.proxy = proxy = random_proxy()
            # proxy_str = parse(proxy).proxy_signature()

            # self.proxy = proxy = '195.85.171.203:3128'
            # proxy_str = proxy

            # print(proxy_str)
            proxy_str = None

            # driver_name = 'chrome'

            if driver_name == 'chrome':
                chrome_options = ChromeOptions()
                # скрывает окно браузера
                # options.add_argument(f'--headless')
                # изменяет размер окна браузера
                chrome_options.add_argument(f'--window-size={window_size}')
                chrome_options.add_argument("--incognito")
                # вырубаем палево с инфой что мы webdriver
                chrome_options.add_argument('--disable-blink-features=AutomationControlled')
                # TODO протестить такой usage прокси
                # chrome_options.add_argument(f'--proxy-server={proxy_str}')
                # user-agent
                # chrome_options.add_argument(f'user-agent={user_agent}')
                # headless mode
                # chrome_options.headless = True

                # chrome_options.add_experimental_option("mobileEmulation",
                #                                        {"deviceName": "Galaxy S5"})  # or whatever

                if proxy_str:
                    chrome_options.add_argument(f'--proxy-server={proxy_str}')

                driver = webdriver.Chrome(executable_path=ChromeDriverManager(cache_valid_range=7).install(),
                                          options=chrome_options)

                driver.delete_all_cookies()
            else:
                firefox_profile = webdriver.FirefoxProfile()
                # меняем user-agent, можно через FirefoxOptions если ЧЕ
                # firefox_profile.set_preference('general.useragent.override', user_agent)
                firefox_profile.set_preference('dom.file.createInChild', True)
                # firefox_profile.set_preference('font.size.variable.x-western', 14)
                # firefox_profile.set_preference("permissions.default.desktop-notification", 1)
                # firefox_profile.set_preference("dom.webnotifications.enabled", 1)
                # firefox_profile.set_preference("dom.push.enabled", 1)
                # firefox_profile.set_preference('browser.download.manager.showWhenStarting', False)
                # firefox_profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv')
                # firefox_profile.set_preference("browser.link.open_newwindow", 3)
                # firefox_profile.set_preference("browser.link.open_newwindow.restriction", 2)

                # proxy
                # firefox_profile.set_preference("network.proxy.type", 1)
                # firefox_profile.set_preference("network.proxy.http", proxy)
                # firefox_profile.set_preference("network.proxy.http_port", port)
                # firefox_profile.set_preference("network.proxy.ssl", proxy)
                # firefox_profile.set_preference("network.proxy.ssl_port", port)

                # firefox_profile.set_preference("places.history.enabled", False)
                firefox_profile.set_preference("privacy.clearOnShutdown.offlineApps", True)
                firefox_profile.set_preference("privacy.clearOnShutdown.passwords", True)
                firefox_profile.set_preference("privacy.clearOnShutdown.siteSettings", True)
                firefox_profile.set_preference("privacy.sanitize.sanitizeOnShutdown", True)
                # firefox_profile.set_preference("signon.rememberSignons", False)
                firefox_profile.set_preference("network.cookie.lifetimePolicy", 2)
                firefox_profile.set_preference("network.dns.disablePrefetch", True)
                firefox_profile.set_preference("network.http.sendRefererHeader", 0)
                # firefox_profile.set_preference("javascript.enabled", False)

                firefox_profile.update_preferences()

                if proxy_str:
                    firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
                    firefox_capabilities['marionette'] = True

                    firefox_capabilities['proxy'] = {
                        'proxyType': 'MANUAL',
                        'httpProxy': proxy_str,
                        'ftpProxy': proxy_str,
                        'sslProxy': proxy_str
                    }
                else:
                    firefox_capabilities = None

                firefox_options = FirefoxOptions()
                # размер окна браузера
                firefox_options.add_argument(f'--width={window_size.split(",")[0]}')
                firefox_options.add_argument(f'--height={window_size.split(",")[1]}')
                # вырубаем палево с инфой что мы webdriver
                firefox_options.set_preference('dom.webdriver.enabled', False)
                # headless mode
                # firefox_options.headless = True

                # инициализируем firefox
                driver = webdriver.Firefox(firefox_profile=firefox_profile,
                                           capabilities=firefox_capabilities,
                                           executable_path=GeckoDriverManager(cache_valid_range=7).install(),
                                           options=firefox_options,
                                           service_log_path=f'{get_instagram_module_path()}/logs/geckodriver.log')

        driver.delete_all_cookies()

        self.username = username
        self.password = password
        self.driver = driver

    # метод для закрытия браузера
    def close_driver(self):
        self.driver.close()
        self.driver.quit()

    def wait_and_close_driver(self):
        input('ERROR, Press enter if you want to stop browser right now')
        self.close_driver()
        sys.exit()

    # метод логина
    def login(self):

        driver = self.driver
        driver.get('https://www.instagram.com')
        time.sleep(random.randrange(2, 4))

        # путь к кукисам для юзера
        cookies_file_path = f'{get_user_directory_path(self.username)}/{self.username}_cookies'

        # логинимся через кукисы, если есть
        if os.path.exists(cookies_file_path):
            driver.delete_all_cookies()
            driver.execute_script("window.localStorage.clear()")

            for cookie in pickle.load(open(cookies_file_path, 'rb')):
                driver.add_cookie(cookie)

            time.sleep(2)

            print('load cookies')
            driver.refresh()

            time.sleep(5)
        # если нет - логинимся по стандарту
        else:
            username_input = driver.find_element_by_name('username')
            username_input.clear()
            username_input.send_keys(self.username)

            time.sleep(2)

            password_input = driver.find_element_by_name('password')
            password_input.clear()
            password_input.send_keys(self.password)

            password_input.send_keys(Keys.ENTER)
            time.sleep(7)

            # сразу запишем кукисы))
            pickle.dump(driver.get_cookies(), open(cookies_file_path, 'wb'))

            not_now_btn = driver.find_element_by_class_name('cmbtv')
            not_now_btn.click()

            time.sleep(4)

        # проверяем, есть ли окно алертов
        notification_dialog_search_pattern = '[role="dialog"]'
        if self.exist_element(notification_dialog_search_pattern, By.CSS_SELECTOR):
            # закрываем окно алертов
            notification_dialog = driver.find_element(By.CSS_SELECTOR, '[role="dialog"]')
            off_notifications = notification_dialog.find_element_by_xpath(
                './/div/div/div[3]/button[2]')
            off_notifications.click()

            time.sleep(3)

    def get_account_info(self):

        driver = self.driver

        # старый код через тыки по иконкам
        # user_profile_xpath = '//div[@data-testid="user-avatar"]'
        # user_account_link = driver.find_element_by_xpath(user_profile_xpath)
        # user_account_link = driver.find_element_by_link_text(USERNAME)
        # user_account_link.click()
        driver.get(f'https://www.instagram.com/{self.username}/')

        time.sleep(3)

        edit_profile_btn = driver.find_element(
            By.CSS_SELECTOR, '[href="/accounts/edit/"]')
        edit_profile_btn.click()

        time.sleep(3)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        name = soup.find('input', id='pepName')
        print(name['value'])

        username = soup.find('input', id='pepUsername')
        print(username['value'])

        website = soup.find('input', id='pepWebsite')
        print(website['value'])

        bio = soup.find('textarea', id='pepBio')
        print(bio.get_text())

        email = soup.find('input', id='pepEmail')
        print(email['value'])

        phone = soup.find('input', id='pepPhone Number')
        print(phone['value'])

        gender_label = soup.find('label', {'for': 'pepGender'})
        div_gender = gender_label.parent.parent
        gender = div_gender.find('input')
        print(gender['value'])

        driver.back()
        time.sleep(10)

    def reg_account(self, username, password, email=None, name=None):
        driver = self.driver
        driver.get('https://www.instagram.com')
        time.sleep(random.randrange(2, 4))

        reg_btn = driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[2]/div/p/a/span')
        reg_btn.click()
        time.sleep(random.randrange(2, 4))

        phone_number, activation = get_phone_number()

        if phone_number:

            name_or_phone_textbox = driver.find_element_by_name('emailOrPhone')
            name_or_phone_textbox.clear()
            name_or_phone_textbox.send_keys(phone_number)

            time.sleep(2)

            if name:
                fullname_textbox = driver.find_element_by_name('fullName')
                fullname_textbox.clear()
                fullname_textbox.send_keys(name)

                time.sleep(2)

            username_textbox = driver.find_element_by_name('username')
            username_textbox.clear()
            username_textbox.send_keys(username)

            time.sleep(2)

            password_textbox = driver.find_element_by_name('password')
            password_textbox.clear()
            password_textbox.send_keys(password)

            time.sleep(2)

            error_phone = 'Похоже, вы неверно указали номер телефона. Введите полный номер с кодом страны.'
            error_username = 'Это имя пользователя уже занято. Попробуйте другое.'

            # TODO в случае если недоступны какие то части рег инфы
            while True:
                password_textbox.send_keys(Keys.ENTER)

                time.sleep(3)

                try:
                    error_alert = driver.find_element_by_id('ssfErrorAlert')
                    error_alert_value = error_alert.text

                    if error_alert_value == error_username:
                        print('что то сделать если неправильно введен юзернейм')
                    elif error_alert_value == error_phone:
                        print('что то сделать если неправильно введен номер телефона')

                except Exception as e:
                    print(e)

                break

            time.sleep(2)

            birth_month_selection_xpath_first = '/html/body/div[1]/section/main/article/div[2]' \
                                                '/div[1]/div/div[4]/div/div/span/span[1]/select'
            birth_month_selection_xpath_second = '/html/body/div[1]/section/main/div/div/' \
                                                 'div[1]/div/div[4]/div/div/span/span[1]/select'

            if self.exist_element(birth_month_selection_xpath_first):
                birth_month_selection = Select(driver.find_element_by_xpath(birth_month_selection_xpath_first))
            elif self.exist_element(birth_month_selection_xpath_second):
                birth_month_selection = Select(driver.find_element_by_xpath(birth_month_selection_xpath_second))
            else:
                birth_month_selection = None

            random_month = random.randrange(11)
            if birth_month_selection:
                birth_month_selection.select_by_index(random_month)
            else:
                print('month selection not founded')

            time.sleep(2)

            birth_day_selection_xpath = '/html/body/div[1]/section/main/div/div/' \
                                        'div[1]/div/div[4]/div/div/span/span[2]/select'
            birth_day_selection = Select(driver.find_element_by_xpath(birth_day_selection_xpath))

            random_day = random.randrange(29)
            birth_day_selection.select_by_index(random_day)

            time.sleep(2)

            birth_year_selection_xpath = '/html/body/div[1]/section/main/div/div/' \
                                         'div[1]/div/div[4]/div/div/span/span[3]/select'
            birth_year_selection = Select(driver.find_element_by_xpath(birth_year_selection_xpath))

            random_year = random.randrange(1975, 2007)
            birth_year_selection.select_by_value(str(random_year))

            time.sleep(2)

            button_next_xpath = '/html/body/div[1]/section/main/div/div/div[1]/div/div[6]/button'
            button_next = driver.find_element_by_xpath(button_next_xpath)
            button_next.click()

            time.sleep(3)

            if activation:
                print('activation exist')
                sms_code = get_sms_code(activation)
            else:
                sms_code = 123456

            sms_code_input_xpath = '/html/body/div[1]/section/main/div/div/' \
                                   'div[1]/div/div/div/form/div[1]/div/label/input'
            sms_code_input = driver.find_element_by_xpath(sms_code_input_xpath)
            # TODO придумать как вводить код посимвольно
            sms_code_input.send_keys(sms_code)
            time.sleep(2)
            sms_code_input.send_keys(Keys.ENTER)

            # сохраняем всех подписчиков пользователя в файл
            with open(f'{get_instagram_module_path()}/accounts.txt', 'a') as accounts_file:
                accounts_file.write(username + ':' + password +
                                    ', ' + str(phone_number) + '\n')

            time.sleep(10)
        else:
            print('phone number not exist, try again')
            return None

    # метод ставит лайки по hashtag
    def like_hashtag(self, hashtag, likes_count, randomize):

        driver = self.driver
        driver.get(f'https://www.instagram.com/explore/tags/{hashtag}/')
        time.sleep(5)

        for i in range(1, 2):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.randrange(3, 5))

        hrefs = driver.find_elements_by_tag_name('a')
        posts_urls = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]
        print(posts_urls)

        if posts_urls:
            # TODO еще юзать likes_count
            # for url in posts_urls:
            url = posts_urls[0]
            try:
                driver.get(url)
                time.sleep(3)

                is_liked = self.like_button_click()

                # TODO изменить паузу чтоб не спалиться
                time.sleep(random.randrange(5, 10))
            except Exception as ex:
                print(ex)
                self.wait_and_close_driver()
        else:
            print(f'постов по хештегу #{hashtag} нет :(')

    def like_button_click(self):
        like_button_xpath = '/html/body/div[1]/section/main/div/div[1]/article/' \
                            'div[3]/section[1]/span[1]/button'

        like_button = self.driver.find_element_by_xpath(like_button_xpath)

        # проверяем, стоит ли уже лайк на посте
        is_liked_xpath = like_button.find_element_by_tag_name('svg')
        is_liked = is_liked_xpath.get_attribute('fill')

        # 262626 лайк не стоит - не закрашено сердечко
        # #ed4956
        if is_liked == '#262626':
            self.driver.execute_script("arguments[0].click();", like_button)

            return True
        else:
            return False

    # метод ставит лайк на пост по прямой ссылке
    def like_post(self, post):

        if self.post_exist(post):
            print(f'Ставим лайк на пост: {post}')
            time.sleep(2)

            is_liked = self.like_button_click()

            time.sleep(2)

            print(f'Лайк на пост: {post} поставлен!')
        else:

            self.wait_and_close_driver()

    # метод оставляет коммент под постом по прямой ссылке
    def comment_post(self, post_url, comment):

        if self.post_exist(post_url):
            print(f'Ставим коммент к посту {post_url}')
            time.sleep(2)

            # заполняем textarea с комментом нужным текстом
            comment_textarea_xpath = '/html/body/div[1]/section/main/div/div[1]' \
                                     '/article/div[3]/section[3]/div/form/textarea'
            comment_textarea = self.driver.find_element_by_xpath(comment_textarea_xpath)
            # сначала кликнем, без клика по ходу не включается event, и элемент not iterable
            comment_textarea.click()

            time.sleep(2)

            try:
                # нужно опять по xpath найти поле с комментом, после нажатия он меняется
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((
                        By.XPATH, comment_textarea_xpath))).send_keys(comment)

            except Exception as e:
                print(e)
                # закрывает бразуер по нажатию чего угодно в консоль, чтоб процессы не плодить
                self.wait_and_close_driver()
                return False

            # ищем кнопку опубликовать и жмякаем ее
            publish_comment_button_xpath = '/html/body/div[1]/section/main/div/div[1]' \
                                           '/article/div[3]/section[3]/div/form/button[2]'

            publish_comment_button = self.driver.find_element_by_xpath(publish_comment_button_xpath)
            publish_comment_button.click()

            time.sleep(2)

            return True
        else:
            # не нашли пост
            self.wait_and_close_driver()
            return False

    # метод оставляет коммент под случайным постом юзера
    def comment_random(self, username, comment):

        # собираем ссылки на посты в файл
        posts_file_name = self.get_posts_url(username)

        # проверяем, не None ли имя файла (может внутри полететь из-за несоблюденных условий)
        if posts_file_name:
            # user_page = generate_user_url(username)
            #
            # self.driver.get(user_page)

            time.sleep(4)

            with open(posts_file_name) as file:
                url_list = file.readlines()
                print('start url_list len:', len(url_list))

            # выбираем рандомну ссылку на пост
            random_post_url = random.choice(url_list)

            try:
                is_commented = self.comment_post(random_post_url, comment)
                if is_commented:
                    print(f'Коммент на пост {random_post_url} успешно поставлен: {comment}')
                else:
                    print(f'Не удалось оставить коммент на пост {random_post_url}: {comment}')

                time.sleep(3)

            except Exception as ex:
                print(ex)
                self.close_driver()

            # удаляем ссылку на пост из списка, чтоб не повторить на нее лайк
            url_list.remove(random_post_url)
            print('updated url_list len: ', len(url_list))

            return True
        else:
            print(f'файла с постами юзера {username} нет...')
            return False

    def comment_hashtag(self, hashtag, comment, count=1, randomize=False):

        # TODO юзать randomize если нужно рандомно сделать дейтсвия, а не последовательно
        self.driver.get(f'https://www.instagram.com/explore/tags/{hashtag}/')
        time.sleep(5)

        for i in range(1, 2):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.randrange(3, 5))

        hrefs = self.driver.find_elements_by_tag_name('a')
        posts_urls = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]
        print(posts_urls)

        if posts_urls:
            # TODO еще юзать count
            # for url in posts_urls:
            post_url = posts_urls[0]
            try:
                is_commented = self.comment_post(post_url, comment)

                # TODO изменить паузу чтоб не спалиться
                time.sleep(random.randrange(5, 10))
            except Exception as ex:
                print(ex)
                self.wait_and_close_driver()
        else:
            print(f'постов по хештегу #{hashtag} нет :(')

    # метод оставляет коммент под постом по прямой ссылке
    def like_comment_post(self, post, comment):

        driver = self.driver

        if self.post_exist(post):
            print('Ставим лайк')
            time.sleep(2)

            is_liked = self.like_button_click()

            time.sleep(2)

            print(f"Лайк на пост: {post} поставлен!")

            print('Ставим коммент')
            time.sleep(2)

            # заполняем textarea с комментом нужным текстом
            comment_textarea_xpath = '/html/body/div[1]/section/main/div/div[1]' \
                                     '/article/div[3]/section[3]/div/form/textarea'
            comment_textarea = driver.find_element_by_xpath(comment_textarea_xpath)
            # сначала кликнем, без клика по ходу не включается event, и элемент not iterable
            comment_textarea.click()

            time.sleep(2)

            try:
                # нужно опять по xpath найти поле с комментом, после нажатия он меняется
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((
                        By.XPATH, comment_textarea_xpath))).send_keys(comment)

            except Exception as e:
                print(e)
                # закрывает бразуер по нажатию чего угодно в консоль, чтоб процессы не плодить
                self.wait_and_close_driver()
                return False

            # ищем кнопку опубликовать и жмякаем ее
            publish_comment_button_xpath = '/html/body/div[1]/section/main/div/div[1]' \
                                           '/article/div[3]/section[3]/div/form/button[2]'

            publish_comment_button = driver.find_element_by_xpath(publish_comment_button_xpath)
            publish_comment_button.click()

            time.sleep(2)

            print(f'Коммент "{comment}" оставлен к посту: {post}')

            return True
        else:
            # не нашли пост
            self.wait_and_close_driver()
            return False

    # метод собирает ссылки на все посты пользователя
    def get_posts_url(self, username):

        user_page = generate_user_url(username)

        self.driver.get(user_page)
        time.sleep(4)

        wrong_user_page = "/html/body/div[1]/section/main/div/h2"

        if self.exist_element(wrong_user_page):
            print("Такого пользователя не существует, проверьте URL")
            self.close_driver()

            return None
        else:
            print('Пользователь успешно найден, начинаю собирать ссылки...')
            time.sleep(2)

            if not self.check_acc_private():

                post_count_xpath_1 = '/html/body/div[1]/section/main/div/header/section/ul/li[1]/span/span'
                post_count_xpath_2 = '/html/body/div[1]/section/main/div/ul/li[1]/span/span'

                if self.exist_element(post_count_xpath_1):
                    posts_count = int(self.driver.find_element_by_xpath(
                        post_count_xpath_1).text.replace(' ', ''))
                else:
                    posts_count = int(self.driver.find_element_by_xpath(
                        post_count_xpath_2).text.replace(' ', ''))

                loops_count = int(posts_count / 12)
                print('loops count: ', loops_count)
                # ставим 1 пролистывание, чтобы не уходить далеко вниз по ссылкам (ДЛЯ ТЕСТА)
                # значение 0 проверяем в любом случае, а то вообще не зайдем в цикл нижний
                if loops_count == 0 or loops_count > 1:
                    loops_count = 1

                posts_urls = []

                for i in range(0, loops_count):

                    hrefs = self.driver.find_elements_by_tag_name('a')
                    hrefs = [item.get_attribute('href') for item in hrefs
                             if "/p/" in item.get_attribute('href')]

                    for href in hrefs:
                        posts_urls.append(href)

                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                    time.sleep(random.randrange(2, 4))

                    print(f"Итерация #{i}")

                posts_url_set = set(posts_urls)
                posts_url_list = list(posts_url_set)
                print(posts_url_list)

                posts_file_name = get_user_posts_file_path(username)

                # очищает файл перед открытием во избежании повторений, дополняем файл постами
                with open(posts_file_name, 'w') as file:
                    for post_url in posts_url_list:
                        file.write(post_url + '\n')

                return posts_file_name
            else:
                print(f'аккаунт {username} приватный')
                self.wait_and_close_driver()
                return None

    # метод ставит несколько лайков по ссылке на аккаунт пользователя
    def like_multiple(self, username, likes_count):

        # собираем ссылки на посты в файл
        posts_file_name = self.get_posts_url(username)

        # проверяем, не None ли имя файла (может внутри полететь из-за несоблюденных условий)
        if posts_file_name:
            user_page = generate_user_url(username)

            driver = self.driver
            driver.get(user_page)

            time.sleep(4)

            with open(posts_file_name) as file:
                url_list = file.readlines()

            print('start url_list len:', len(url_list))

            for count in range(likes_count):
                # выбираем рандомну ссылку на пост
                random_post_url = random.choice(url_list)

                try:
                    driver.get(random_post_url)
                    time.sleep(5)

                    is_liked = self.like_button_click()
                    if is_liked:
                        print(f'Лайк на пост: {random_post_url} успешно поставлен!')
                    else:
                        print(f'Лайк на посте уже стоит: {random_post_url}')

                    time.sleep(3)

                except Exception as ex:
                    print(ex)
                    self.close_driver()

                # удаляем ссылку на пост из списка, чтоб не повторить на нее лайк
                url_list.remove(random_post_url)
                print('updated url_list len: ', len(url_list))

            return True
        else:
            print(f'файла с постами юзера {username} нет...')
            return False

    # метод скачивает контент со страницы пользователя
    def download_user_content(self, username):

        driver = self.driver

        # self.get_all_posts_url(username)
        time.sleep(2)

        img_and_video_src_urls = []

        with open(get_user_posts_file_path(username)) as file:

            url_list = file.readlines()

            for post_url in url_list:
                try:
                    driver.get(post_url)
                    time.sleep(3)

                    # TODO поиск по xpath, убрать лишнее, допилить скачку для видосов
                    img_src = "/html/body/div[1]/section/main/div/div[1]/article/" \
                              "div[2]/div/div/div[1]/img"
                    video_src = "/html/body/div[1]/section/main/div/div[1]/article/" \
                                "div[2]/div/div/div[1]/div/div/video"
                    # '/html/body/div[1]/section/main/div/div[1]/article/div[2]/div/div[1]/div[2]/div/div/div/ul/li[2]/div/div/div/div[1]/img'

                    post_id = post_url.split('/')[-2]

                    if self.exist_element():
                        img_src_url = bot.driver.find_element_by_class_name('FFVAD').get_attribute("src")
                        # img_src_url = driver.find_element_by_xpath(img_src).get_attribute("src")

                        img_and_video_src_urls.append(img_src_url)

                        # сохраняем изображение
                        get_img = requests.get(img_src_url)

                        with open(f'{get_user_content_dir_path(username)}/'
                                  f'{post_id}_img.jpg', 'wb') as img_file:
                            img_file.write(get_img.content)

                    elif self.exist_element(video_src):
                        video_src_url = driver.find_element_by_xpath(video_src).get_attribute("src")
                        img_and_video_src_urls.append(video_src_url)

                        # сохраняем видео
                        get_video = requests.get(video_src_url, stream=True)

                        with open(f"{get_user_content_dir_path(username)}/"
                                  f"{post_id}_video.mp4", "wb") as video_file:

                            for chunk in get_video.iter_content(chunk_size=1280 * 1024):
                                if chunk:
                                    video_file.write(chunk)
                    else:
                        img_and_video_src_urls.append(f"{post_url}, нет ссылки!")

                    print(f'Просмотрен контент поста: {post_url}')

                except Exception as ex:
                    print(ex)
                    self.close_driver()

            print('контент успешно скачан')
            self.close_driver()

        with open(f'{get_user_content_dir_path(username)}/'
                  f'!_img_and_video_src_urls.txt', 'a') as file:
            for i in img_and_video_src_urls:
                file.write(i + "\n")

        print('записана инфа о скачанном контенте')

    # подписывается на юзера
    def follow_user(self, username):

        user_url = generate_user_url(username)

        try:
            self.driver.get(user_url)
            time.sleep(random.randrange(3, 7))

            page_owner = user_url.split("/")[-2]

            # конпка редактировать профиль
            edit_profile_btn = '//*[@id="react-root"]/section/main/div/header/section/' \
                               'div[2]/div/a'
            # копнка с галкой о подписке
            subscribed_right_now_first = '//*[@id="react-root"]/section/main/div/header/' \
                                         'section/div[2]/div/div/div[2]/div/span/span[1]/button/div/span'
            subscribed_right_now_second = '/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div[2]/button/div/span'
            subscribed_right_now_third = '//*[@id="react-root"]/section/main/div/header/' \
                                         'section/div[2]/div/div/div[1]/div/button'

            # конпка подписки на закрытый акк
            follow_private_acc_btn = '//*[@id="react-root"]/section/main/div/header/' \
                                     'section/div[2]/div/div/div/button'
            # первый варик подписки на открытый акк
            follow_btn_first = '//*[@id="react-root"]/section/main/div/header/section/' \
                               'div[2]/div/div/div/div/span/span[1]/button'
            # второй варик подписки на открытый акк
            follow_btn_second = '/html/body/div[1]/section/main/div/header/section' \
                                '/div[1]/div[1]/div/div/div/span/span[1]/button'

            time.sleep(1)

            # TODO доделать проверки, придумать проверки через парентов и рядом находящиеся блоки
            if self.exist_element(edit_profile_btn):
                print("Это наш профиль, уже подписан, пропускаем итерацию!")
            elif self.exist_element(subscribed_right_now_first):
                print(f"Уже подписаны, на {page_owner} пропускаем итерацию!")
            elif self.exist_element(subscribed_right_now_second):
                print(f"Уже подписаны, на {page_owner} пропускаем итерацию!")
            elif self.exist_element(subscribed_right_now_third):
                print(f"Уже подписаны, на {page_owner} пропускаем итерацию!")
            else:
                # акк закрыт
                if self.check_acc_private():
                    try:
                        # подписка на закрытый акк
                        self.driver.find_element_by_xpath(follow_private_acc_btn).click()
                        print(f'Запросили подписку на пользователя {page_owner}. Закрытый аккаунт!')
                    except Exception as ex:
                        traceback.print_exc(ex)
                else:
                    try:
                        # подписка открытый акк
                        if self.exist_element(follow_btn_first):
                            self.driver.find_element_by_xpath(follow_btn_first).click()
                            print(f'Подписались на пользователя {page_owner}. Открытый аккаунт!')
                        else:
                            self.driver.find_element_by_xpath(follow_btn_second).click()
                            print(f'Подписались на пользователя {page_owner}. Открытый аккаунт!')
                    except Exception as ex:
                        traceback.print_exc(ex)

                # записываем данные в файл для ссылок всех подписок,
                # если файла нет, создаём, если есть - дополняем
                with open(f'{get_user_directory_path(username)}/'
                          f'{username}_subscribe_list.txt',
                          'a') as subscribe_list_file:
                    subscribe_list_file.write(user_url + '\n')

                # TODO увеличить паузу чтобы избежать палева
                time.sleep(random.randrange(4, 9))

        except Exception as ex:
            traceback.print_exc(ex)

    # метод получения всех подписчиков юзера
    def get_followers(self, username):

        # получаем юрлку акка
        user_url = generate_user_url(username)

        self.driver.get(user_url)
        time.sleep(4)

        wrong_user_page = "/html/body/div[1]/section/main/div/h2"

        if self.exist_element(wrong_user_page):
            print(f"Пользователя {username} не существует, проверьте URL")
            self.close_driver()
        else:
            print(f"Пользователь {username} успешно найден, начинаем скачивать ссылки на подписчиков!")
            time.sleep(2)

            followers_button = self.driver.find_element_by_xpath(
                "/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span")

            followers_count = followers_button.get_attribute('title')
            # followers_count = followers_button.text
            # followers_count = int(followers_count.split(' ')[0])

            # если количество подписчиков больше 999, убираем из числа запятые
            if ',' in followers_count:
                followers_count = int(''.join(followers_count.split(',')))
            else:
                followers_count = int(followers_count.replace(' ', ''))

            print(f"Количество подписчиков: {followers_count}")

            loops_count = int(followers_count / 12)
            # DEBUG ставим 1 пролистывание, чтобы не уходить далеко вниз по ссылкам
            if loops_count > 1:
                loops_count = 1

            print(f"Число итераций: {loops_count}")

            followers_button.click()
            time.sleep(2)

            try:
                followers_ul = self.driver.find_element_by_xpath('/html/body/div[5]/div/div/div[2]')
                followers_urls = []

                for i in range(1, loops_count + 1):
                    self.driver.execute_script(f"arguments[0].scrollTop = arguments[0].scrollHeight", followers_ul)
                    time.sleep(random.randrange(2, 4))
                    print(f"Итерация #{i}")

                all_urls_div = followers_ul.find_elements_by_tag_name("li")

                for url in all_urls_div:
                    url = url.find_element_by_tag_name("a").get_attribute("href")
                    followers_urls.append(url)

                # сохраняем всех подписчиков пользователя в файл
                with open(f'{get_user_directory_path(username)}/{username}_subs.txt', 'w') as text_file:
                    for link in followers_urls:
                        text_file.write(link + "\n")

                return followers_urls

            except Exception as ex:
                print(ex)
                self.wait_and_close_driver()

                return None

    # берет у юзера фолловеров и подписывается на них
    def follow_donors(self, username, randomize=False):

        file_path = f'{get_user_directory_path(username)}/{username}_subs.txt'

        # если файл с фоловверами уже существует
        if Path(file_path).is_file():
            with open(file_path) as text_file:
                follower_url_list = text_file.readlines()

            # если файл с фоловверами пустой, опускаемся ниже
            if len(follower_url_list) == 0:
                pass
        else:
            # если файла нет и он пустой вызываем метод получения фоловверов
            follower_url_list = self.get_followers(username)

            print(follower_url_list)

            for i, follower_url in enumerate(follower_url_list):
                follower_url_list[i] = follower_url.replace('\n', '')

            print(follower_url_list)

        # TODO поменять число чтоб вывело больше, юзать рандомайз
        for user_url in follower_url_list[0:2]:
            try:
                # TODO мб по другому проверять существование файла со списком сабов
                try:
                    with open(f'{get_user_directory_path(username)}/'
                              f'{username}_subscribe_list.txt',
                              'r') as subscribe_list_file:

                        lines = subscribe_list_file.readlines()

                        if user_url in lines:
                            print(f'Мы уже подписаны на {user_url}, переходим к следующему пользователю!')
                            continue

                except Exception as ex:
                    print('Файл со ссылками ещё не создан!')
                    traceback.print_exc(ex)

                self.driver.get(user_url)
                page_owner = user_url.split("/")[-2]

                # конпка редактировать профиль
                edit_profile_btn = '//*[@id="react-root"]/section/main/div/header/section/' \
                                   'div[2]/div/a'
                # копнка с галкой о подписке
                subscribed_right_now_first = '//*[@id="react-root"]/section/main/div/header/' \
                                             'section/div[2]/div/div/div[2]/div/span/span[1]/button/div/span'
                subscribed_right_now_second = '/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div[2]/button/div/span'
                subscribed_right_now_third = '//*[@id="react-root"]/section/main/div/header/' \
                                             'section/div[2]/div/div/div[1]/div/button'

                # конпка подписки на закрытый акк
                follow_private_acc_btn = '//*[@id="react-root"]/section/main/div/header/' \
                                         'section/div[2]/div/div/div/button'
                # первый варик подписки на открытый акк
                follow_btn_first = '//*[@id="react-root"]/section/main/div/header/section/' \
                                   'div[2]/div/div/div/div/span/span[1]/button'
                # второй варик подписки на открытый акк
                follow_btn_second = '/html/body/div[1]/section/main/div/header/section' \
                                    '/div[1]/div[1]/div/div/div/span/span[1]/button'

                time.sleep(1)

                # TODO доделать проверки, придумать проверки через парентов и рядом находящиеся блоки
                if self.exist_element(edit_profile_btn):
                    print("Это наш профиль, уже подписан, пропускаем итерацию!")
                elif self.exist_element(subscribed_right_now_first):
                    print(f"Уже подписаны, на {page_owner} пропускаем итерацию!")
                elif self.exist_element(subscribed_right_now_second):
                    print(f"Уже подписаны, на {page_owner} пропускаем итерацию!")
                elif self.exist_element(subscribed_right_now_third):
                    print(f"Уже подписаны, на {page_owner} пропускаем итерацию!")
                else:
                    time.sleep(random.randrange(4, 8))

                    # акк закрыт
                    if self.check_acc_private():
                        try:
                            # подписка на закрытый акк
                            self.driver.find_element_by_xpath(follow_private_acc_btn).click()
                            print(f'Запросили подписку на пользователя {page_owner}. Закрытый аккаунт!')
                        except Exception as ex:
                            traceback.print_exc(ex)
                    else:
                        try:
                            # подписка открытый акк
                            if self.exist_element(follow_btn_first):
                                self.driver.find_element_by_xpath(follow_btn_first).click()
                                print(f'Подписались на пользователя {page_owner}. Открытый аккаунт!')
                            else:
                                self.driver.find_element_by_xpath(follow_btn_second).click()
                                print(f'Подписались на пользователя {page_owner}. Открытый аккаунт!')
                        except Exception as ex:
                            traceback.print_exc(ex)

                    # записываем данные в файл для ссылок всех подписок,
                    # если файла нет, создаём, если есть - дополняем
                    with open(f'{get_user_directory_path(username)}/'
                              f'{username}_subscribe_list.txt',
                              'a') as subscribe_list_file:
                        subscribe_list_file.write(user_url + '\n')

                    # TODO увеличить паузу чтобы избежать палева
                    time.sleep(random.randrange(7, 15))

            except Exception as ex:
                traceback.print_exc(ex)

    # находит юзеров по хештешгам и фолловит
    def follow_hashtag(self, hashtag, randomize=False):

        self.driver.get(f'https://www.instagram.com/explore/tags/{hashtag}/')
        time.sleep(5)

        for i in range(1, 2):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.randrange(3, 5))

        all_link_list = self.driver.find_elements_by_tag_name('a')
        post_url_list = [item.get_attribute('href') for item in all_link_list if "/p/" in item.get_attribute('href')]

        if post_url_list:
            # TODO еще юзать randomize
            post_link = post_url_list[0]
            try:
                self.driver.get(post_link)
                time.sleep(4)
                # WebDriverWait(self.driver, 3).until(EC.visibility_of(post_link))

                follow_button_xpath_1 = '/html/body/div[5]/div[2]/div/article/header/div[2]/div[1]/div[2]/button'
                follow_button_xpath_2 = '/html/body/div[5]/div/div/article/div[2]/div[1]/header/div[2]/div[1]/div[2]/button'
                follow_button_xpath_3 = '/html/body/div[1]/section/main/div/div[1]/article/header/div[2]/div[1]/div[2]/button'

                if self.exist_element(follow_button_xpath_3):
                    follow_button = self.driver.find_element_by_xpath(follow_button_xpath_3)
                elif self.exist_element(follow_button_xpath_2):
                    follow_button = self.driver.find_element_by_xpath(follow_button_xpath_2)
                else:
                    follow_button = self.driver.find_element_by_xpath(follow_button_xpath_1)

                if follow_button.text == 'Подписаться':
                    follow_button.click()
                    print(f'зафолловил по хештегу #{hashtag}: {post_link}')
                else:
                    print(f'уже фолловит по хештегу #{hashtag} юзера: {post_link}')

                # TODO изменить паузу чтоб не спалиться
                time.sleep(random.randrange(5, 10))
            except Exception as ex:
                # вот в таком виде это исключение печатается
                traceback.print_exception(type(ex), ex, ex.__traceback__)
                self.wait_and_close_driver()
        else:
            print(f'постов по хештегу #{hashtag} нет :(')

    # метод для отправки сообщений в директ
    def direct_user(self, username, message='', img_path=''):

        # self.driver.get(generate_user_url(username))
        # time.sleep(4)

        direct_message_button_1 = "/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[2]/a"
        direct_message_button_2 = '/html/body/div[1]/section/div/div[1]/div/div[3]/div/div[2]/a'

        direct_message_button = None

        if self.exist_element(direct_message_button_2):
            direct_message_button = direct_message_button_2
        elif self.exist_element(direct_message_button_1):
            direct_message_button = direct_message_button_1
        else:
            print('Кнопка отправки сообщений не найдена!')
            self.wait_and_close_driver()

        print('Отправляем сообщение...')
        direct_message = self.driver.find_element_by_xpath(direct_message_button).click()
        time.sleep(random.randrange(3, 7))

        # отключаем всплывающее окно
        if self.exist_element("/html/body/div[4]/div/div"):
            self.driver.find_element_by_xpath("/html/body/div[4]/div/div/div/div[3]/button[2]").click()
            time.sleep(random.randrange(2, 4))

        send_message_button = self.driver.find_element_by_xpath(
            "/html/body/div[1]/section/div/div[2]/div/div/div[2]/div/div[3]/div/button").click()
        time.sleep(random.randrange(2, 4))

        # вводим получателя
        to_input = self.driver.find_element_by_xpath("/html/body/div[5]/div/div/div[2]/div[1]/div/div[2]/input")
        to_input.send_keys(username)
        time.sleep(random.randrange(2, 4))

        # выбираем получателя из списка
        users_list = self.driver.find_element_by_xpath(
            "/html/body/div[5]/div/div/div[2]/div[2]/div/div").find_element_by_tag_name("button").click()
        time.sleep(random.randrange(2, 4))


        next_button = self.driver.find_element_by_xpath(
            "/html/body/div[5]/div/div/div[1]/div/div[2]/div/button").click()
        time.sleep(random.randrange(5, 10))

        # отправка текстового сообщения
        if message:
            text_message_area = self.driver.find_element_by_xpath(
                "/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea")
            text_message_area.clear()
            text_message_area.send_keys(message)

            time.sleep(random.randrange(2, 4))

            text_message_area.send_keys(Keys.ENTER)
            print(f'Сообщение для {username} успешно отправлено!')

            time.sleep(random.randrange(2, 4))

        # отправка изображения
        if img_path:
            send_img_input = self.driver.find_element_by_xpath(
                "/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/form/input")
            send_img_input.send_keys(img_path)

            print(f"Изображение для {username} успешно отправлено!")
            time.sleep(random.randrange(2, 4))

    def direct_users(self, username_list, message=''):

        self.driver.get(generate_user_url(self.username))

        for username in username_list[0:2]:
            self.direct_user(username, message)

    # метод для отправки сообщений в директ
    def direct_donors(self, donor_username, message='', img_path=''):

        followers_url_list = self.get_followers(donor_username)

        followers_list = [parse_username(follower_url) for follower_url in followers_url_list]
        print(followers_list)

        self.direct_users(followers_list, message)

    def direct_group_chat(self, username_list, message=''):

        direct_message_button = "/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[2]/a"

        if not self.exist_element(direct_message_button):
            print("Кнопка отправки сообщений не найдена!")
            self.close_driver()
        else:
            print("Отправляем сообщение...")
            direct_message = self.driver.find_element_by_xpath(direct_message_button).click()
            time.sleep(random.randrange(2, 4))

        # отключаем всплывающее окно
        if self.exist_element("/html/body/div[4]/div/div"):
            self.driver.find_element_by_xpath("/html/body/div[4]/div/div/div/div[3]/button[2]").click()
        time.sleep(random.randrange(2, 4))

        send_message_button = self.driver.find_element_by_xpath(
            "/html/body/div[1]/section/div/div[2]/div/div/div[2]/div/div[3]/div/button").click()
        time.sleep(random.randrange(2, 4))

        # отправка сообщения нескольким пользователям
        for user in username_list[0:3]:
            # вводим получателя
            to_input = self.driver.find_element_by_xpath("/html/body/div[5]/div/div/div[2]/div[1]/div/div[2]/input")
            to_input.send_keys(user)
            time.sleep(random.randrange(2, 4))

            # выбираем получателя из списка
            users_list = self.driver.find_element_by_xpath(
                "/html/body/div[5]/div/div/div[2]/div[2]/div/div").find_element_by_tag_name("button").click()
            time.sleep(random.randrange(2, 4))

        next_button = self.driver.find_element_by_xpath(
            "/html/body/div[5]/div/div/div[1]/div/div[2]/div/button").click()
        time.sleep(random.randrange(5, 10))

        # отправка текстового сообщения
        if message:
            text_message_area = self.driver.find_element_by_xpath(
                "/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea")
            text_message_area.clear()
            text_message_area.send_keys(message)

            time.sleep(random.randrange(2, 4))

            text_message_area.send_keys(Keys.ENTER)
            print(f'Сообщение для {username_list} успешно отправлено!')

            time.sleep(random.randrange(2, 4))

    # метод отписки от всех пользователей
    def unfollow_all(self):

        user_page = generate_user_url(self.username)
        self.driver.get(user_page)

        time.sleep(random.randrange(2, 4))

        following_button = self.driver.find_element_by_xpath(
            "/html/body/div[1]/section/main/div/header/section/ul/li[3]/a")
        following_count = following_button.find_element_by_tag_name("span").text

        # если количество подписчиков больше 999, убираем из числа запятые
        if ',' in following_count:
            following_count = int(''.join(following_count.split(',')))
        else:
            following_count = int(following_count)

        print(f"Количество подписок: {following_count}")

        time.sleep(random.randrange(2, 4))

        loops_count = int(following_count / 10) + 1
        print(f"Количество перезагрузок страницы: {loops_count}")

        following_users_dict = {}

        for loop in range(1, loops_count + 1):

            count = 10
            self.driver.get(user_page)
            time.sleep(random.randrange(3, 6))

            # кликаем/вызываем меню подписок
            following_button = self.driver.find_element_by_xpath(
                "/html/body/div[1]/section/main/div/header/section/ul/li[3]/a")

            following_button.click()
            time.sleep(random.randrange(3, 6))

            # забираем все li из ul, в них хранится кнопка отписки и ссылки на подписки
            following_div_block = self.driver.find_element_by_xpath("/html/body/div[5]/div/div/div[2]/ul/div")
            following_users = following_div_block.find_elements_by_tag_name("li")
            time.sleep(random.randrange(3, 6))

            for user in following_users:

                # вышли за пределы 10, выходим из цикла, обновляем страницу
                if not count:
                    break

                user_url = user.find_element_by_tag_name("a").get_attribute("href")
                user_name = user_url.split("/")[-2]

                # добавляем в словарь пару имя_пользователя: ссылка на аккаунт,
                # на всякий, просто полезно сохранять информацию
                following_users_dict[user_name] = user_url

                following_button = user.find_element_by_tag_name("button").click()
                time.sleep(random.randrange(3, 6))
                unfollow_button = self.driver.find_element_by_xpath(
                    "/html/body/div[6]/div/div/div/div[3]/button[1]").click()

                print(f"Итерация до перезагрузки #{count} >>> Отписался от пользователя {user_name}")
                count -= 1

                # time.sleep(random.randrange(120, 130))
                time.sleep(random.randrange(2, 4))

        with open(f'{get_user_directory_path(self.username)}/'
                  f'{self.username}_following_users_dict.txt', 'w',
                  encoding='utf-8') as file:
            json.dump(following_users_dict, file)

    # метод отписки, отписываемся от всех кто не подписан на нас
    def smart_unsubscribe(self):

        user_page = generate_user_url(self.username)
        self.driver.get(user_page)

        time.sleep(random.randrange(3, 6))

        # кнопка подписчиков
        followers_button = self.driver.find_element_by_xpath(
            "/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span")
        followers_count = followers_button.get_attribute("title")

        # кнопка подписок
        following_button = self.driver.find_element_by_xpath(
            "/html/body/div[1]/section/main/div/header/section/ul/li[3]/a")
        following_count = following_button.find_element_by_tag_name("span").text

        time.sleep(random.randrange(3, 6))

        # если количество подписчиков больше 999, убираем из числа запятые
        if ',' in followers_count or following_count:
            followers_count, following_count = int(''.join(followers_count.split(','))), int(
                ''.join(following_count.split(',')))
        else:
            followers_count, following_count = int(followers_count), int(following_count)

        print(f"Количество подписчиков: {followers_count}")
        followers_loops_count = int(followers_count / 12) + 1
        print(f"Число итераций для сбора подписчиков: {followers_loops_count}")

        print(f"Количество подписок: {following_count}")
        following_loops_count = int(following_count / 12) + 1
        print(f"Число итераций для сбора подписок: {following_loops_count}")

        # собираем список подписчиков
        followers_button.click()
        time.sleep(4)

        # список подписчиков
        follower_list_xpath = '/html/body/div[4]/div/div/div[2]'
        followers_urls = []

        if self.exist_element(follower_list_xpath):
            followers_ul = self.driver.find_element_by_xpath(follower_list_xpath)

            try:
                print("Запускаем сбор подписчиков...")
                for i in range(1, followers_loops_count + 1):
                    self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", followers_ul)
                    time.sleep(random.randrange(2, 4))
                    print(f"Итерация #{i}")

                all_urls_div = followers_ul.find_elements_by_tag_name("li")

                for url in all_urls_div:
                    url = url.find_element_by_tag_name("a").get_attribute("href")
                    followers_urls.append(url)

                # сохраняем всех подписчиков пользователя в файл
                with open(f'{self.username}_followers_list.txt', 'a') as followers_file:
                    for link in followers_urls:
                        followers_file.write(link + "\n")

                time.sleep(random.randrange(4, 6))
            except Exception as ex:
                print(ex)
                self.close_driver()

        self.driver.get(user_page)
        time.sleep(random.randrange(3, 6))

        # собираем список подписок
        following_button = self.driver.find_element_by_xpath(
            "/html/body/div[1]/section/main/div/header/section/ul/li[3]/a")
        following_button.click()
        time.sleep(random.randrange(3, 5))

        # TODO тут тоже не работает
        following_ul = self.driver.find_element_by_xpath("/html/body/div[5]/div/div/div[2]")

        try:
            following_urls = []
            print("Запускаем сбор подписок")

            for i in range(1, following_loops_count + 1):
                self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", following_ul)
                time.sleep(random.randrange(2, 4))
                print(f"Итерация #{i}")

            all_urls_div = following_ul.find_elements_by_tag_name("li")

            for url in all_urls_div:
                url = url.find_element_by_tag_name("a").get_attribute("href")
                following_urls.append(url)

            # сохраняем всех подписок пользователя в файл
            with open(f'{get_user_directory_path(self.username)}/'
                      f'{self.username}_following_list.txt', 'a') as following_file:
                for link in following_urls:
                    following_file.write(link + "\n")

            """Сравниваем два списка, если пользователь есть в подписках, но его нет в подписчиках,
            заносим его в отдельный список"""

            count = 0
            unfollow_list = []
            if followers_urls:
                for user in following_urls:
                    if user not in followers_urls:
                        count += 1
                        unfollow_list.append(user)
                print(f"Нужно отписаться от {count} пользователей")

            # сохраняем всех от кого нужно отписаться в файл
            with open(f'{get_user_directory_path(self.username)}/'
                      f'{self.username}_unfollow_list.txt', 'a') as unfollow_file:
                for user in unfollow_list:
                    unfollow_file.write(user + "\n")

            print("Запускаем отписку...")
            time.sleep(2)

            # заходим к каждому пользователю на страницу и отписываемся
            with open(f'{get_user_directory_path(self.username)}/'
                      f'{self.username}_unfollow_list.txt') as unfollow_file:
                unfollow_users_list = unfollow_file.readlines()
                unfollow_users_list = [row.strip() for row in unfollow_users_list]

            try:
                count = len(unfollow_users_list)
                for user_url in unfollow_users_list:
                    self.driver.get(user_url)
                    time.sleep(random.randrange(4, 6))

                    # кнопка отписки
                    unfollow_button = self.driver.find_element_by_xpath(
                        "/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div[2]/div/span/span[1]/button")
                    unfollow_button.click()

                    time.sleep(random.randrange(4, 6))

                    # подтверждение отписки
                    unfollow_button_confirm = self.driver.find_element_by_xpath(
                        "/html/body/div[5]/div/div/div/div[3]/button[1]")
                    unfollow_button_confirm.click()

                    print(f"Отписались от {user_url}")
                    count -= 1
                    print(f"Осталось отписаться от: {count} пользователей")

                    # time.sleep(random.randrange(120, 130))
                    time.sleep(random.randrange(4, 6))

            except Exception as ex:
                print(ex)
                self.wait_and_close_driver()

        except Exception as ex:
            print(ex)
            self.wait_and_close_driver()

    # метод проверяет по xpath существует ли элемент на странице
    def exist_element(self, search_pattern=None, search_by=None):
        # TODO допилить проверку (я для картинок тут проверяю)

        is_xpath = False
        img_default = False

        if search_pattern:
            if search_pattern.startswith('/html') or search_pattern.startswith('//'):
                is_xpath = True
            else:
                img_default = True
        else:
            img_default = True

        # ищем по xpath, если передается
        if is_xpath:
            try:
                self.driver.find_element_by_xpath(search_pattern)
                exist = True
            except NoSuchElementException:
                exist = False
            except Exception as ex:
                print(ex)
                exist = False
        else:
            if search_by:
                try:
                    self.driver.find_element(search_by, search_pattern)
                    exist = True
                except NoSuchElementException:
                    exist = False
                except Exception as ex:
                    print(ex)
                    exist = False
            else:
                try:
                    elem = self.driver.find_element_by_class_name('FFVAD')
                    print(elem)
                    print('elem text:', elem.text)
                    exist = True
                except NoSuchElementException:
                    exist = False

        return exist

    # проверка закрыт ли аккаунт
    def check_acc_private(self):
        # надпись закрытый акк
        private_acc_info_1 = '/html/body/div[1]/section/main/div/div[2]/article/div[1]/div/h2'
        private_acc_info_2 = '/html/body/div[1]/section/main/div/div/article/div[1]/div/h2'

        is_private_1 = self.exist_element(private_acc_info_1)
        is_private_2 = self.exist_element(private_acc_info_2)

        # ищем надпись на странице
        return is_private_1 or is_private_2

    def locate_element(self, search_pattern, search_by=None):
        is_xpath = False

        if search_pattern.startswith('/html') or search_pattern.startswith('//'):
            is_xpath = True

        driver = self.driver

        if is_xpath:
            try:
                located_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, search_pattern))
                )
            except TimeoutException as e:
                print('timeout:\n', e)
                return None
            except Exception as e:
                print(e)
                return None
        else:
            located_element = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((search_by, search_pattern))
            )

        return located_element

    # проверяем, есть ли такой пост в инсте вообще
    def post_exist(self, post_url):
        self.driver.get(post_url)
        time.sleep(5)

        # xpath с блоком 'указанная страница не найдена'
        wrong_post_url = '/html/body/div[1]/section/main/div/h2'

        # надписи с неправильной ссылкой нет
        if not self.exist_element(wrong_post_url):
            print(f'Пост успешно найден: {post_url}')
            time.sleep(1)

            return True
        else:
            print(f'Такого поста не существует, проверьте URL: {post_url}')
            return False


def get_phone_number():
    wrapper = Sms(sms_activate_api)

    try:
        # try get phone for inst
        activation = GetNumber(
            service=SmsService().Instagram
        ).request(wrapper)
    except Exception as e:
        print(e)
        return None, None

    try:
        # show activation id and phone for reception sms
        phone_number = activation.phone_number
        print('id: {} phone: {}'.format(str(activation.id), str(phone_number)))

        return phone_number, activation

    except Exception as e:
        print(e)
        return None, activation


def get_sms_code(activation):
    wrapper = Sms(sms_activate_api)

    # .. send phone number to you service
    user_action = input('Press enter if you sms was sent or type "cancel": ')
    if user_action == 'cancel':
        if user_action == 'cancel':
            set_as_cancel = SetStatus(
                id=activation.id,
                status=SmsTypes.Status.Cancel
            ).request(wrapper)
            print(set_as_cancel)
            exit(1)

    # getting and show current activation status
    response = GetStatus(id=activation.id).request(wrapper)
    print(response)

    print('get code')

    # set current activation status as SmsSent (code was sent to phone)
    set_as_sent = SetStatus(
        id=activation.id,
        status=SmsTypes.Status.SmsSent
    ).request(wrapper)
    print(set_as_sent)

    # .. wait code
    while True:
        time.sleep(1)
        response = GetStatus(id=activation.id).request(wrapper)
        if response['code']:
            sms_code = response['code']
            print('Your code:{}'.format(sms_code))
            break

    # set current activation status as End (you got code and it was right)
    set_as_end = SetStatus(
        id=activation.id,
        status=SmsTypes.Status.End
    ).request(wrapper)
    print(set_as_end)

    # .. and wait one mode code
    # (!) if you not set not_end (or set False) – activation ended before return code
    # activation.wait_code(callback=fuck_yeah, wrapper=wrapper)

    return sms_code


def test_massive():
    for user, user_data in users_settings_dict.items():
        username = user_data['login']
        password = user_data['password']

        my_bot = InstagramBot(username, password)
        my_bot.login()
        # my_bot.send_direct_message(direct_users_list, "Hey! How's it going?", "/home/cain/PycharmProjects/instagram_bot/lesson_6/img1.jpg")
        my_bot.get_followers('https://www.instagram.com/squalordf/')
        time.sleep(random.randrange(4, 8))


def test_massive_2():
    for user, user_data in users_settings_dict.items():
        username = user_data['login']
        password = user_data['password']

        my_bot = InstagramBot(username, password)
        my_bot.login()
        my_bot.smart_unsubscribe("username")


def get_accounts_auth_data(account_count_need):
    # забираем все акки из файла
    with open(f'{get_instagram_module_path()}/accounts.txt') as accounts_file:
        account_list = accounts_file.readlines()

    accounts_auth_data_list = []
    account_count = 0

    while account_list and account_count < account_count_need:
        random_account = random.choice(account_list)

        auth_data = random_account.split(',')[0].split(':')

        # заглушка для акка без номера телефона, там алерт с указанием номера вылазит (
        if not auth_data[0] == 'Ashlynmacey71':
            auth_data_list = [auth_data[0], auth_data[1]]

            accounts_auth_data_list.append(auth_data_list)
            account_count += 1

        account_list.remove(random_account)

    return accounts_auth_data_list


if __name__ == '__main__':
    bot = InstagramBot(USERNAME, PASSWORD)
    bot.login()

    # bot.driver.get('https://www.instagram.com/pretty_flayo/')
    # time.sleep(4)
    # bot.driver.get('https://naruto.fandom.com/ru/wiki/%D0%94%D0%B5%D0%B9%D0%B4%D0%B0%D1%80%D0%B0')
    # elem = bot.locate_element('/html/body/div[3]/div[7]/header/div[2]/div[1]/a')
    # elem = bot.locate_element('firstHeading', By.ID)
    # print(elem)
    # bot.driver.get('https://2ip.ru/')
    # bot.driver.get('http://checkip.org/')
    # print(bot.proxy)
    # time.sleep(5)
    # time.sleep(5)
    # bot.login()
    # bot.get_account_info()
    # bot.reg_account('sollofkid_junky', 'Sollofkid_junky1')
    # bot.like_photo_by_hashtag('zadizmoralen')
    # bot.like_post('https://www.instagram.com/p/CMPF3TeDWJ6/')
    # bot.comment_post('https://www.instagram.com/p/CMo6Y73n69f/', 'зайки <3')
    # bot.get_all_posts_url('https://www.instagram.com/squalordf/')
    # bot.put_many_likes('squalordf')

    # bot.download_user_content('squalordf')
    # bot.get_all_followers('squalordf')
    # не сработает без предыдущего
    # bot.follow_to_list_of_user_follows('squalordf')

    # bot.send_direct_message(direct_users_list, 'hi there', 'D:\PyCharm_projects\LB_soft\instagram//violet_sea.jpg')

    # bot.unsubscribe_for_all_users()
    # bot.smart_unsubscribe(USERNAME)

    # test_massive()
    bot.wait_and_close_driver()
