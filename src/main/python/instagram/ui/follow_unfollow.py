import re

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QMainWindow, QGridLayout, QSizePolicy,
                             QTabWidget)

import instagram.instagram_bot_start as instagram_bot
from instagram.ui.tab import Tab


class InstagramFollowUnfollow(QMainWindow):
    bot = None

    # вызываем конструктор супер класса обычного виндова
    def __init__(self, bot):
        # вызываем конструктор без родителя чтобы не скрывалась иконка приложения из таскбара
        super(InstagramFollowUnfollow, self).__init__()

        self.bot = bot

        self.setWindowTitle('Истаграм Подписки/Отписки')

        # self.setGeometry(300, 250, 350, 200)
        self.resize(1000, 600)

        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)

        layout = QGridLayout()
        layout.addWidget(self.create_left_tab_widget(), 0, 0)
        # коофицент растяжение колонки (растягивается сначала та, у которой он больше)
        # layout.setRowStretch(1, 1)
        # layout.setRowStretch(1, 1)
        # коофицент растяжение колонки (растягивается сначала та, у которой он больше)
        # layout.setColumnStretch(0, 2)
        # layout.setColumnStretch(1, 1)

        self.central_widget.setLayout(layout)

    # закрываем браузер, ресетим поле с ботом, чтоб коннетк потом открыть к нему заново
    def bot_reset(self):
        self.bot.close_driver()
        self.bot = None

    def create_left_tab_widget(self):
        left_tab_widget = QTabWidget()
        left_tab_widget.setSizePolicy(QSizePolicy.Preferred,
                                      QSizePolicy.Ignored)

        left_tab_widget.addTab(self.fill_follow_tab(), 'Подписки')
        left_tab_widget.addTab(self.fill_unfollow_tab(), 'Отписки')

        return left_tab_widget

    def fill_follow_tab(self):
        follow_tab = QTabWidget()
        follow_tab.setSizePolicy(QSizePolicy.Preferred,
                                 QSizePolicy.Ignored)

        # TODO как то подвинуть вкладки ниже на 10 пикселей, заезжает на верхние
        follow_tab.addTab(self.fill_follow_users_tab(), 'На пользователей')
        follow_tab.addTab(self.fill_follow_donors_tab(), 'На подписчиков')
        follow_tab.addTab(self.fill_follow_hashtag_tab(), 'По хештегам')

        return follow_tab

    def fill_follow_users_tab(self):
        return Tab(self, 'follow', is_usernames=True, func_desc='Список имен аккаунтов в Instagram (в столбик)',
                   gbox_desc_limit='Лимиты подписок по пользователям:').get_tab()

    def fill_follow_donors_tab(self):
        return Tab(self, 'follow', is_usernames=True,
                   func_desc='Список доноров, у которых нужно взять подписчиков в Instagram (в столбик)',
                   gbox_desc_limit='Лимиты подписок по донорам:').get_tab()

    def fill_follow_hashtag_tab(self):
        return Tab(self, 'follow', is_usernames=True,
                   func_desc='Список хештегов, по которым нужно лайкнуть в Instagram (в столбик, без решетки)',
                   gbox_desc_limit='Лимиты подписок по хэштегам:').get_tab()

    def fill_unfollow_tab(self):
        return Tab(self, 'unfollow', is_usernames=True, func_desc=None,
                   gbox_desc_limit='Лимиты отписок:').get_tab()

    def follow_users(self, usernames_plain_text):
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

        is_done = self.bot.follow_user(username_list[0])

        self.bot_reset()

    def follow_donors(self, usernames_plain_text):
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

        is_done = self.bot.follow_donors(username_list[0])

        self.bot_reset()

    def follow_hashtags(self, hashtags_plain_text):
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

        self.bot.follow_hashtag(hashtag_list[0])

        self.bot_reset()

    def unfollow_smart(self):

        if not self.bot:
            self.bot = instagram_bot.create()
            self.bot.login()

        self.bot.smart_unsubscribe()

        self.bot_reset()

    def unfollow_all(self):

        if not self.bot:
            self.bot = instagram_bot.create()
            self.bot.login()

        self.bot.unfollow_all()

        self.bot_reset()
