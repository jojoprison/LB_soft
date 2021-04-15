import re
import random

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QApplication, QMainWindow, QCheckBox, QComboBox, QDateTimeEdit,
                             QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
                             QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
                             QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
                             QVBoxLayout, QWidget, QSpacerItem)

import instagram.instagram_bot_start as instagram_bot
from instagram.util.urls import parse_username


class InstagramStrategy(QMainWindow):
    bot = None

    # вызываем конструктор супер класса обычного виндова
    def __init__(self, bot):
        # вызываем конструктор без родителя чтобы не скрывалась иконка приложения из таскбара
        super(InstagramStrategy, self).__init__()

        self.bot = bot

        self.setWindowTitle('Настройка стратегии')

        usernames_from_file_button = QtWidgets.QPushButton('Лайки')
        # добавляем функционал на кнопку
        usernames_from_file_button.clicked.connect(
            lambda: self.get_usernames_from_file(self.direct_donors_usernames_text_edit))

        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)

        layout = QGridLayout()
        layout.addWidget(self.like_widget(), 0, 0)
        layout.addWidget(self.interval_widget(), 0, 1)
        # layout.addWidget(self.create_right_limits_widget(), 0, 1)
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

    def like_widget(self):
        task_group_box = QGroupBox('Выполнять задания')

        likes_checkbox = QPushButton('Лайки')
        follow_button = QtWidgets.QPushButton('Подписаться по хештегам')
        # добавляем функционал на кнопку
        follow_button.clicked.connect(lambda: self.like_window())
        likes_checkbox.setChecked(True)
        comments_checkbox = QCheckBox('Комменты')
        comments_checkbox.setChecked(True)
        follows_checkbox = QCheckBox('Подписки')
        follows_checkbox.setChecked(True)

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.addWidget(likes_checkbox)
        layout.addWidget(comments_checkbox)
        layout.addWidget(follows_checkbox)
        layout.addStretch(1)

        task_group_box.setLayout(layout)

        return task_group_box

    def like_window(self):
        self.like_window = InstagramLikeStrategy(self.bot)
        self.like_window.show()

    def task_widget(self):
        task_group_box = QGroupBox('Выполнять задания')

        likes_checkbox = QCheckBox('Лайки')
        likes_checkbox.setChecked(True)
        comments_checkbox = QCheckBox('Комменты')
        comments_checkbox.setChecked(True)
        follows_checkbox = QCheckBox('Подписки')
        follows_checkbox.setChecked(True)

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.addWidget(likes_checkbox)
        layout.addWidget(comments_checkbox)
        layout.addWidget(follows_checkbox)
        layout.addStretch(1)

        task_group_box.setLayout(layout)

        return task_group_box

    def interval_widget(self):
        interval_group_box = QGroupBox('Паузы между заданиями (сек.)')

        # создаем панель интервалов лайков
        like_interval_start = QSpinBox()
        like_interval_start.setMinimum(5)
        like_interval_start.setMaximum(999)
        like_interval_start.setValue(30)
        like_separator_label = QLabel(' - ')
        like_interval_end = QSpinBox()
        like_interval_end.setMaximum(30)
        like_interval_end.setMaximum(1000)
        like_interval_end.setValue(240)

        like_interval_layout = QHBoxLayout()
        like_interval_layout.addWidget(like_interval_start)
        like_interval_layout.addWidget(like_separator_label)
        like_interval_layout.addWidget(like_interval_end)

        comment_interval_start = QSpinBox()
        comment_interval_start.setMinimum(5)
        comment_interval_start.setMaximum(999)
        comment_interval_start.setValue(30)
        comment_separator_label = QLabel(' - ')
        comment_interval_end = QSpinBox()
        comment_interval_end.setMaximum(30)
        comment_interval_end.setMaximum(1000)
        comment_interval_end.setValue(240)

        comment_interval_layout = QHBoxLayout()
        comment_interval_layout.addWidget(comment_interval_start)
        comment_interval_layout.addWidget(comment_separator_label)
        comment_interval_layout.addWidget(comment_interval_end)

        follow_interval_start = QSpinBox()
        follow_interval_start.setMinimum(5)
        follow_interval_start.setMaximum(999)
        follow_interval_start.setValue(30)
        follow_separator_label = QLabel(' - ')
        follow_interval_end = QSpinBox()
        follow_interval_end.setMaximum(30)
        follow_interval_end.setMaximum(1000)
        follow_interval_end.setValue(240)

        follow_interval_layout = QHBoxLayout()
        follow_interval_layout.addWidget(follow_interval_start)
        follow_interval_layout.addWidget(follow_separator_label)
        follow_interval_layout.addWidget(follow_interval_end)

        main_layout = QVBoxLayout()
        main_layout.addLayout(like_interval_layout)
        main_layout.addLayout(comment_interval_layout)
        main_layout.addLayout(follow_interval_layout)
        main_layout.addStretch(1)

        interval_group_box.setLayout(main_layout)

        return interval_group_box

    def block_widget(self):
        block_group_box = QGroupBox('Блокировка действий')

        # создаем панель интервалов лайков
        like_interval_start = QSpinBox()
        like_interval_start.setMinimum(5)
        like_interval_start.setMaximum(999)
        like_interval_start.setValue(30)
        like_separator_label = QLabel(' - ')
        like_interval_end = QSpinBox()
        like_interval_end.setMaximum(30)
        like_interval_end.setMaximum(1000)
        like_interval_end.setValue(240)

        like_interval_layout = QHBoxLayout()
        like_interval_layout.addWidget(like_interval_start)
        like_interval_layout.addWidget(like_separator_label)
        like_interval_layout.addWidget(like_interval_end)

        comment_interval_start = QSpinBox()
        comment_interval_start.setMinimum(5)
        comment_interval_start.setMaximum(999)
        comment_interval_start.setValue(30)
        comment_separator_label = QLabel(' - ')
        comment_interval_end = QSpinBox()
        comment_interval_end.setMaximum(30)
        comment_interval_end.setMaximum(1000)
        comment_interval_end.setValue(240)

        comment_interval_layout = QHBoxLayout()
        comment_interval_layout.addWidget(comment_interval_start)
        comment_interval_layout.addWidget(comment_separator_label)
        comment_interval_layout.addWidget(comment_interval_end)

        follow_interval_start = QSpinBox()
        follow_interval_start.setMinimum(5)
        follow_interval_start.setMaximum(999)
        follow_interval_start.setValue(30)
        follow_separator_label = QLabel(' - ')
        follow_interval_end = QSpinBox()
        follow_interval_end.setMaximum(30)
        follow_interval_end.setMaximum(1000)
        follow_interval_end.setValue(240)

        follow_interval_layout = QHBoxLayout()
        follow_interval_layout.addWidget(follow_interval_start)
        follow_interval_layout.addWidget(follow_separator_label)
        follow_interval_layout.addWidget(follow_interval_end)

        main_layout = QVBoxLayout()
        main_layout.addLayout(like_interval_layout)
        main_layout.addLayout(comment_interval_layout)
        main_layout.addLayout(follow_interval_layout)
        main_layout.addStretch(1)

        block_group_box.setLayout(main_layout)

        return block_group_box

    def fill_direct_users_tab(self):

        usernames_label = QtWidgets.QLabel('Список имен аккаунтов в Instagram (в столбик)')

        usernames_from_file_button = QtWidgets.QPushButton('Из файла')
        # добавляем функционал на кнопку
        usernames_from_file_button.clicked.connect(
            lambda: self.get_usernames_from_file(self.direct_users_usernames_text_edit))

        self.direct_users_usernames_text_edit = QtWidgets.QPlainTextEdit()
        self.direct_users_usernames_text_edit.setPlaceholderText('Список имен аккаунтов в Instagram (в столбик)')

        direct_message_label = QtWidgets.QLabel('Текст сообщения:')

        direct_message_line = QtWidgets.QLineEdit()
        direct_message_line.setPlaceholderText('Текст сообщения...')

        direct_button = QtWidgets.QPushButton('Написать пользователям')
        # добавляем функционал на кнопку
        direct_button.clicked.connect(lambda: self.direct_users(
            self.direct_users_usernames_text_edit.toPlainText(), direct_message_line.text()))

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.addWidget(usernames_label)
        layout.addWidget(usernames_from_file_button)
        layout.addWidget(self.direct_users_usernames_text_edit)
        layout.addWidget(direct_message_label)
        layout.addWidget(direct_message_line)
        layout.addWidget(direct_button)
        layout.addStretch(1)

        direct_users_tab = QWidget()
        direct_users_tab.setLayout(layout)

        return direct_users_tab

    def fill_direct_subs_tab(self):
        function_description = 'Список доноров, у которых нужно взять подписчиков в Instagram (в столбик)'

        usernames_label = QtWidgets.QLabel(function_description)

        usernames_from_file_button = QtWidgets.QPushButton('Из файла')
        # добавляем функционал на кнопку
        usernames_from_file_button.clicked.connect(
            lambda: self.get_usernames_from_file(self.direct_donors_usernames_text_edit))

        self.direct_donors_usernames_text_edit = QtWidgets.QPlainTextEdit()
        self.direct_donors_usernames_text_edit.setPlaceholderText(function_description)

        direct_message_label = QtWidgets.QLabel('Текст сообщения:')

        direct_message_line = QtWidgets.QLineEdit()
        direct_message_line.setPlaceholderText('Текст сообщения...')

        direct_button = QtWidgets.QPushButton('Написать пользователям')
        # добавляем функционал на кнопку
        direct_button.clicked.connect(lambda: self.direct_donors(
            self.direct_donors_usernames_text_edit.toPlainText(), direct_message_line.text()))

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.addWidget(usernames_label)
        layout.addWidget(usernames_from_file_button)
        layout.addWidget(self.direct_donors_usernames_text_edit)
        layout.addWidget(direct_message_label)
        layout.addWidget(direct_message_line)
        layout.addWidget(direct_button)
        layout.addStretch(1)

        direct_donors_tab = QWidget()
        direct_donors_tab.setLayout(layout)

        return direct_donors_tab

    def direct_users(self, usernames_plain_text, message):
        username_list = usernames_plain_text.split('\n')
        # удаляем пустые элементы
        username_list = [username for username in username_list if username != '']

        for i, username in enumerate(username_list):
            username = re.sub('[ ,.:\t]', '', username)

            username_list[i] = username

        print(username_list)

        if not self.bot:
            self.bot = instagram_bot.create()
            self.bot.login()

        print(message)
        self.bot.direct_users(username_list, message)

        self.bot_reset()

    def direct_donors(self, usernames_plain_text, message):

        if message == '':
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

            self.bot.direct_donors(username_list[0], message)

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


class InstagramLikeStrategy(QMainWindow):
    bot = None

    # вызываем конструктор супер класса обычного виндова
    def __init__(self, bot):
        # вызываем конструктор без родителя чтобы не скрывалась иконка приложения из таскбара
        super(InstagramLikeStrategy, self).__init__()

        self.bot = bot

        self.setWindowTitle('Настройка стратегии')

        usernames_from_file_button = QtWidgets.QPushButton('Лайки')
        # добавляем функционал на кнопку
        usernames_from_file_button.clicked.connect(
            lambda: self.get_usernames_from_file(self.direct_donors_usernames_text_edit))

        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)

        layout = QGridLayout()
        layout.addWidget(usernames_from_file_button)
        layout.addWidget(self.interval_widget(), 0, 1)
        # layout.addWidget(self.create_right_limits_widget(), 0, 1)
        # коофицент растяжение колонки (растягивается сначала та, у которой он больше)
        # layout.setRowStretch(1, 1)
        # layout.setRowStretch(1, 1)
        # коофицент растяжение колонки (растягивается сначала та, у которой он больше)
        # layout.setColumnStretch(0, 2)
        # layout.setColumnStretch(1, 1)

        self.central_widget.setLayout(layout)





