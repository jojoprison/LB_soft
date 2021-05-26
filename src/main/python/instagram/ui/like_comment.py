import random
import re

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import (QMainWindow, QGridLayout, QSizePolicy,
                             QTabWidget, QVBoxLayout, QWidget)

import instagram.instagram_bot_start as instagram_bot
from instagram.ui.tab import Tab
from instagram.util.urls import parse_username


class InstagramLikeCommentWindow(QMainWindow):
    bot = None

    # вызываем конструктор супер класса обычного виндова
    def __init__(self, bot):
        # вызываем конструктор без родителя чтобы не скрывалась иконка приложения из таскбара
        super(InstagramLikeCommentWindow, self).__init__()

        self.bot = bot

        self.setWindowTitle('Истаграм Лайк/Коммент')

        self.setGeometry(300, 250, 1000, 600)
        # self.resize(1200, 600)

        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)

        layout = QGridLayout()
        layout.addWidget(self.create_left_tab_widget(), 0, 0)
        # layout.addWidget(self.create_right_limits_widget(), 0, 1)
        # коофицент растяжение колонки (растягивается сначала та, у которой он больше)
        # layout.setRowStretch(1, 1)
        # layout.setRowStretch(1, 1)
        # коофицент растяжение колонки (растягивается сначала та, у которой он больше)
        # layout.setColumnStretch(0, 2)
        # layout.setColumnStretch(1, 1)

        self.central_widget.setLayout(layout)

    def bot_reset(self):
        self.bot.close_driver()
        self.bot = None

    def create_left_tab_widget(self):
        left_tab_widget = QTabWidget()
        left_tab_widget.setSizePolicy(QSizePolicy.Preferred,
                                      QSizePolicy.Ignored)

        left_tab_widget.addTab(self.fill_likes_tab(), 'Лайки')
        left_tab_widget.addTab(self.fill_comments_tab(), 'Комменты')

        return left_tab_widget

    def fill_likes_tab(self):
        like_tab = QTabWidget()
        like_tab.setSizePolicy(QSizePolicy.Preferred,
                               QSizePolicy.Ignored)

        # TODO как то подвинуть вкладки ниже на 10 пикселей, заезжает на верхние
        like_tab.addTab(self.fill_like_users_tab(), 'Пользователям')
        like_tab.addTab(self.fill_like_donors_tab(), 'Подписчикам')
        like_tab.addTab(self.fill_like_hashtag_tab(), 'По хештегу')

        return like_tab

    def fill_comments_tab(self):
        comment_tab = QTabWidget()
        comment_tab.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Ignored)

        comment_tab.addTab(self.fill_comment_users_tab(), 'Пользователям')
        comment_tab.addTab(self.fill_comment_donors_tab(), 'Подписчикам')
        comment_tab.addTab(self.fill_comment_hashtag_tab(), 'По хештегу')

        return comment_tab

    def fill_like_users_tab(self):
        return Tab(self, 'like', is_usernames=True, func_desc='Список имен аккаунтов в Instagram (в столбик)',
                   gbox_desc_limit='Лимиты лайков по пользователям:').get_tab()

    def fill_like_donors_tab(self):
        return Tab(self, 'like', is_usernames=True,
                   func_desc='Список доноров, у которых нужно взять подписчиков в Instagram (в столбик)',
                   gbox_desc_limit='Лимиты лайков по подписчикам:').get_tab()

    def fill_like_hashtag_tab(self):
        return Tab(self, 'like', is_usernames=True,
                   func_desc='Список хештегов, по которым нужно лайкнуть в Instagram (в столбик, без решетки)',
                   gbox_desc_limit='Лимиты лайков по хештегам:').get_tab()

    def fill_comment_users_tab(self):
        return Tab(self, 'comment', is_usernames=True,
                   func_desc='Список имен аккаунтов в Instagram (в столбик)',
                   gbox_desc_limit='Лимиты комментариев по пользователям:').get_tab()

    def fill_comment_donors_tab(self):
        return Tab(self, 'comment', is_usernames=True,
                   func_desc='Список доноров, у которых нужно взять подписчиков в Instagram (в столбик)',
                   gbox_desc_limit='Лимиты комментариев по подписчикам:').get_tab()

    def fill_comment_hashtag_tab(self):
        return Tab(self, 'comment', is_usernames=True,
                   func_desc='Список хештегов, по которым нужно лайкнуть в Instagram (в столбик, без решетки)',
                   gbox_desc_limit='Лимиты комментариев по хештегам:').get_tab()

    # TODO подумать как потом пристроить
    def fill_like_comment_tab(self):
        self.post_line_edit = QtWidgets.QLineEdit()
        self.post_line_edit.setObjectName('post_line_edit')
        self.post_line_edit.setGeometry(QtCore.QRect(200, 60, 400, 40))
        self.post_line_edit.setPlaceholderText('Ссылка на пост в Insagram')

        self.comment_line_edit = QtWidgets.QLineEdit()
        self.comment_line_edit.setObjectName('comment_line_edit')
        self.comment_line_edit.setGeometry(QtCore.QRect(200, 120, 400, 40))
        self.comment_line_edit.setPlaceholderText('комментарий...')

        self.bot_button = QtWidgets.QPushButton()
        self.bot_button.setGeometry(QtCore.QRect(300, 200, 200, 40))
        self.bot_button.setObjectName('like_comment_button')
        self.bot_button.setText('Лайк+Коммент')
        # добавляем функционал на кнопку
        self.bot_button.clicked.connect(lambda: self.like_comment_post(
            self.post_line_edit.text(), self.comment_line_edit.text()))

        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.addWidget(self.post_line_edit)
        layout.addWidget(self.comment_line_edit)
        layout.addWidget(self.bot_button)
        layout.addStretch(1)

        tab = QWidget()
        tab.setLayout(layout)

        return tab

    def like_comment_post(self, post, comment):
        if post:
            if not self.bot:
                self.bot = instagram_bot.create()
                self.bot.login()

            is_done = self.bot.like_comment_post(post, comment)

            self.bot_reset()

            if is_done:
                self.new_text.setText('Готово!')
            else:
                self.new_text.setText('Нудача!')

    def like_users(self, usernames_plain_text, like_count_start, like_count_end):
        username_list = usernames_plain_text.split('\n')
        # удаляем пустые элементы
        username_list = [username for username in username_list if username != '']

        for i, username in enumerate(username_list):
            username = re.sub('[ ,.:]', '', username)

            username_list[i] = username

        print(username_list)

        if not self.bot:
            self.bot = instagram_bot.create()
            self.bot.login()

        is_done = self.bot.like_multiple(username_list[0], int(like_count_start))

        self.bot_reset()

    def like_donors(self, usernames_plain_text, like_count_start, like_count_end):
        username_list = usernames_plain_text.split('\n')
        # удаляем пустые элементы
        username_list = [username for username in username_list if username != '']

        for i, username in enumerate(username_list):
            username = re.sub('[ ,.:]', '', username)

            username_list[i] = username

        print(username_list)

        if not self.bot:
            self.bot = instagram_bot.create()
            self.bot.login()

        followers_url_list = self.bot.get_followers(username_list[0])
        print(followers_url_list)

        username = parse_username(random.choice(followers_url_list))
        print(username)

        self.bot.like_multiple(username, int(likes_count))

        self.bot_reset()

    def like_hashtags(self, hashtags_plain_text, like_count_start, like_count_end):
        hashtag_list = hashtags_plain_text.split('\n')

        # удаляем пустые элементы
        hashtag_list = [hashtag for hashtag in hashtag_list if hashtag != '']
        print(hashtag_list)

        for i, hashtag in enumerate(hashtag_list):
            hashtag = re.sub('[ ,.:]', '', hashtag)

            hashtag_list[i] = hashtag

        print(hashtag_list)

        if not self.bot:
            self.bot = instagram_bot.create()
            self.bot.login()

        self.bot.like_hashtag(hashtag_list[0], int(likes_count), False)

        self.bot_reset()

    def comment_users(self, usernames_plain_text, comment):

        if comment == '':
            print('Заполните поле комментария!')
        else:
            username_list = usernames_plain_text.split('\n')
            # удаляем пустые элементы
            username_list = [username for username in username_list if username != '']

            for i, username in enumerate(username_list):
                username = re.sub('[ ,.:]', '', username)

                username_list[i] = username

            print(username_list)

            if not self.bot:
                self.bot = instagram_bot.create()
                self.bot.login()

            is_done = self.bot.comment_random(username_list[0], comment)

            self.bot_reset()

    def comment_donors(self, usernames_plain_text, comment):

        if comment == '':
            print('Заполните поле комментария!')
        else:
            username_list = usernames_plain_text.split('\n')
            # удаляем пустые элементы
            username_list = [username for username in username_list if username != '']

            for i, username in enumerate(username_list):
                username = re.sub('[ ,.:]', '', username)
                username_list[i] = username

            print(username_list)

            if not self.bot:
                self.bot = instagram_bot.create()
                self.bot.login()

            followers_url_list = self.bot.get_followers(username_list[0])
            print(followers_url_list)

            username = parse_username(random.choice(followers_url_list))
            print(username)

            is_done = self.bot.comment_random(username, comment)

            self.bot_reset()

    def comment_hashtags(self, hashtags_plain_text, comment):

        if comment == '':
            print('Заполните поле комментария!')
        else:
            hashtag_list = hashtags_plain_text.split('\n')

            # удаляем пустые элементы
            hashtag_list = [hashtag for hashtag in hashtag_list if hashtag != '']
            print(hashtag_list)

            for i, hashtag in enumerate(hashtag_list):
                hashtag = re.sub('[ ,.:]', '', hashtag)

                hashtag_list[i] = hashtag

            print(hashtag_list)

            if not self.bot:
                self.bot = instagram_bot.create()
                self.bot.login()

            self.bot.comment_hashtag(hashtag_list[0], comment)

            self.bot_reset()
