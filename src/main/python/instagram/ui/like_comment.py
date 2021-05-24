import random
import re

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QDateTime, QTime
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QMainWindow, QGridLayout, QGroupBox, QRadioButton, QSizePolicy,
                             QTabWidget, QVBoxLayout, QWidget, QLabel, QSpinBox, QHBoxLayout,
                             QCheckBox, QDateTimeEdit, QTimeEdit, QTableWidget, QTableWidgetItem, QPushButton)

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

    # TODO подумать мб выбрать начальную директорию дрругую
    # username=True - значит пользователи, usernames=False - значит хештеги из файла
    def get_args_list_from_file(self, text_edit_object, is_usernames=True, directory=''):
        if is_usernames:
            desc = 'Выберите файл с именами аккаунтов Instagram'
        else:
            desc = 'Выберите файл со списком хештогов для Instagram'

        file_filter = 'Text files (*.txt)'

        file_name = QtWidgets.QFileDialog.getOpenFileName(
            self, desc, directory, file_filter)[0]

        with open(file_name) as file:
            args_list = file.read()

            text_edit_object.setPlainText(args_list)

    def fill_time_table(self, time_table):
        time_table.setItem(0, 0, QTableWidgetItem('12:00'))
        time_table.setItem(0, 1, QTableWidgetItem('13:00'))
        time_table.setItem(0, 2, QTableWidgetItem('5'))

        time_table.setHorizontalHeaderLabels(['Начало', 'Конец', 'Кол-во лайков'])
        # ставим описание при наведении
        time_table.horizontalHeaderItem(0).setToolTip('Во сколько начинать ставить лайки')
        time_table.horizontalHeaderItem(1).setToolTip('Во сколько заканчивать ставить лайки')
        time_table.horizontalHeaderItem(2).setToolTip('Сколько лайков поставить за период')

        rows_count = time_table.rowCount()
        for row in range(rows_count):
            time_table.setRowHeight(row, 10)

        # включить сорировку
        time_table.setSortingEnabled(True)

    def add_table_element(self, time_table):
        row_count = time_table.rowCount()
        time_table.setRowCount(row_count + 1)
        time_table.setRowHeight(row_count, 10)

    class Tab:
        parent_window = None
        tab = None

        def __init__(self, parent_window):
            self.parent_window = parent_window

        def fill_tab(self, gbox_desc_main, func_desc, count_desc, gbox_desc_limit,
                     block_pause_lbl, day_limit_desc, time_lbl, is_usernames, is_comments=False):
            # левая часть окна с настройками
            main_group_box = QGroupBox(gbox_desc_main)

            # метка, описывающая че в текстарею писать
            func_list_lbl = QtWidgets.QLabel(func_desc)

            # список имен пользователей, комментов или хештегов из файла (в столбик)
            args_list_from_file_btn = QtWidgets.QPushButton('Из файла')
            # добавляем функционал на кнопку
            args_list_from_file_btn.clicked.connect(
                lambda: self.parent_window.get_args_list_from_file(self.args_list_text, is_usernames))

            # text_edit со списком агрументов в функцию (в столбик)
            self.args_list_text = QtWidgets.QPlainTextEdit()
            self.args_list_text.setPlaceholderText(func_desc)

            # кол-во действий в день
            count_lbl = QtWidgets.QLabel(count_desc)

            # создаем панель интервалов
            self.count_start = QSpinBox()
            self.count_start.setMinimum(1)
            self.count_start.setMaximum(250)
            self.count_start.setValue(1)
            separator_lbl = QLabel(' - ')
            self.count_end = QSpinBox()
            self.count_end.setMaximum(1)
            self.count_end.setMaximum(500)
            self.count_end.setValue(3)

            # область с лимитами
            task_count_layout = QHBoxLayout()
            task_count_layout.addWidget(self.count_start)
            task_count_layout.addWidget(separator_lbl)
            task_count_layout.addWidget(self.count_end)

            self.random_cbox = QCheckBox('Ставить в случайном порядке')

            # добавляем все элементы в лаяут
            layout = QVBoxLayout()
            # отступы со всех сторон
            layout.setContentsMargins(10, 10, 10, 10)
            layout.addWidget(func_list_lbl)
            layout.addWidget(args_list_from_file_btn)
            layout.addWidget(self.args_list_text)
            # добавим дополнительное поле, если окно для комментов
            if is_comments:
                comment_label = QtWidgets.QLabel('Какой коммент оставить под постом:')
                self.comment = QtWidgets.QLineEdit()
                self.comment.setPlaceholderText('Какой коммент оставить под постом:')

                layout.addWidget(comment_label)
                layout.addWidget(self.comment)
            layout.addWidget(count_lbl)
            layout.addLayout(task_count_layout)
            layout.addWidget(self.random_cbox)
            # стретч чтоб растягивать элементы по окну
            layout.addStretch(1)

            main_group_box.setLayout(layout)
            # layout.setSizePolicy(QSizePolicy.Minimum)

            main_layout = QGridLayout()
            main_layout.addWidget(main_group_box, 0, 0)
            main_layout.addWidget(self.create_limit_gbox(), 0, 1)

            # заносим результат в поле класса и возвращаем его
            self.tab = QWidget()
            self.tab.setLayout(main_layout)
            # main_group_box.setContentsMargins(10, 10, 10, 10)

            return self.tab

        def create_limit_gbox(self, gbox_desc_limit, block_pause_lbl, day_limit_desc, time_lbl):
            # правая часть окна с лимитами действий
            limit_group_box = QGroupBox(gbox_desc_limit)

            pause_between_tasks_label = QtWidgets.QLabel('Пауза между заданиями (сек.)')

            # создаем панель интервалов между заданиями
            self.pause_between_tasks_start = QSpinBox()
            self.pause_between_tasks_start.setMinimum(15)
            self.pause_between_tasks_start.setMaximum(240)
            self.pause_between_tasks_start.setValue(30)
            pause_between_tasks_separator_label = QLabel(' - ')
            self.pause_between_tasks_end = QSpinBox()
            self.pause_between_tasks_end.setMinimum(16)
            self.pause_between_tasks_end.setMaximum(720)
            self.pause_between_tasks_end.setValue(240)

            pause_between_tasks_layout = QHBoxLayout()
            pause_between_tasks_layout.addWidget(self.pause_between_tasks_start)
            pause_between_tasks_layout.addWidget(pause_between_tasks_separator_label)
            pause_between_tasks_layout.addWidget(self.pause_between_tasks_end)

            pause_when_block_label = QtWidgets.QLabel(block_pause_lbl)

            # создаем панель интервалов
            self.pause_block = QtWidgets.QLineEdit('200')
            self.pause_block.setPlaceholderText(block_pause_lbl)

            day_limit_label = QtWidgets.QLabel(day_limit_desc)

            self.day_limit = QtWidgets.QLineEdit('60')
            self.day_limit.setPlaceholderText(day_limit_desc)

            time_label = QtWidgets.QLabel(time_lbl)

            # создаем и заполняем таблицу с периодами работы
            self.time_table = QTableWidget(1, 3)
            self.parent_window.fill_time_table(self.time_table)

            table_button = QPushButton('Добавить период')
            table_button.clicked.connect(lambda: self.parent_window.add_table_element(self.time_table))

            table_layout = QVBoxLayout()
            table_layout.setContentsMargins(5, 5, 5, 5)
            table_layout.addWidget(self.time_table)
            table_layout.addWidget(table_button)

            vbox = QVBoxLayout()
            vbox.addWidget(pause_between_tasks_label)
            vbox.addLayout(pause_between_tasks_layout)
            vbox.addWidget(pause_when_block_label)
            vbox.addWidget(self.pause_block)
            vbox.addWidget(day_limit_label)
            vbox.addWidget(self.day_limit)
            vbox.addWidget(time_label)
            vbox.addLayout(table_layout)
            vbox.addStretch(1)

            limit_group_box.setLayout(vbox)

            return limit_group_box

    def fill_like_users_tab(self):
        return self.Tab(self).fill_tab('Кому будем ставить лайки:', 'Список имен аккаунтов в Instagram (в столбик)',
                                       'Кол-во лайкнутых постов за день', 'Лимиты лайков по пользователям:',
                                       'Пауза при блокировке лайков (мин.)', 'Лимит лайков на день',
                                       'Время для лайков в течение дня', is_usernames=True)

    def fill_like_donors_tab(self):
        return self.Tab(self).fill_tab('Кому будем ставить лайки:',
                                       'Список доноров, у которых нужно взять подписчиков в Instagram (в столбик)',
                                       'Кол-во лайкнутых постов за день', 'Лимиты лайков по подписчикам:',
                                       'Пауза при блокировке лайков (мин.)', 'Лимит лайков на день',
                                       'Время для лайков в течение дня', is_usernames=True)

    def fill_like_hashtag_tab(self):
        return self.Tab(self).fill_tab('Кому будем ставить лайки:',
                                       'Список хештегов, по которым нужно лайкнуть в Instagram (в столбик, без решетки)',
                                       'Кол-во лайкнутых постов за день', 'Лимиты лайков по хештегам:',
                                       'Пауза при блокировке лайков (мин.)', 'Лимит лайков на день',
                                       'Время для лайков в течение дня', is_usernames=False)

    def fill_comment_users_tab(self):
        return self.Tab(self).fill_tab('Кому будем ставить лайки:',
                                       'Список имен аккаунтов в Instagram (в столбик)',
                                       'Кол-во оставляемых в день комментариев',
                                       'Лимиты комментариев по пользователям:',
                                       'Пауза при блокировке комментариев (мин.)', 'Лимит комментариев на день',
                                       'Время для комментариев в течение дня', is_usernames=True, is_comments=True)

    def fill_comment_donors_tab(self):
        return self.Tab(self).fill_tab('Кому будем ставить лайки:',
                                       'Список доноров, у которых нужно взять подписчиков в Instagram (в столбик)',
                                       'Кол-во оставляемых в день комментариев',
                                       'Лимиты комментариев по подписчикам:',
                                       'Пауза при блокировке комментариев (мин.)', 'Лимит комментариев на день',
                                       'Время для комментариев в течение дня', is_usernames=True, is_comments=True)

    def fill_comment_hashtag_tab(self):
        return self.Tab(self).fill_tab('Кому будем ставить лайки:',
                                       'Список хештегов, по которым нужно лайкнуть в Instagram (в столбик, без решетки)',
                                       'Кол-во оставляемых в день комментариев',
                                       'Лимиты комментариев по хештегам:',
                                       'Пауза при блокировке комментариев (мин.)', 'Лимит комментариев на день',
                                       'Время для комментариев в течение дня', is_usernames=False, is_comments=True)

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
