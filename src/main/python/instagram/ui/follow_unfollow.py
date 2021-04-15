import re

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QMainWindow, QGridLayout, QGroupBox, QRadioButton, QSizePolicy,
                             QTabWidget, QVBoxLayout, QWidget)

import instagram.instagram_bot_start as instagram_bot


class InstagramFollowUnfollow(QMainWindow):
    bot = None

    # вызываем конструктор супер класса обычного виндова
    def __init__(self, bot):
        # вызываем конструктор без родителя чтобы не скрывалась иконка приложения из таскбара
        super(InstagramFollowUnfollow, self).__init__()

        self.bot = bot

        self.setWindowTitle('Истаграм Подписки/Отписки')

        # self.setGeometry(300, 250, 350, 200)
        self.setObjectName('main_window')
        self.resize(1000, 600)

        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)

        layout = QGridLayout()
        layout.addWidget(self.create_left_tab_widget(), 0, 0)
        layout.addWidget(self.create_right_limits_widget(), 0, 1)
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
        follow_tab.addTab(self.fill_follow_users_tab(), 'Пользователям')
        follow_tab.addTab(self.fill_follow_subs_tab(), 'Подписчикам')
        follow_tab.addTab(self.fill_follow_hashtag_tab(), 'По хештегу')

        return follow_tab

    # TODO подумать мб выбрать начальную директорию дрругую
    def get_usernames_from_file(self, text_edit_object=None, directory=''):
        usernames_file_filter = 'Text files (*.txt)'
        usernames_file_name = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Выберите файл с именами аккаунтов Instagram', directory, usernames_file_filter)[0]

        with open(usernames_file_name) as file:
            username_list = file.read()

            text_edit_object.setPlainText(username_list)

    def fill_follow_users_tab(self):
        usernames_label = QtWidgets.QLabel('Список имен аккаунтов в Instagram (в столбик)')

        usernames_from_file_button = QtWidgets.QPushButton('Из файла')
        # добавляем функционал на кнопку
        usernames_from_file_button.clicked.connect(
            lambda: self.get_usernames_from_file(self.follow_users_usernames_text_edit))

        self.follow_users_usernames_text_edit = QtWidgets.QPlainTextEdit()
        self.follow_users_usernames_text_edit.setPlaceholderText('Список имен аккаунтов в Instagram (в столбик)')

        follow_button = QtWidgets.QPushButton('Подписаться на аккаунты')
        # добавляем функционал на кнопку
        follow_button.clicked.connect(lambda: self.follow_users(
            self.follow_users_usernames_text_edit.toPlainText()))

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.addWidget(usernames_label)
        layout.addWidget(usernames_from_file_button)
        layout.addWidget(self.follow_users_usernames_text_edit)
        layout.addWidget(follow_button)
        layout.addStretch(1)

        follow_users_tab = QWidget()
        follow_users_tab.setLayout(layout)

        return follow_users_tab

    def fill_follow_subs_tab(self):
        function_description = 'Список доноров, у которых нужно взять подписчиков в Instagram (в столбик)'

        usernames_label = QtWidgets.QLabel(function_description)

        usernames_from_file_button = QtWidgets.QPushButton('Из файла')
        # добавляем функционал на кнопку
        usernames_from_file_button.clicked.connect(
            lambda: self.get_usernames_from_file(self.follow_donors_usernames_text_edit))

        self.follow_donors_usernames_text_edit = QtWidgets.QPlainTextEdit()
        self.follow_donors_usernames_text_edit.setPlaceholderText(function_description)

        follow_button = QtWidgets.QPushButton('Подписаться на аккаунты')
        # добавляем функционал на кнопку
        follow_button.clicked.connect(lambda: self.follow_donors(
            self.follow_donors_usernames_text_edit.toPlainText()))

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.addWidget(usernames_label)
        layout.addWidget(usernames_from_file_button)
        layout.addWidget(self.follow_donors_usernames_text_edit)
        layout.addWidget(follow_button)
        layout.addStretch(1)

        follow_donors_tab = QWidget()
        follow_donors_tab.setLayout(layout)

        return follow_donors_tab

    def fill_follow_hashtag_tab(self):

        def get_hashtags_from_file(parent=None, text_edit_object=None, directory=''):
            hashtags_file_filter = 'Text files (*.txt)'
            hashtags_file_name = QtWidgets.QFileDialog.getOpenFileName(
                parent, 'Выберите файл со списком хештогов для Instagram',
                directory, hashtags_file_filter)[0]

            with open(hashtags_file_name) as file:
                username_list = file.read()

                text_edit_object.setPlainText(username_list)

        function_description = 'Список хештегов, по которым нужно лайкнуть в Instagram (в столбик, без решетки)'

        usernames_label = QtWidgets.QLabel(function_description)

        usernames_from_file_button = QtWidgets.QPushButton('Из файла')
        # добавляем функционал на кнопку
        usernames_from_file_button.clicked.connect(
            lambda: get_hashtags_from_file(self, self.follow_hashtags_usernames_text_edit))

        self.follow_hashtags_usernames_text_edit = QtWidgets.QPlainTextEdit()
        self.follow_hashtags_usernames_text_edit.setPlaceholderText(function_description)

        follow_button = QtWidgets.QPushButton('Подписаться по хештегам')
        # добавляем функционал на кнопку
        follow_button.clicked.connect(lambda: self.follow_hashtags(
            self.follow_hashtags_usernames_text_edit.toPlainText()))

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.addWidget(usernames_label)
        layout.addWidget(usernames_from_file_button)
        layout.addWidget(self.follow_hashtags_usernames_text_edit)
        layout.addWidget(follow_button)
        layout.addStretch(1)

        follow_hashtags_tab = QWidget()
        follow_hashtags_tab.setLayout(layout)

        return follow_hashtags_tab

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

    def fill_unfollow_tab(self):
        unfollow_tab = QTabWidget()
        unfollow_tab.setSizePolicy(QSizePolicy.Preferred,
                               QSizePolicy.Ignored)

        # TODO как то подвинуть вкладки ниже на 10 пикселей, заезжает на верхние
        unfollow_tab.addTab(self.fill_unfollow_smart_tab(), 'Умная отписка')
        unfollow_tab.addTab(self.fill_unfollow_all_tab(), 'От всех')

        return unfollow_tab

    def fill_unfollow_smart_tab(self):
        unfollow_label = QtWidgets.QLabel('Умная отписка')

        unfollow_button = QtWidgets.QPushButton('Отписаться')
        # добавляем функционал на кнопку
        unfollow_button.clicked.connect(lambda: self.unfollow_smart())

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.addWidget(unfollow_label)
        layout.addWidget(unfollow_button)
        layout.addStretch(1)

        unfollow_smart_tab = QWidget()
        unfollow_smart_tab.setLayout(layout)

        return unfollow_smart_tab

    def fill_unfollow_all_tab(self):
        unfollow_label = QtWidgets.QLabel('Отписка от всех')

        unfollow_button = QtWidgets.QPushButton('Отписаться')
        # добавляем функционал на кнопку
        unfollow_button.clicked.connect(lambda: self.unfollow_all())

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.addWidget(unfollow_label)
        layout.addWidget(unfollow_button)
        layout.addStretch(1)

        unfollow_all_tab = QWidget()
        unfollow_all_tab.setLayout(layout)

        return unfollow_all_tab

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

    def create_right_limits_widget(self):
        groupBox = QGroupBox('Лимиты')

        radio1 = QRadioButton("&Radio button 1")
        radio2 = QRadioButton("R&adio button 2")
        radio3 = QRadioButton("Ra&dio button 3")

        radio1.setChecked(True)

        vbox = QVBoxLayout()
        vbox.addWidget(radio1)
        vbox.addWidget(radio2)
        vbox.addWidget(radio3)
        vbox.addStretch(1)
        groupBox.setLayout(vbox)

        return groupBox
