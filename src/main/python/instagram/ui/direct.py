import re
import random

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QMainWindow, QGridLayout, QGroupBox, QRadioButton, QSizePolicy,
                             QTabWidget, QVBoxLayout, QWidget)

import instagram.instagram_bot_start as instagram_bot
from instagram.util.urls import parse_username


class InstagramDirect(QMainWindow):
    bot = None

    # вызываем конструктор супер класса обычного виндова
    def __init__(self, bot):
        # вызываем конструктор без родителя чтобы не скрывалась иконка приложения из таскбара
        super(InstagramDirect, self).__init__()

        self.bot = bot

        self.setWindowTitle('Истаграм Директ')

        # self.setGeometry(300, 250, 350, 200)
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
        left_direct_tab_widget = QTabWidget()
        left_direct_tab_widget.setSizePolicy(QSizePolicy.Preferred,
                                      QSizePolicy.Ignored)

        left_direct_tab_widget.addTab(self.fill_direct_users_tab(), 'Пользователям')
        left_direct_tab_widget.addTab(self.fill_direct_subs_tab(), 'Подписчикам')

        return left_direct_tab_widget

    # TODO подумать мб выбрать начальную директорию дрругую
    def get_usernames_from_file(self, text_edit_object=None, directory=''):
        usernames_file_filter = 'Text files (*.txt)'
        usernames_file_name = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Выберите файл с именами аккаунтов Instagram', directory, usernames_file_filter)[0]

        with open(usernames_file_name) as file:
            username_list = file.read()

            text_edit_object.setPlainText(username_list)

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
