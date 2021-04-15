import random
import re

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QDateTime, QTime
from PyQt5.QtWidgets import (QMainWindow, QGridLayout, QGroupBox, QRadioButton, QSizePolicy,
                             QTabWidget, QVBoxLayout, QWidget, QLabel, QSpinBox, QHBoxLayout,
                             QCheckBox, QDateTimeEdit, QTimeEdit, QTableWidget, QTableWidgetItem)

import instagram.instagram_bot_start as instagram_bot
from instagram.util.urls import parse_username


class InstagramLikeCommentWindow(QMainWindow):
    bot = None

    # вызываем конструктор супер класса обычного виндова
    def __init__(self, bot):
        # вызываем конструктор без родителя чтобы не скрывалась иконка приложения из таскбара
        super(InstagramLikeCommentWindow, self).__init__()

        self.bot = bot

        self.setWindowTitle('Истаграм Лайк/Коммент')

        self.setObjectName('main_window')
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
        like_tab.addTab(self.fill_like_subs_tab(), 'Подписчикам')
        like_tab.addTab(self.fill_like_hashtag_tab(), 'По хештегу')

        return like_tab

    def fill_comments_tab(self):
        comment_tab = QTabWidget()
        comment_tab.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Ignored)

        comment_tab.addTab(self.fill_comment_users_tab(), 'Пользователям')
        comment_tab.addTab(self.fill_comment_subs_tab(), 'Подписчикам')
        comment_tab.addTab(self.fill_comment_hashtag_tab(), 'По хештегу')

        return comment_tab

    # TODO подумать мб выбрать начальную директорию дрругую
    def get_usernames_from_file(self, text_edit_object=None, directory=''):
        usernames_file_filter = 'Text files (*.txt)'
        usernames_file_name = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Выберите файл с именами аккаунтов Instagram', directory, usernames_file_filter)[0]

        with open(usernames_file_name) as file:
            username_list = file.read()

            text_edit_object.setPlainText(username_list)

    def fill_like_users_tab(self):

        main_group_box = QGroupBox('Лимиты лайков по пользователям:')

        usernames_label = QtWidgets.QLabel('Список имен аккаунтов в Instagram (в столбик)')

        usernames_from_file_button = QtWidgets.QPushButton('Из файла')
        # добавляем функционал на кнопку
        usernames_from_file_button.clicked.connect(
            lambda: self.get_usernames_from_file(self.like_users_usernames_text_edit))

        self.like_users_usernames_text_edit = QtWidgets.QPlainTextEdit()
        self.like_users_usernames_text_edit.setPlaceholderText('Список имен аккаунтов в Instagram (в столбик)')

        likes_count_label = QtWidgets.QLabel('Кол-во лайкнутых постов за день')

        # создаем панель интервалов лайков
        like_count_start = QSpinBox()
        like_count_start.setMinimum(1)
        like_count_start.setMaximum(250)
        like_count_start.setValue(1)
        like_separator_label = QLabel(' - ')
        like_count_end = QSpinBox()
        like_count_end.setMaximum(1)
        like_count_end.setMaximum(500)
        like_count_end.setValue(3)

        like_count_layout = QHBoxLayout()
        like_count_layout.addWidget(like_count_start)
        like_count_layout.addWidget(like_separator_label)
        like_count_layout.addWidget(like_count_end)

        like_random_checkbox = QCheckBox('Ставить в случайном порядке')

        # TODO убрать функцию в другое место
        # like_button.clicked.connect(lambda: self.like_users(
        #     self.like_users_usernames_text_edit.toPlainText(),
        #     like_count_start.text(),
        #     like_count_end.text()
        # ))

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.addWidget(usernames_label)
        layout.addWidget(usernames_from_file_button)
        layout.addWidget(self.like_users_usernames_text_edit)
        layout.addWidget(likes_count_label)
        layout.addLayout(like_count_layout)
        layout.addWidget(like_random_checkbox)
        layout.addStretch(1)

        main_group_box.setLayout(layout)
        # layout.setSizePolicy(QSizePolicy.Minimum)

        limit_group_box = QGroupBox('Лимиты лайков по пользователям:')

        pause_between_tasks_label = QtWidgets.QLabel('Пауза между заданиями (сек.)')

        # создаем панель интервалов лайков
        pause_between_tasks_start = QSpinBox()
        pause_between_tasks_start.setMinimum(15)
        pause_between_tasks_start.setMaximum(240)
        pause_between_tasks_start.setValue(30)
        pause_between_tasks_separator_label = QLabel(' - ')
        pause_between_tasks_end = QSpinBox()
        pause_between_tasks_end.setMinimum(16)
        pause_between_tasks_end.setMaximum(720)
        pause_between_tasks_end.setValue(240)

        pause_between_tasks_layout = QHBoxLayout()
        pause_between_tasks_layout.addWidget(pause_between_tasks_start)
        pause_between_tasks_layout.addWidget(pause_between_tasks_separator_label)
        pause_between_tasks_layout.addWidget(pause_between_tasks_end)

        pause_when_block_label = QtWidgets.QLabel('Пауза при блокировке лайков (мин.)')

        # создаем панель интервалов лайков
        pause_when_block = QtWidgets.QLineEdit('200')
        pause_when_block.setPlaceholderText('Рекомендуемый лимит лайков на день')

        day_limit_label = QtWidgets.QLabel('Рекомендуемый лимит лайков на день')

        day_limit_line = QtWidgets.QLineEdit('60')
        day_limit_line.setPlaceholderText('Рекомендуемый лимит лайков на день')

        time_label = QtWidgets.QLabel('Время для лайков в течение дня')

        time_edit = QTimeEdit()
        time_edit.setTime(QTime.currentTime())

        vbox = QVBoxLayout()
        vbox.addWidget(pause_between_tasks_label)
        vbox.addLayout(pause_between_tasks_layout)
        vbox.addWidget(pause_when_block_label)
        vbox.addWidget(pause_when_block)
        vbox.addWidget(day_limit_label)
        vbox.addWidget(day_limit_line)
        vbox.addWidget(time_label)
        vbox.addWidget(time_edit)
        vbox.addStretch(1)

        limit_group_box.setLayout(vbox)

        main_layout = QGridLayout()
        main_layout.addWidget(main_group_box, 0, 0)
        main_layout.addWidget(limit_group_box, 0, 1)

        like_user_tab = QWidget()
        like_user_tab.setLayout(main_layout)
        # main_group_box.setContentsMargins(10, 10, 10, 10)

        return like_user_tab

    def fill_like_subs_tab(self):

        main_group_box = QGroupBox('Лимиты лайков по подписчикам:')

        function_description = 'Список доноров, у которых нужно взять подписчиков в Instagram (в столбик)'

        usernames_label = QtWidgets.QLabel(function_description)

        usernames_from_file_button = QtWidgets.QPushButton('Из файла')
        # добавляем функционал на кнопку
        usernames_from_file_button.clicked.connect(
            lambda: self.get_usernames_from_file(self.like_subs_usernames_text_edit))

        self.like_subs_usernames_text_edit = QtWidgets.QPlainTextEdit()
        self.like_subs_usernames_text_edit.setPlaceholderText(function_description)

        likes_count_label = QtWidgets.QLabel('Кол-во лайкнутых постов за день')

        # создаем панель интервалов лайков
        like_count_start = QSpinBox()
        like_count_start.setMinimum(1)
        like_count_start.setMaximum(250)
        like_count_start.setValue(1)
        like_separator_label = QLabel(' - ')
        like_count_end = QSpinBox()
        like_count_end.setMaximum(1)
        like_count_end.setMaximum(500)
        like_count_end.setValue(3)

        like_count_layout = QHBoxLayout()
        like_count_layout.addWidget(like_count_start)
        like_count_layout.addWidget(like_separator_label)
        like_count_layout.addWidget(like_count_end)

        like_random_checkbox = QCheckBox('Ставить в случайном порядке')

        # TODO убрать функцию в другое место
        like_button = QtWidgets.QPushButton('Лайкнуть аккаунты')
        # добавляем функционал на кнопку
        like_button.clicked.connect(lambda: self.like_donors(
            self.like_subs_usernames_text_edit.toPlainText(),
            like_count_start.text(),
            like_count_end.text()
        ))

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.addWidget(usernames_label)
        layout.addWidget(usernames_from_file_button)
        layout.addWidget(self.like_subs_usernames_text_edit)
        layout.addWidget(likes_count_label)
        layout.addLayout(like_count_layout)
        layout.addWidget(like_random_checkbox)
        # layout.addWidget(like_button)
        layout.addStretch(1)

        main_group_box.setLayout(layout)

        limit_group_box = QGroupBox('Лимиты лайков по подписчикам:')

        pause_between_tasks_label = QtWidgets.QLabel('Пауза между заданиями (сек.)')

        # создаем панель интервалов лайков
        pause_between_tasks_start = QSpinBox()
        pause_between_tasks_start.setMinimum(15)
        pause_between_tasks_start.setMaximum(240)
        pause_between_tasks_start.setValue(30)
        pause_between_tasks_separator_label = QLabel(' - ')
        pause_between_tasks_end = QSpinBox()
        pause_between_tasks_end.setMinimum(16)
        pause_between_tasks_end.setMaximum(720)
        pause_between_tasks_end.setValue(240)

        pause_between_tasks_layout = QHBoxLayout()
        pause_between_tasks_layout.addWidget(pause_between_tasks_start)
        pause_between_tasks_layout.addWidget(pause_between_tasks_separator_label)
        pause_between_tasks_layout.addWidget(pause_between_tasks_end)

        pause_when_block_label = QtWidgets.QLabel('Пауза при блокировке лайков (мин.)')

        # создаем панель интервалов лайков
        pause_when_block = QtWidgets.QLineEdit('200')
        pause_when_block.setPlaceholderText('Рекомендуемый лимит лайков на день')

        day_limit_label = QtWidgets.QLabel('Рекомендуемый лимит лайков на день')

        day_limit_line = QtWidgets.QLineEdit('60')
        day_limit_line.setPlaceholderText('Рекомендуемый лимит лайков на день')

        time_label = QtWidgets.QLabel('Время для лайков в течение дня')

        time_edit = QTimeEdit()
        time_edit.setTime(QTime.currentTime())

        vbox = QVBoxLayout()
        vbox.addWidget(pause_between_tasks_label)
        vbox.addLayout(pause_between_tasks_layout)
        vbox.addWidget(pause_when_block_label)
        vbox.addWidget(pause_when_block)
        vbox.addWidget(day_limit_label)
        vbox.addWidget(day_limit_line)
        vbox.addWidget(time_label)
        vbox.addWidget(time_edit)
        vbox.addStretch(1)

        limit_group_box.setLayout(vbox)

        main_layout = QGridLayout()
        main_layout.addWidget(main_group_box, 0, 0)
        main_layout.addWidget(limit_group_box, 0, 1)

        like_user_tab = QWidget()
        like_user_tab.setLayout(main_layout)

        return like_user_tab

    def fill_like_hashtag_tab(self):

        def get_hashtags_from_file(parent=None, text_edit_object=None, directory=''):
            hashtags_file_filter = 'Text files (*.txt)'
            hashtags_file_name = QtWidgets.QFileDialog.getOpenFileName(
                parent, 'Выберите файл со списком хештогов для Instagram',
                directory, hashtags_file_filter)[0]

            with open(hashtags_file_name) as file:
                username_list = file.read()

                text_edit_object.setPlainText(username_list)

        main_group_box = QGroupBox('Лимиты лайков по хештегам:')

        function_description = 'Список хештегов, по которым нужно лайкнуть в Instagram (в столбик, без решетки)'

        usernames_label = QtWidgets.QLabel(function_description)

        usernames_from_file_button = QtWidgets.QPushButton('Из файла')
        # добавляем функционал на кнопку
        usernames_from_file_button.clicked.connect(
            lambda: get_hashtags_from_file(self, self.like_hastags_usernames_text_edit))

        self.like_hastags_usernames_text_edit = QtWidgets.QPlainTextEdit()
        self.like_hastags_usernames_text_edit.setPlaceholderText(function_description)

        likes_count_label = QtWidgets.QLabel('Кол-во лайкнутых постов за день')

        # создаем панель интервалов лайков
        like_count_start = QSpinBox()
        like_count_start.setMinimum(1)
        like_count_start.setMaximum(250)
        like_count_start.setValue(1)
        like_separator_label = QLabel(' - ')
        like_count_end = QSpinBox()
        like_count_end.setMaximum(1)
        like_count_end.setMaximum(500)
        like_count_end.setValue(3)

        like_count_layout = QHBoxLayout()
        like_count_layout.addWidget(like_count_start)
        like_count_layout.addWidget(like_separator_label)
        like_count_layout.addWidget(like_count_end)

        like_random_checkbox = QCheckBox('Ставить в случайном порядке')

        # TODO убрать функцию в другое место
        like_button = QtWidgets.QPushButton('Лайкнуть аккаунты')
        # добавляем функционал на кнопку
        like_button.clicked.connect(lambda: self.like_hashtags(
            self.like_hastags_usernames_text_edit.toPlainText(),
            like_count_start.text(),
            like_count_end.text()
        ))

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.addWidget(usernames_label)
        layout.addWidget(usernames_from_file_button)
        layout.addWidget(self.like_hastags_usernames_text_edit)
        layout.addWidget(likes_count_label)
        layout.addLayout(like_count_layout)
        layout.addWidget(like_random_checkbox)
        # layout.addWidget(like_button)
        layout.addStretch(1)

        main_group_box.setLayout(layout)

        limit_group_box = QGroupBox('Лимиты лайков по хештегам:')

        pause_between_tasks_label = QtWidgets.QLabel('Пауза между заданиями (сек.)')

        # создаем панель интервалов лайков
        pause_between_tasks_start = QSpinBox()
        pause_between_tasks_start.setMinimum(15)
        pause_between_tasks_start.setMaximum(240)
        pause_between_tasks_start.setValue(30)
        pause_between_tasks_separator_label = QLabel(' - ')
        pause_between_tasks_end = QSpinBox()
        pause_between_tasks_end.setMinimum(16)
        pause_between_tasks_end.setMaximum(720)
        pause_between_tasks_end.setValue(240)

        pause_between_tasks_layout = QHBoxLayout()
        pause_between_tasks_layout.addWidget(pause_between_tasks_start)
        pause_between_tasks_layout.addWidget(pause_between_tasks_separator_label)
        pause_between_tasks_layout.addWidget(pause_between_tasks_end)

        pause_when_block_label = QtWidgets.QLabel('Пауза при блокировке лайков (мин.)')

        # создаем панель интервалов лайков
        pause_when_block = QtWidgets.QLineEdit('200')
        pause_when_block.setPlaceholderText('Рекомендуемый лимит лайков на день')

        day_limit_label = QtWidgets.QLabel('Рекомендуемый лимит лайков на день')

        day_limit_line = QtWidgets.QLineEdit('60')
        day_limit_line.setPlaceholderText('Рекомендуемый лимит лайков на день')

        time_label = QtWidgets.QLabel('Время для лайков в течение дня')

        time_edit = QTimeEdit()
        time_edit.setTime(QTime.currentTime())

        vbox = QVBoxLayout()
        vbox.addWidget(pause_between_tasks_label)
        vbox.addLayout(pause_between_tasks_layout)
        vbox.addWidget(pause_when_block_label)
        vbox.addWidget(pause_when_block)
        vbox.addWidget(day_limit_label)
        vbox.addWidget(day_limit_line)
        vbox.addWidget(time_label)
        vbox.addWidget(time_edit)
        vbox.addStretch(1)

        limit_group_box.setLayout(vbox)

        main_layout = QGridLayout()
        main_layout.addWidget(main_group_box, 0, 0)
        main_layout.addWidget(limit_group_box, 0, 1)

        like_user_tab = QWidget()
        like_user_tab.setLayout(main_layout)

        return like_user_tab

    def fill_comment_users_tab(self):

        main_group_box = QGroupBox('Лимиты лайков по пользователям:')

        usernames_label = QtWidgets.QLabel('Список имен аккаунтов в Instagram (в столбик)')

        usernames_from_file_button = QtWidgets.QPushButton('Из файла')
        # добавляем функционал на кнопку
        usernames_from_file_button.clicked.connect(
            lambda: self.get_usernames_from_file(self.comment_users_usernames_text_edit))

        self.comment_users_usernames_text_edit = QtWidgets.QPlainTextEdit()
        self.comment_users_usernames_text_edit.setPlaceholderText('Список имен аккаунтов в Instagram (в столбик)')

        comment_label = QtWidgets.QLabel('Какой коммент оставить под постом:')

        comment_line = QtWidgets.QLineEdit()
        comment_line.setPlaceholderText('Какой коммент оставить под постом:')

        comment_count_label = QtWidgets.QLabel('Кол-во оставляемых в день комментариев')
        # создаем панель интервалов лайков
        comment_count_start = QSpinBox()
        comment_count_start.setMinimum(1)
        comment_count_start.setMaximum(250)
        comment_count_start.setValue(1)
        like_separator_label = QLabel(' - ')
        comment_count_end = QSpinBox()
        comment_count_end.setMaximum(1)
        comment_count_end.setMaximum(500)
        comment_count_end.setValue(3)

        comment_count_layout = QHBoxLayout()
        comment_count_layout.addWidget(comment_count_start)
        comment_count_layout.addWidget(like_separator_label)
        comment_count_layout.addWidget(comment_count_end)

        comment_random_checkbox = QCheckBox('Ставить в случайном порядке')

        # добавляем функционал на кнопку
        # comment_button.clicked.connect(lambda: self.comment_users(
        #     self.comment_users_usernames_text_edit.toPlainText(), comment_line.text()))

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.addWidget(usernames_label)
        layout.addWidget(usernames_from_file_button)
        layout.addWidget(self.comment_users_usernames_text_edit)
        layout.addWidget(comment_label)
        layout.addWidget(comment_line)
        layout.addWidget(comment_count_label)
        layout.addLayout(comment_count_layout)
        layout.addWidget(comment_random_checkbox)
        layout.addStretch(1)

        main_group_box.setLayout(layout)

        limit_group_box = QGroupBox('Лимиты комментариев по пользователям:')

        pause_between_tasks_label = QtWidgets.QLabel('Пауза между заданиями (сек.)')

        # создаем панель интервалов лайков
        pause_between_tasks_start = QSpinBox()
        pause_between_tasks_start.setMinimum(15)
        pause_between_tasks_start.setMaximum(240)
        pause_between_tasks_start.setValue(30)
        pause_between_tasks_separator_label = QLabel(' - ')
        pause_between_tasks_end = QSpinBox()
        pause_between_tasks_end.setMinimum(16)
        pause_between_tasks_end.setMaximum(720)
        pause_between_tasks_end.setValue(240)

        pause_between_tasks_layout = QHBoxLayout()
        pause_between_tasks_layout.addWidget(pause_between_tasks_start)
        pause_between_tasks_layout.addWidget(pause_between_tasks_separator_label)
        pause_between_tasks_layout.addWidget(pause_between_tasks_end)

        pause_when_block_label = QtWidgets.QLabel('Пауза при блокировке комментариев (мин.)')

        # создаем панель интервалов лайков
        pause_when_block = QtWidgets.QLineEdit('200')
        pause_when_block.setPlaceholderText('Пауза при блокировке комментариев (мин.)')

        day_limit_label = QtWidgets.QLabel('Рекомендуемый лимит комментариев на день')

        day_limit_line = QtWidgets.QLineEdit('60')
        day_limit_line.setPlaceholderText('Рекомендуемый лимит комментариев на день')

        time_label = QtWidgets.QLabel('Время для комментариев в течение дня')

        time_edit = QTimeEdit()
        time_edit.setTime(QTime.currentTime())

        vbox = QVBoxLayout()
        vbox.addWidget(pause_between_tasks_label)
        vbox.addLayout(pause_between_tasks_layout)
        vbox.addWidget(pause_when_block_label)
        vbox.addWidget(pause_when_block)
        vbox.addWidget(day_limit_label)
        vbox.addWidget(day_limit_line)
        vbox.addWidget(time_label)
        vbox.addWidget(time_edit)
        vbox.addStretch(1)

        limit_group_box.setLayout(vbox)

        main_layout = QGridLayout()
        main_layout.addWidget(main_group_box, 0, 0)
        main_layout.addWidget(limit_group_box, 0, 1)

        like_user_tab = QWidget()
        like_user_tab.setLayout(main_layout)

        return like_user_tab

    def fill_comment_subs_tab(self):

        main_group_box = QGroupBox('Лимиты лайков по пользователям:')

        function_description = 'Список доноров, у которых нужно взять подписчиков в Instagram (в столбик)'

        usernames_label = QtWidgets.QLabel(function_description)

        usernames_from_file_button = QtWidgets.QPushButton('Из файла')
        # добавляем функционал на кнопку
        usernames_from_file_button.clicked.connect(
            lambda: self.get_usernames_from_file(self.comment_subs_usernames_text_edit))

        self.comment_subs_usernames_text_edit = QtWidgets.QPlainTextEdit()
        self.comment_subs_usernames_text_edit.setPlaceholderText('Список имен аккаунтов в Instagram (в столбик)')

        comment_label = QtWidgets.QLabel('Какой коммент оставить под постом:')

        comment_line = QtWidgets.QLineEdit()
        comment_line.setPlaceholderText('Какой коммент оставить под постом:')

        comment_count_label = QtWidgets.QLabel('Кол-во оставляемых в день комментариев')
        # создаем панель интервалов лайков
        comment_count_start = QSpinBox()
        comment_count_start.setMinimum(1)
        comment_count_start.setMaximum(250)
        comment_count_start.setValue(1)
        like_separator_label = QLabel(' - ')
        comment_count_end = QSpinBox()
        comment_count_end.setMaximum(1)
        comment_count_end.setMaximum(500)
        comment_count_end.setValue(3)

        comment_count_layout = QHBoxLayout()
        comment_count_layout.addWidget(comment_count_start)
        comment_count_layout.addWidget(like_separator_label)
        comment_count_layout.addWidget(comment_count_end)

        comment_random_checkbox = QCheckBox('Ставить в случайном порядке')

        # comment_button.clicked.connect(lambda: self.comment_donors(
        #     self.comment_subs_usernames_text_edit.toPlainText(), comment_line.text()))

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.addWidget(usernames_label)
        layout.addWidget(usernames_from_file_button)
        layout.addWidget(self.comment_subs_usernames_text_edit)
        layout.addWidget(comment_label)
        layout.addWidget(comment_line)
        layout.addWidget(comment_count_label)
        layout.addLayout(comment_count_layout)
        layout.addWidget(comment_random_checkbox)
        layout.addStretch(1)

        main_group_box.setLayout(layout)

        limit_group_box = QGroupBox('Лимиты комментариев по подписчикам:')

        pause_between_tasks_label = QtWidgets.QLabel('Пауза между заданиями (сек.)')

        # создаем панель интервалов лайков
        pause_between_tasks_start = QSpinBox()
        pause_between_tasks_start.setMinimum(15)
        pause_between_tasks_start.setMaximum(240)
        pause_between_tasks_start.setValue(30)
        pause_between_tasks_separator_label = QLabel(' - ')
        pause_between_tasks_end = QSpinBox()
        pause_between_tasks_end.setMinimum(16)
        pause_between_tasks_end.setMaximum(720)
        pause_between_tasks_end.setValue(240)

        pause_between_tasks_layout = QHBoxLayout()
        pause_between_tasks_layout.addWidget(pause_between_tasks_start)
        pause_between_tasks_layout.addWidget(pause_between_tasks_separator_label)
        pause_between_tasks_layout.addWidget(pause_between_tasks_end)

        pause_when_block_label = QtWidgets.QLabel('Пауза при блокировке комментариев (мин.)')

        # создаем панель интервалов лайков
        pause_when_block = QtWidgets.QLineEdit('200')
        pause_when_block.setPlaceholderText('Пауза при блокировке комментариев (мин.)')

        day_limit_label = QtWidgets.QLabel('Рекомендуемый лимит комментариев на день')

        day_limit_line = QtWidgets.QLineEdit('60')
        day_limit_line.setPlaceholderText('Рекомендуемый лимит комментариев на день')

        time_label = QtWidgets.QLabel('Время для комментариев в течение дня')

        time_edit = QTimeEdit()
        time_edit.setTime(QTime.currentTime())

        vbox = QVBoxLayout()
        vbox.addWidget(pause_between_tasks_label)
        vbox.addLayout(pause_between_tasks_layout)
        vbox.addWidget(pause_when_block_label)
        vbox.addWidget(pause_when_block)
        vbox.addWidget(day_limit_label)
        vbox.addWidget(day_limit_line)
        vbox.addWidget(time_label)
        vbox.addWidget(time_edit)
        vbox.addStretch(1)

        limit_group_box.setLayout(vbox)

        main_layout = QGridLayout()
        main_layout.addWidget(main_group_box, 0, 0)
        main_layout.addWidget(limit_group_box, 0, 1)

        like_user_tab = QWidget()
        like_user_tab.setLayout(main_layout)

        return like_user_tab

    def fill_comment_hashtag_tab(self):

        def get_hashtags_from_file(parent=None, text_edit_object=None, directory=''):
            hashtags_file_filter = 'Text files (*.txt)'
            hashtags_file_name = QtWidgets.QFileDialog.getOpenFileName(
                parent, 'Выберите файл со списком хештогов для Instagram',
                directory, hashtags_file_filter)[0]

            with open(hashtags_file_name) as file:
                username_list = file.read()

                text_edit_object.setPlainText(username_list)

        main_group_box = QGroupBox('Лимиты лайков по пользователям:')

        function_description = 'Список хештегов, по которым нужно лайкнуть в Instagram (в столбик, без решетки)'

        usernames_label = QtWidgets.QLabel(function_description)

        usernames_from_file_button = QtWidgets.QPushButton('Из файла')
        # добавляем функционал на кнопку
        usernames_from_file_button.clicked.connect(
            lambda: get_hashtags_from_file(self, self.comment_hashtags_usernames_text_edit))

        self.comment_hashtags_usernames_text_edit = QtWidgets.QPlainTextEdit()
        self.comment_hashtags_usernames_text_edit.setPlaceholderText('Список имен аккаунтов в Instagram (в столбик)')

        comment_label = QtWidgets.QLabel('Какой коммент оставить под постом:')

        comment_line = QtWidgets.QLineEdit()
        comment_line.setPlaceholderText('Какой коммент оставить под постом:')

        comment_count_label = QtWidgets.QLabel('Кол-во оставляемых в день комментариев')
        # создаем панель интервалов лайков
        comment_count_start = QSpinBox()
        comment_count_start.setMinimum(1)
        comment_count_start.setMaximum(250)
        comment_count_start.setValue(1)
        like_separator_label = QLabel(' - ')
        comment_count_end = QSpinBox()
        comment_count_end.setMaximum(1)
        comment_count_end.setMaximum(500)
        comment_count_end.setValue(3)

        comment_count_layout = QHBoxLayout()
        comment_count_layout.addWidget(comment_count_start)
        comment_count_layout.addWidget(like_separator_label)
        comment_count_layout.addWidget(comment_count_end)

        comment_random_checkbox = QCheckBox('Ставить в случайном порядке')

        # comment_button.clicked.connect(lambda: self.comment_hashtags(
        #     self.comment_hashtags_usernames_text_edit.toPlainText(), comment_line.text()))

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.addWidget(usernames_label)
        layout.addWidget(usernames_from_file_button)
        layout.addWidget(self.comment_hashtags_usernames_text_edit)
        layout.addWidget(comment_label)
        layout.addWidget(comment_line)
        layout.addWidget(comment_count_label)
        layout.addLayout(comment_count_layout)
        layout.addWidget(comment_random_checkbox)
        layout.addStretch(1)

        main_group_box.setLayout(layout)

        limit_group_box = QGroupBox('Лимиты комментариев по хештегам:')

        pause_between_tasks_label = QtWidgets.QLabel('Пауза между заданиями (сек.)')

        # создаем панель интервалов лайков
        pause_between_tasks_start = QSpinBox()
        pause_between_tasks_start.setMinimum(15)
        pause_between_tasks_start.setMaximum(240)
        pause_between_tasks_start.setValue(30)
        pause_between_tasks_separator_label = QLabel(' - ')
        pause_between_tasks_end = QSpinBox()
        pause_between_tasks_end.setMinimum(16)
        pause_between_tasks_end.setMaximum(720)
        pause_between_tasks_end.setValue(240)

        pause_between_tasks_layout = QHBoxLayout()
        pause_between_tasks_layout.addWidget(pause_between_tasks_start)
        pause_between_tasks_layout.addWidget(pause_between_tasks_separator_label)
        pause_between_tasks_layout.addWidget(pause_between_tasks_end)

        pause_when_block_label = QtWidgets.QLabel('Пауза при блокировке комментариев (мин.)')

        # создаем панель интервалов лайков
        pause_when_block = QtWidgets.QLineEdit('200')
        pause_when_block.setPlaceholderText('Пауза при блокировке комментариев (мин.)')

        day_limit_label = QtWidgets.QLabel('Рекомендуемый лимит комментариев на день')

        day_limit_line = QtWidgets.QLineEdit('60')
        day_limit_line.setPlaceholderText('Рекомендуемый лимит комментариев на день')

        time_label = QtWidgets.QLabel('Время для комментариев в течение дня')

        time_edit = QTimeEdit()
        time_edit.setTime(QTime.currentTime())

        vbox = QVBoxLayout()
        vbox.addWidget(pause_between_tasks_label)
        vbox.addLayout(pause_between_tasks_layout)
        vbox.addWidget(pause_when_block_label)
        vbox.addWidget(pause_when_block)
        vbox.addWidget(day_limit_label)
        vbox.addWidget(day_limit_line)
        vbox.addWidget(time_label)
        vbox.addWidget(time_edit)
        vbox.addStretch(1)

        limit_group_box.setLayout(vbox)

        main_layout = QGridLayout()
        main_layout.addWidget(main_group_box, 0, 0)
        main_layout.addWidget(limit_group_box, 0, 1)

        like_user_tab = QWidget()
        like_user_tab.setLayout(main_layout)

        return like_user_tab

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

    def create_right_limits_widget(self):
        groupBox = QGroupBox('Лимиты лайков по пользователям:')

        pause_between_tasks_label = QtWidgets.QLabel('Пауза между заданиями (сек.)')

        # создаем панель интервалов лайков
        pause_between_tasks_start = QSpinBox()
        pause_between_tasks_start.setMinimum(15)
        pause_between_tasks_start.setMaximum(240)
        pause_between_tasks_start.setValue(30)
        pause_between_tasks_separator_label = QLabel(' - ')
        pause_between_tasks_end = QSpinBox()
        pause_between_tasks_end.setMinimum(16)
        pause_between_tasks_end.setMaximum(720)
        pause_between_tasks_end.setValue(240)

        pause_between_tasks_layout = QHBoxLayout()
        pause_between_tasks_layout.addWidget(pause_between_tasks_start)
        pause_between_tasks_layout.addWidget(pause_between_tasks_separator_label)
        pause_between_tasks_layout.addWidget(pause_between_tasks_end)

        pause_when_block_label = QtWidgets.QLabel('Пауза при блокировке лайков (мин.)')

        # создаем панель интервалов лайков
        pause_when_block = QtWidgets.QLineEdit('200')
        pause_when_block.setPlaceholderText('Рекомендуемый лимит лайков на день')

        day_limit_label = QtWidgets.QLabel('Рекомендуемый лимит лайков на день')

        day_limit_line = QtWidgets.QLineEdit('60')
        day_limit_line.setPlaceholderText('Рекомендуемый лимит лайков на день')

        time_label = QtWidgets.QLabel('Время для лайков в течение дня')

        time_table = QTableWidget()
        time_table.setRowCount(3)
        time_table.setColumnCount(3)
        row_pos = time_table.rowCount()
        time_table.setItem(row_pos, 0, QTableWidgetItem('temp'))
        time_table.move(0, 0)
        time_table.showRow(0)

        table_layout = QHBoxLayout()
        table_layout.setContentsMargins(5, 5, 5, 5)
        table_layout.addWidget(time_table)

        time_edit = QTimeEdit()
        time_edit.setTime(QTime.currentTime())

        vbox = QVBoxLayout()
        vbox.addWidget(pause_between_tasks_label)
        vbox.addLayout(pause_between_tasks_layout)
        vbox.addWidget(pause_when_block_label)
        vbox.addWidget(pause_when_block)
        vbox.addWidget(day_limit_label)
        vbox.addWidget(day_limit_line)
        vbox.addWidget(time_label)
        # vbox.addWidget(time_edit)
        # vbox.addWidget(time_table)
        vbox.addWidget(time_table)
        vbox.addStretch(1)
        groupBox.setLayout(vbox)

        return groupBox

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
