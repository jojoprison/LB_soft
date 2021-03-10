import json
import os
import random
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from instagram.config import *
from instagram.config import users_settings_dict


def get_user_page_url(username):
    return f'https://www.instagram.com/{username}/'


def get_user_directory_path(username):
    directory_path = f'users/{username}'

    # создаём папку с именем пользователя для чистоты проекта
    if not os.path.exists(directory_path):
        os.mkdir(directory_path)

    return directory_path


def get_user_posts_file_path(username):
    return f'{get_user_directory_path(username)}/{username}_posts.txt'


class InstagramBot:
    def __init__(self, driver=None, username=None, password=None):
        if not username:
            username = USERNAME
        if not password:
            password = PASSWORD
        if not driver:
            driver = webdriver.Chrome("../drivers/chromedriver.exe")

        self.username = username
        self.password = password
        self.driver = driver

    # метод для закрытия браузера
    def close_driver(self):
        self.driver.close()
        self.driver.quit()

    # метод логина
    def login(self):

        driver = self.driver
        driver.get('https://www.instagram.com')
        time.sleep(random.randrange(3, 5))

        username_input = driver.find_element_by_name('username')
        username_input.clear()
        username_input.send_keys(self.username)

        time.sleep(2)

        password_input = driver.find_element_by_name('password')
        password_input.clear()
        password_input.send_keys(self.password)

        password_input.send_keys(Keys.ENTER)
        time.sleep(7)

        not_now_btn = driver.find_element_by_class_name('cmbtv')
        not_now_btn.click()

        time.sleep(4)

        notification_dialog = driver.find_element(By.CSS_SELECTOR, '[role="dialog"]')
        off_notifications = notification_dialog.find_element_by_xpath(
            './/div/div/div[3]/button[2]')
        off_notifications.click()

        time.sleep(1)

    def get_account_info(self):

        driver = self.driver
        self.login()

        user_account_link = driver.find_element_by_link_text(USERNAME)
        user_account_link.click()

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

    # метод ставит лайки по hashtag
    def like_photo_by_hashtag(self, hashtag):

        driver = self.driver
        driver.get(f'https://www.instagram.com/explore/tags/{hashtag}/')
        time.sleep(5)

        for i in range(1, 4):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.randrange(3, 5))

        hrefs = driver.find_elements_by_tag_name('a')
        posts_urls = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]

        for url in posts_urls:
            try:
                driver.get(url)
                time.sleep(3)

                like_button = driver.find_element_by_xpath(
                    '/html/body/div[1]/section/main/div/div[1]/article/'
                    'div[3]/section[1]/span[1]/button')
                like_button.click()

                time.sleep(random.randrange(80, 100))
            except Exception as ex:
                print(ex)
                self.close_driver()

    # метод проверяет по xpath существует ли элемент на странице
    def exist_element(self, xpath=None):

        driver = self.driver

        # ищем по xpath, если передается
        if xpath:
            try:
                driver.find_element_by_xpath(xpath)
                exist = True
            except NoSuchElementException:
                exist = False
        # ищем тег <a> с указанным классом, там выдернем ссылку на контент
        else:
            try:
                elem = driver.find_element_by_class_name('savefrom-helper--btn')
                print(elem.text)
                exist = True
            except NoSuchElementException:
                exist = False

        return exist

    # метод ставит лайк на пост по прямой ссылке
    def like_post(self, insta_post):

        driver = self.driver
        driver.get(insta_post)
        time.sleep(4)

        wrong_user_page = "/html/body/div[1]/section/main/div/h2"

        if self.exist_element(wrong_user_page):
            print("Такого поста не существует, проверьте URL")
            self.close_driver()
        else:
            print("Пост успешно найден, ставим лайк!")
            time.sleep(2)

            like_button_xpath = '/html/body/div[1]/section/main/div/div[1]/article/' \
                                'div[3]/section[1]/span[1]/button'

            like_button = driver.find_element_by_xpath(like_button_xpath)
            driver.execute_script("arguments[0].click();", like_button)

            time.sleep(2)

            print(f"Лайк на пост: {insta_post} поставлен!")
            self.close_driver()

    # метод собирает ссылки на все посты пользователя
    def get_all_posts_url(self, username):

        driver = self.driver

        user_page = get_user_page_url(username)

        driver.get(user_page)
        time.sleep(4)

        wrong_user_page = "/html/body/div[1]/section/main/div/h2"

        if self.exist_element(wrong_user_page):
            print("Такого пользователя не существует, проверьте URL")
            self.close_driver()

            return None
        else:
            print("Пользователь успешно найден, начинаю собирать ссылки...")
            time.sleep(2)

            posts_count = int(driver.find_element_by_xpath(
                "/html/body/div[1]/section/main/div/header/section/ul/li[1]/span/span").text)
            loops_count = int(posts_count / 12)
            print(loops_count)

            posts_urls = []

            for i in range(0, loops_count):

                hrefs = driver.find_elements_by_tag_name('a')
                hrefs = [item.get_attribute('href') for item in hrefs
                         if "/p/" in item.get_attribute('href')]

                for href in hrefs:
                    posts_urls.append(href)

                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                time.sleep(random.randrange(2, 4))

                print(f"Итерация #{i}")

            posts_url_set = set(posts_urls)
            posts_url_set = list(posts_url_set)

            with open(get_user_posts_file_path(username), 'a') as file:
                for post_url in posts_url_set:
                    file.write(post_url + '\n')

            return username

    # метод ставит лайки по ссылке на аккаунт пользователя
    def put_many_likes(self, username):

        driver = self.driver

        # собираем ссылки на посты в файл
        self.get_all_posts_url(username)

        time.sleep(4)

        user_page = get_user_page_url(username)
        driver.get(user_page)

        time.sleep(4)

        with open(get_user_posts_file_path(username)) as file:
            url_list = file.readlines()

            for post_url in url_list[0:6]:
                try:
                    driver.get(post_url)
                    time.sleep(2)

                    like_button = "/html/body/div[1]/section/main/div/div/article/" \
                                  "div[3]/section[1]/span[1]/button"
                    driver.find_element_by_xpath(like_button).click()
                    time.sleep(2)

                    print(f"Лайк на пост: {post_url} успешно поставлен!")

                except Exception as ex:
                    print(ex)
                    self.close_driver()

        self.close_driver()

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
                    time.sleep(4)

                    img_src = "/html/body/div[1]/section/main/div/div[1]/article/" \
                              "div[2]/div/div/div[1]/img"
                    video_src = "/html/body/div[1]/section/main/div/div[1]/article/" \
                                "div[2]/div/div/div[1]/div/div/video"

                    post_id = post_url.split('/')[-2]

                    if self.exist_element(img_src):
                        img_src_url = driver.find_element_by_xpath(img_src).get_attribute("src")

                        img_and_video_src_urls.append(img_src_url)

                        # сохраняем изображение
                        get_img = requests.get(img_src_url)

                        with open(f'{get_user_directory_path(username)}/'
                                  f'{username}_{post_id}_img.jpg', 'wb') as img_file:
                            img_file.write(get_img.content)

                    elif self.exist_element(video_src):
                        video_src_url = driver.find_element_by_xpath(video_src).get_attribute("src")
                        img_and_video_src_urls.append(video_src_url)

                        # сохраняем видео
                        get_video = requests.get(video_src_url, stream=True)

                        with open(f"{get_user_directory_path(username)}/"
                                  f"{username}_{post_id}_video.mp4", "wb") as video_file:

                            for chunk in get_video.iter_content(chunk_size=1280 * 1024):
                                if chunk:
                                    video_file.write(chunk)
                    else:
                        img_and_video_src_urls.append(f"{post_url}, нет ссылки!")

                    print(f'Просмотрен контент поста: {post_url}')

                except Exception as ex:
                    print(ex)
                    self.close_driver()

            self.close_driver()

        with open(f'{get_user_directory_path(username)}/'
                  f'{username}_img_and_video_src_urls.txt', 'a') as file:
            for i in img_and_video_src_urls:
                file.write(i + "\n")

    # метод подписки на всех подписчиков переданного аккаунта
    def get_all_followers(self, username):

        user_page = get_user_page_url(username)

        driver = self.driver
        driver.get(user_page)
        time.sleep(4)

        wrong_user_page = "/html/body/div[1]/section/main/div/h2"

        if self.exist_element(wrong_user_page):
            print(f"Пользователя {username} не существует, проверьте URL")
            self.close_driver()
        else:
            print(f"Пользователь {username} успешно найден, начинаем скачивать ссылки на подписчиков!")
            time.sleep(2)

            followers_button = driver.find_element_by_xpath(
                "/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span")

            followers_count = followers_button.get_attribute('title')
            # followers_count = followers_button.text
            # followers_count = int(followers_count.split(' ')[0])

            # если количество подписчиков больше 999, убираем из числа запятые
            if ',' in followers_count:
                followers_count = int(''.join(followers_count.split(',')))
            else:
                followers_count = int(followers_count)

            print(f"Количество подписчиков: {followers_count}")
            time.sleep(2)

            loops_count = int(followers_count / 12)

            print(f"Число итераций: {loops_count}")
            time.sleep(4)

            followers_button.click()
            time.sleep(4)

            followers_ul = driver.find_element_by_xpath("/html/body/div[5]/div/div/div[2]/ul")

            try:
                followers_urls = []

                for i in range(1, loops_count + 1):
                    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", followers_ul)
                    time.sleep(random.randrange(2, 4))
                    print(f"Итерация #{i}")

                all_urls_div = followers_ul.find_elements_by_tag_name("li")

                for url in all_urls_div:
                    url = url.find_element_by_tag_name("a").get_attribute("href")
                    followers_urls.append(url)

                # сохраняем всех подписчиков пользователя в файл
                with open(f'{get_user_directory_path(username)}/{username}_subs.txt', 'a') as text_file:
                    for link in followers_urls:
                        text_file.write(link + "\n")

                with open(f'{get_user_directory_path(username)}/{username}_subs.txt') as text_file:
                    users_urls = text_file.readlines()

                    for user in users_urls[0:10]:
                        try:
                            try:
                                with open(f'{get_user_directory_path(username)}/'
                                          f'{username}_subscribe_list.txt',
                                          'r') as subscribe_list_file:

                                    lines = subscribe_list_file.readlines()

                                    if user in lines:
                                        print(f'Мы уже подписаны на {user}, переходим к следующему пользователю!')
                                        continue

                            except Exception as ex:
                                print('Файл со ссылками ещё не создан!')
                                # print(ex)

                            driver = self.driver
                            driver.get(user)
                            page_owner = user.split("/")[-2]

                            if self.exist_element("/html/body/div[1]/section/main/div/header/section/div[1]/div/a"):

                                print("Это наш профиль, уже подписан, пропускаем итерацию!")
                            elif self.exist_element(
                                    "/html/body/div[1]/section/main/div/header/section/div[1]/div[2]/div/span/span[1]/button/div/span"):
                                print(f"Уже подписаны, на {page_owner} пропускаем итерацию!")
                            else:
                                time.sleep(random.randrange(4, 8))

                                if self.exist_element(
                                        "/html/body/div[1]/section/main/div/div/article/div[1]/div/h2"):
                                    try:
                                        follow_button = driver.find_element_by_xpath(
                                            "/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/button").click()
                                        print(f'Запросили подписку на пользователя {page_owner}. Закрытый аккаунт!')
                                    except Exception as ex:
                                        print(ex)
                                else:
                                    try:
                                        if self.exist_element(
                                                "/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/button"):
                                            follow_button = driver.find_element_by_xpath(
                                                "/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/button").click()
                                            print(f'Подписались на пользователя {page_owner}. Открытый аккаунт!')
                                        else:
                                            follow_button = driver.find_element_by_xpath(
                                                "/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/span/span[1]/button").click()
                                            print(f'Подписались на пользователя {page_owner}. Открытый аккаунт!')
                                    except Exception as ex:
                                        print(ex)

                                # записываем данные в файл для ссылок всех подписок, если файла нет, создаём, если есть - дополняем
                                with open(f'{get_user_directory_path(username)}/'
                                          f'{username}_subscribe_list.txt',
                                          'a') as subscribe_list_file:
                                    subscribe_list_file.write(user)

                                time.sleep(random.randrange(7, 15))

                        except Exception as ex:
                            print(ex)
                            self.close_driver()

            except Exception as ex:
                print(ex)
                self.close_driver()

        self.close_driver()

    # метод для отправки сообщений в директ
    def send_direct_message(self, usernames="", message="", img_path=''):

        driver = self.driver
        time.sleep(random.randrange(2, 4))

        direct_message_button = "/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[2]/a"

        if not self.exist_element(direct_message_button):
            print("Кнопка отправки сообщений не найдена!")
            self.close_driver()
        else:
            print("Отправляем сообщение...")
            direct_message = driver.find_element_by_xpath(direct_message_button).click()
            time.sleep(random.randrange(2, 4))

        # отключаем всплывающее окно
        if self.exist_element("/html/body/div[4]/div/div"):
            driver.find_element_by_xpath("/html/body/div[4]/div/div/div/div[3]/button[2]").click()
        time.sleep(random.randrange(2, 4))

        send_message_button = driver.find_element_by_xpath(
            "/html/body/div[1]/section/div/div[2]/div/div/div[2]/div/button").click()
        time.sleep(random.randrange(2, 4))

        # отправка сообщения нескольким пользователям
        for user in usernames:
            # вводим получателя
            to_input = driver.find_element_by_xpath("/html/body/div[4]/div/div/div[2]/div[1]/div/div[2]/input")
            to_input.send_keys(user)
            time.sleep(random.randrange(2, 4))

            # выбираем получателя из списка
            users_list = driver.find_element_by_xpath(
                "/html/body/div[4]/div/div/div[2]/div[2]").find_element_by_tag_name("button").click()
            time.sleep(random.randrange(2, 4))

        next_button = driver.find_element_by_xpath(
            "/html/body/div[4]/div/div/div[1]/div/div[2]/div/button").click()
        time.sleep(random.randrange(2, 4))

        # отправка текстового сообщения
        if message:
            text_message_area = driver.find_element_by_xpath(
                "/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea")
            text_message_area.clear()
            text_message_area.send_keys(message)
            time.sleep(random.randrange(2, 4))
            text_message_area.send_keys(Keys.ENTER)
            print(f"Сообщение для {usernames} успешно отправлено!")
            time.sleep(random.randrange(2, 4))

        # отправка изображения
        if img_path:
            send_img_input = driver.find_element_by_xpath(
                "/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/form/input")
            send_img_input.send_keys(img_path)
            print(f"Изображение для {usernames} успешно отправлено!")
            time.sleep(random.randrange(2, 4))

        self.close_driver()

    # метод отписки от всех пользователей
    def unsubscribe_for_all_users(self, userpage):

        driver = self.driver
        driver.get(f"https://www.instagram.com/{USERNAME}/")
        time.sleep(random.randrange(3, 6))

        following_button = driver.find_element_by_xpath(
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
            driver.get(f"https://www.instagram.com/{USERNAME}/")
            time.sleep(random.randrange(3, 6))

            # кликаем/вызываем меню подписок
            following_button = driver.find_element_by_xpath(
                "/html/body/div[1]/section/main/div/header/section/ul/li[3]/a")

            following_button.click()
            time.sleep(random.randrange(3, 6))

            # забираем все li из ul, в них хранится кнопка отписки и ссылки на подписки
            following_div_block = driver.find_element_by_xpath("/html/body/div[4]/div/div/div[2]/ul/div")
            following_users = following_div_block.find_elements_by_tag_name("li")
            time.sleep(random.randrange(3, 6))

            for user in following_users:

                if not count:
                    break

                user_url = user.find_element_by_tag_name("a").get_attribute("href")
                user_name = user_url.split("/")[-2]

                # добавляем в словарь пару имя_пользователя: ссылка на аккаунт, на всякий, просто полезно сохранять информацию
                following_users_dict[user_name] = user_url

                following_button = user.find_element_by_tag_name("button").click()
                time.sleep(random.randrange(3, 6))
                unfollow_button = driver.find_element_by_xpath(
                    "/html/body/div[5]/div/div/div/div[3]/button[1]").click()

                print(f"Итерация #{count} >>> Отписался от пользователя {user_name}")
                count -= 1

                # time.sleep(random.randrange(120, 130))
                time.sleep(random.randrange(2, 4))

        with open("following_users_dict.txt", "w", encoding="utf-8") as file:
            json.dump(following_users_dict, file)

        self.close_driver()

    # метод отписки, отписываемся от всех кто не подписан на нас
    def smart_unsubscribe(self, username):

        driver = self.driver
        driver.get(f"https://www.instagram.com/{username}/")
        time.sleep(random.randrange(3, 6))

        followers_button = driver.find_element_by_xpath(
            "/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span")
        followers_count = followers_button.get_attribute("title")

        following_button = driver.find_element_by_xpath(
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

        followers_ul = driver.find_element_by_xpath("/html/body/div[4]/div/div/div[2]")

        try:
            followers_urls = []
            print("Запускаем сбор подписчиков...")
            for i in range(1, followers_loops_count + 1):
                driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", followers_ul)
                time.sleep(random.randrange(2, 4))
                print(f"Итерация #{i}")

            all_urls_div = followers_ul.find_elements_by_tag_name("li")

            for url in all_urls_div:
                url = url.find_element_by_tag_name("a").get_attribute("href")
                followers_urls.append(url)

            # сохраняем всех подписчиков пользователя в файл
            with open(f"{username}_followers_list.txt", "a") as followers_file:
                for link in followers_urls:
                    followers_file.write(link + "\n")
        except Exception as ex:
            print(ex)
            self.close_driver()

        time.sleep(random.randrange(4, 6))
        driver.get(f"https://www.instagram.com/{username}/")
        time.sleep(random.randrange(3, 6))

        # собираем список подписок
        following_button = driver.find_element_by_xpath(
            "/html/body/div[1]/section/main/div/header/section/ul/li[3]/a")
        following_button.click()
        time.sleep(random.randrange(3, 5))

        following_ul = driver.find_element_by_xpath("/html/body/div[4]/div/div/div[2]")

        try:
            following_urls = []
            print("Запускаем сбор подписок")

            for i in range(1, following_loops_count + 1):
                driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", following_ul)
                time.sleep(random.randrange(2, 4))
                print(f"Итерация #{i}")

            all_urls_div = following_ul.find_elements_by_tag_name("li")

            for url in all_urls_div:
                url = url.find_element_by_tag_name("a").get_attribute("href")
                following_urls.append(url)

            # сохраняем всех подписок пользователя в файл
            with open(f"{username}_following_list.txt", "a") as following_file:
                for link in following_urls:
                    following_file.write(link + "\n")

            """Сравниваем два списка, если пользователь есть в подписках, но его нет в подписчиках,
            заносим его в отдельный список"""

            count = 0
            unfollow_list = []
            for user in following_urls:
                if user not in followers_urls:
                    count += 1
                    unfollow_list.append(user)
            print(f"Нужно отписаться от {count} пользователей")

            # сохраняем всех от кого нужно отписаться в файл
            with open(f"{username}_unfollow_list.txt", "a") as unfollow_file:
                for user in unfollow_list:
                    unfollow_file.write(user + "\n")

            print("Запускаем отписку...")
            time.sleep(2)

            # заходим к каждому пользователю на страницу и отписываемся
            with open(f"{username}_unfollow_list.txt") as unfollow_file:
                unfollow_users_list = unfollow_file.readlines()
                unfollow_users_list = [row.strip() for row in unfollow_users_list]

            try:
                count = len(unfollow_users_list)
                for user_url in unfollow_users_list:
                    driver.get(user_url)
                    time.sleep(random.randrange(4, 6))

                    # кнопка отписки
                    unfollow_button = driver.find_element_by_xpath(
                        "/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div[2]/div/span/span[1]/button")
                    unfollow_button.click()

                    time.sleep(random.randrange(4, 6))

                    # подтверждение отписки
                    unfollow_button_confirm = driver.find_element_by_xpath(
                        "/html/body/div[4]/div/div/div/div[3]/button[1]")
                    unfollow_button_confirm.click()

                    print(f"Отписались от {user_url}")
                    count -= 1
                    print(f"Осталось отписаться от: {count} пользователей")

                    # time.sleep(random.randrange(120, 130))
                    time.sleep(random.randrange(4, 6))

            except Exception as ex:
                print(ex)
                self.close_driver()

        except Exception as ex:
            print(ex)
            self.close_driver()

        time.sleep(random.randrange(4, 6))
        self.close_driver()


def test_massive():
    for user, user_data in users_settings_dict.items():
        username = user_data['login']
        password = user_data['password']

        my_bot = InstagramBot(username, password)
        my_bot.login()
        # my_bot.send_direct_message(direct_users_list, "Hey! How's it going?", "/home/cain/PycharmProjects/instagram_bot/lesson_6/img1.jpg")
        my_bot.get_all_followers('https://www.instagram.com/squalordf/')
        time.sleep(random.randrange(4, 8))


def test_massive_2():
    for user, user_data in users_settings_dict.items():
        username = user_data['login']
        password = user_data['password']

        my_bot = InstagramBot(username, password)
        my_bot.login()
        my_bot.smart_unsubscribe("username")


if __name__ == '__main__':
    bot = InstagramBot(USERNAME, PASSWORD)
    # bot.get_account_info()
    bot.login()
    # bot.like_photo_by_hashtag('ogbuda')
    # bot.like_post('https://www.instagram.com/p/CMPF3TeDWJ6/')
    # bot.get_all_posts_url('https://www.instagram.com/squalordf/')
    # bot.put_many_likes('squalordf')

    bot.download_user_content('squalordf')
    # bot.put_many_likes("https://www.instagram.com/squalordf/")

    # test_massive()
