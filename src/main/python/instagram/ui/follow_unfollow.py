import re

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QMainWindow, QGridLayout, QGroupBox, QRadioButton, QSizePolicy,
                             QTabWidget, QVBoxLayout, QWidget, QCheckBox, QHBoxLayout, QSpinBox, QLabel, QPushButton,
                             QTableWidget, QTableWidgetItem)

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
        follow_tab.addTab(self.fill_follow_subs_tab(), 'На подписчиков')
        follow_tab.addTab(self.fill_follow_hashtag_tab(), 'По хештегам')

        return follow_tab

    # TODO подумать мб выбрать начальную директорию дрругую
    def get_usernames_from_file(self, text_edit_object=None, directory=''):
        usernames_file_filter = 'Text files (*.txt)'
        usernames_file_name = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Выберите файл с именами аккаунтов Instagram', directory, usernames_file_filter)[0]

        with open(usernames_file_name) as file:
            username_list = file.read()

            text_edit_object.setPlainText(username_list)

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

        # enable sorting
        time_table.setSortingEnabled(True)

    def add_table_element(self, time_table):
        row_count = time_table.rowCount()
        time_table.setRowCount(row_count + 1)
        time_table.setRowHeight(row_count, 10)

    def fill_follow_users_tab(self):
        main_group_box = QGroupBox('Список пользователей:')

        usernames_label = QtWidgets.QLabel('Список имен аккаунтов в Instagram (в столбик)')

        usernames_from_file_button = QtWidgets.QPushButton('Из файла')
        # добавляем функционал на кнопку
        usernames_from_file_button.clicked.connect(
            lambda: self.get_usernames_from_file(self.follow_users_usernames_text_edit))

        self.follow_users_usernames_text_edit = QtWidgets.QPlainTextEdit()
        self.follow_users_usernames_text_edit.setPlaceholderText('Список имен аккаунтов в Instagram (в столбик)')

        follow_count_label = QtWidgets.QLabel('Кол-во подписок на пользователей в день')

        # создаем панель интервалов лайков
        follow_count_start = QSpinBox()
        follow_count_start.setMinimum(1)
        follow_count_start.setMaximum(250)
        follow_count_start.setValue(1)
        follow_separator_label = QLabel(' - ')
        follow_count_end = QSpinBox()
        follow_count_end.setMaximum(1)
        follow_count_end.setMaximum(500)
        follow_count_end.setValue(3)

        follow_count_layout = QHBoxLayout()
        follow_count_layout.addWidget(follow_count_start)
        follow_count_layout.addWidget(follow_separator_label)
        follow_count_layout.addWidget(follow_count_end)

        follow_random_checkbox = QCheckBox('Ставить в случайном порядке')

        # follow_button = QtWidgets.QPushButton('Подписаться на аккаунты')
        # # добавляем функционал на кнопку
        # follow_button.clicked.connect(lambda: self.follow_users(
        #     self.follow_users_usernames_text_edit.toPlainText()))

        follow_layout = QVBoxLayout()
        follow_layout.setContentsMargins(10, 10, 10, 10)
        follow_layout.addWidget(usernames_label)
        follow_layout.addWidget(usernames_from_file_button)
        follow_layout.addWidget(self.follow_users_usernames_text_edit)
        follow_layout.addWidget(follow_count_label)
        follow_layout.addLayout(follow_count_layout)
        follow_layout.addWidget(follow_random_checkbox)
        follow_layout.addStretch(1)

        main_group_box.setLayout(follow_layout)

        limit_group_box = QGroupBox('Лимиты подписок по пользователям:')

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

        pause_when_block_label = QtWidgets.QLabel('Пауза при блокировке подписок (мин.)')

        # создаем панель интервалов лайков
        pause_when_block = QtWidgets.QLineEdit('200')
        pause_when_block.setPlaceholderText('Рекомендуемый лимит подписок на день')

        day_limit_label = QtWidgets.QLabel('Рекомендуемый лимит подписок на день')

        day_limit_line = QtWidgets.QLineEdit('60')
        day_limit_line.setPlaceholderText('Рекомендуемый лимит подписок на день')

        time_label = QtWidgets.QLabel('Время для подписок в течение дня')

        # создаем и заполняем таблицу с периодами работы
        self.follow_users_time_table = QTableWidget(1, 3)
        self.fill_time_table(self.follow_users_time_table)

        table_button = QPushButton('Добавить период')
        table_button.clicked.connect(lambda: self.add_table_element(self.follow_users_time_table))

        table_layout = QVBoxLayout()
        table_layout.setContentsMargins(5, 5, 5, 5)
        table_layout.addWidget(self.follow_users_time_table)
        table_layout.addWidget(table_button)

        vbox = QVBoxLayout()
        vbox.addWidget(pause_between_tasks_label)
        vbox.addLayout(pause_between_tasks_layout)
        vbox.addWidget(pause_when_block_label)
        vbox.addWidget(pause_when_block)
        vbox.addWidget(day_limit_label)
        vbox.addWidget(day_limit_line)
        vbox.addWidget(time_label)
        vbox.addLayout(table_layout)
        vbox.addStretch(1)

        limit_group_box.setLayout(vbox)

        main_layout = QGridLayout()
        main_layout.addWidget(main_group_box, 0, 0)
        main_layout.addWidget(limit_group_box, 0, 1)

        follow_user_tab = QWidget()
        follow_user_tab.setLayout(main_layout)
        # main_group_box.setContentsMargins(10, 10, 10, 10)

        return follow_user_tab

    def fill_follow_subs_tab(self):
        main_group_box = QGroupBox('Список доноров:')

        function_description = 'Список доноров, у которых нужно взять подписчиков в Instagram (в столбик)'

        usernames_label = QtWidgets.QLabel(function_description)

        usernames_from_file_button = QtWidgets.QPushButton('Из файла')
        # добавляем функционал на кнопку
        usernames_from_file_button.clicked.connect(
            lambda: self.get_usernames_from_file(self.follow_donors_usernames_text_edit))

        self.follow_donors_usernames_text_edit = QtWidgets.QPlainTextEdit()
        self.follow_donors_usernames_text_edit.setPlaceholderText(function_description)

        # follow_button = QtWidgets.QPushButton('Подписаться на аккаунты')
        # # добавляем функционал на кнопку
        # follow_button.clicked.connect(lambda: self.follow_donors(
        #     self.follow_donors_usernames_text_edit.toPlainText()))

        follow_count_label = QtWidgets.QLabel('Кол-во подписок на доноров в день')

        # создаем панель интервалов лайков
        follow_count_start = QSpinBox()
        follow_count_start.setMinimum(1)
        follow_count_start.setMaximum(250)
        follow_count_start.setValue(1)
        follow_separator_label = QLabel(' - ')
        follow_count_end = QSpinBox()
        follow_count_end.setMaximum(1)
        follow_count_end.setMaximum(500)
        follow_count_end.setValue(3)

        follow_count_layout = QHBoxLayout()
        follow_count_layout.addWidget(follow_count_start)
        follow_count_layout.addWidget(follow_separator_label)
        follow_count_layout.addWidget(follow_count_end)

        follow_random_checkbox = QCheckBox('Ставить в случайном порядке')

        # follow_button = QtWidgets.QPushButton('Подписаться на аккаунты')
        # # добавляем функционал на кнопку
        # follow_button.clicked.connect(lambda: self.follow_users(
        #     self.follow_users_usernames_text_edit.toPlainText()))

        follow_layout = QVBoxLayout()
        follow_layout.setContentsMargins(10, 10, 10, 10)
        follow_layout.addWidget(usernames_label)
        follow_layout.addWidget(usernames_from_file_button)
        follow_layout.addWidget(self.follow_donors_usernames_text_edit)
        follow_layout.addWidget(follow_count_label)
        follow_layout.addLayout(follow_count_layout)
        follow_layout.addWidget(follow_random_checkbox)
        follow_layout.addStretch(1)

        main_group_box.setLayout(follow_layout)

        limit_group_box = QGroupBox('Лимиты подписок по донорам:')

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

        pause_when_block_label = QtWidgets.QLabel('Пауза при блокировке подписок (мин.)')

        # создаем панель интервалов лайков
        pause_when_block = QtWidgets.QLineEdit('200')
        pause_when_block.setPlaceholderText('Рекомендуемый лимит подписок на день')

        day_limit_label = QtWidgets.QLabel('Рекомендуемый лимит подписок на день')

        day_limit_line = QtWidgets.QLineEdit('60')
        day_limit_line.setPlaceholderText('Рекомендуемый лимит подписок на день')

        time_label = QtWidgets.QLabel('Время для подписок в течение дня')

        # создаем и заполняем таблицу с периодами работы
        self.follow_donors_time_table = QTableWidget(1, 3)
        self.fill_time_table(self.follow_donors_time_table)

        table_button = QPushButton('Добавить период')
        table_button.clicked.connect(lambda: self.add_table_element(self.follow_donors_time_table))

        table_layout = QVBoxLayout()
        table_layout.setContentsMargins(5, 5, 5, 5)
        table_layout.addWidget(self.follow_donors_time_table)
        table_layout.addWidget(table_button)

        vbox = QVBoxLayout()
        vbox.addWidget(pause_between_tasks_label)
        vbox.addLayout(pause_between_tasks_layout)
        vbox.addWidget(pause_when_block_label)
        vbox.addWidget(pause_when_block)
        vbox.addWidget(day_limit_label)
        vbox.addWidget(day_limit_line)
        vbox.addWidget(time_label)
        vbox.addLayout(table_layout)
        vbox.addStretch(1)

        limit_group_box.setLayout(vbox)

        main_layout = QGridLayout()
        main_layout.addWidget(main_group_box, 0, 0)
        main_layout.addWidget(limit_group_box, 0, 1)

        follow_user_tab = QWidget()
        follow_user_tab.setLayout(main_layout)
        # main_group_box.setContentsMargins(10, 10, 10, 10)

        return follow_user_tab

    def fill_follow_hashtag_tab(self):

        def get_hashtags_from_file(parent=None, text_edit_object=None, directory=''):
            hashtags_file_filter = 'Text files (*.txt)'
            hashtags_file_name = QtWidgets.QFileDialog.getOpenFileName(
                parent, 'Выберите файл со списком хештогов для Instagram',
                directory, hashtags_file_filter)[0]

            with open(hashtags_file_name) as file:
                username_list = file.read()

                text_edit_object.setPlainText(username_list)

        main_group_box = QGroupBox('Список хэштегов:')

        function_description = 'Список хештегов, по которым нужно лайкнуть в Instagram (в столбик, без решетки)'

        usernames_label = QtWidgets.QLabel(function_description)

        usernames_from_file_button = QtWidgets.QPushButton('Из файла')
        # добавляем функционал на кнопку
        usernames_from_file_button.clicked.connect(
            lambda: get_hashtags_from_file(self, self.follow_hashtags_usernames_text_edit))

        self.follow_hashtags_usernames_text_edit = QtWidgets.QPlainTextEdit()
        self.follow_hashtags_usernames_text_edit.setPlaceholderText(function_description)

        # follow_button = QtWidgets.QPushButton('Подписаться по хештегам')
        # # добавляем функционал на кнопку
        # follow_button.clicked.connect(lambda: self.follow_hashtags(
        #     self.follow_hashtags_usernames_text_edit.toPlainText()))

        follow_count_label = QtWidgets.QLabel('Кол-во подписок по хэштегам в день')

        # создаем панель интервалов лайков
        follow_count_start = QSpinBox()
        follow_count_start.setMinimum(1)
        follow_count_start.setMaximum(250)
        follow_count_start.setValue(1)
        follow_separator_label = QLabel(' - ')
        follow_count_end = QSpinBox()
        follow_count_end.setMaximum(1)
        follow_count_end.setMaximum(500)
        follow_count_end.setValue(3)

        follow_count_layout = QHBoxLayout()
        follow_count_layout.addWidget(follow_count_start)
        follow_count_layout.addWidget(follow_separator_label)
        follow_count_layout.addWidget(follow_count_end)

        follow_random_checkbox = QCheckBox('Ставить в случайном порядке')

        # follow_button = QtWidgets.QPushButton('Подписаться на аккаунты')
        # # добавляем функционал на кнопку
        # follow_button.clicked.connect(lambda: self.follow_users(
        #     self.follow_users_usernames_text_edit.toPlainText()))

        follow_layout = QVBoxLayout()
        follow_layout.setContentsMargins(10, 10, 10, 10)
        follow_layout.addWidget(usernames_label)
        follow_layout.addWidget(usernames_from_file_button)
        follow_layout.addWidget(self.follow_hashtags_usernames_text_edit)
        follow_layout.addWidget(follow_count_label)
        follow_layout.addLayout(follow_count_layout)
        follow_layout.addWidget(follow_random_checkbox)
        follow_layout.addStretch(1)

        main_group_box.setLayout(follow_layout)

        limit_group_box = QGroupBox('Лимиты подписок по хэштегам:')

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

        pause_when_block_label = QtWidgets.QLabel('Пауза при блокировке подписок (мин.)')

        # создаем панель интервалов лайков
        pause_when_block = QtWidgets.QLineEdit('200')
        pause_when_block.setPlaceholderText('Рекомендуемый лимит подписок на день')

        day_limit_label = QtWidgets.QLabel('Рекомендуемый лимит подписок на день')

        day_limit_line = QtWidgets.QLineEdit('60')
        day_limit_line.setPlaceholderText('Рекомендуемый лимит подписок на день')

        time_label = QtWidgets.QLabel('Время для подписок в течение дня')

        # создаем и заполняем таблицу с периодами работы
        self.follow_hashtags_time_table = QTableWidget(1, 3)
        self.fill_time_table(self.follow_hashtags_time_table)

        table_button = QPushButton('Добавить период')
        table_button.clicked.connect(lambda: self.add_table_element(self.follow_hashtags_time_table))

        table_layout = QVBoxLayout()
        table_layout.setContentsMargins(5, 5, 5, 5)
        table_layout.addWidget(self.follow_hashtags_time_table)
        table_layout.addWidget(table_button)

        vbox = QVBoxLayout()
        vbox.addWidget(pause_between_tasks_label)
        vbox.addLayout(pause_between_tasks_layout)
        vbox.addWidget(pause_when_block_label)
        vbox.addWidget(pause_when_block)
        vbox.addWidget(day_limit_label)
        vbox.addWidget(day_limit_line)
        vbox.addWidget(time_label)
        vbox.addLayout(table_layout)
        vbox.addStretch(1)

        limit_group_box.setLayout(vbox)

        main_layout = QGridLayout()
        main_layout.addWidget(main_group_box, 0, 0)
        main_layout.addWidget(limit_group_box, 0, 1)

        follow_user_tab = QWidget()
        follow_user_tab.setLayout(main_layout)
        # main_group_box.setContentsMargins(10, 10, 10, 10)

        return follow_user_tab

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
        main_group_box = QGroupBox('Выберите режим отписки')

        unfollow_radio_smart = QRadioButton('Умная отписка')
        unfollow_radio_all = QRadioButton('От всех')
        # unfollow_button.clicked.connect(lambda: self.unfollow_all())
        # unfollow_button.clicked.connect(lambda: self.unfollow_smart())

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.addWidget(unfollow_radio_smart)
        layout.addWidget(unfollow_radio_all)
        layout.addStretch(1)

        main_group_box.setLayout(layout)

        limit_group_box = QGroupBox('Лимиты отписок:')

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

        pause_when_block_label = QtWidgets.QLabel('Пауза при блокировке отписок (мин.)')

        # создаем панель интервалов лайков
        pause_when_block = QtWidgets.QLineEdit('200')
        pause_when_block.setPlaceholderText('Рекомендуемый лимит отписок на день')

        day_limit_label = QtWidgets.QLabel('Рекомендуемый лимит отписок на день')

        day_limit_line = QtWidgets.QLineEdit('60')
        day_limit_line.setPlaceholderText('Рекомендуемый лимит отписок на день')

        time_label = QtWidgets.QLabel('Время для отписок в течение дня')

        # создаем и заполняем таблицу с периодами работы
        self.unfollow_users_time_table = QTableWidget(1, 3)
        self.fill_time_table(self.unfollow_users_time_table)

        table_button = QPushButton('Добавить период')
        table_button.clicked.connect(lambda: self.add_table_element(self.unfollow_users_time_table))

        table_layout = QVBoxLayout()
        table_layout.setContentsMargins(5, 5, 5, 5)
        table_layout.addWidget(self.unfollow_users_time_table)
        table_layout.addWidget(table_button)

        vbox = QVBoxLayout()
        vbox.addWidget(pause_between_tasks_label)
        vbox.addLayout(pause_between_tasks_layout)
        vbox.addWidget(pause_when_block_label)
        vbox.addWidget(pause_when_block)
        vbox.addWidget(day_limit_label)
        vbox.addWidget(day_limit_line)
        vbox.addWidget(time_label)
        vbox.addLayout(table_layout)
        vbox.addStretch(1)

        limit_group_box.setLayout(vbox)

        main_layout = QGridLayout()
        main_layout.addWidget(main_group_box, 0, 0)
        main_layout.addWidget(limit_group_box, 0, 1)

        unfollow_tab = QTabWidget()
        unfollow_tab.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Ignored)
        unfollow_tab.setLayout(main_layout)

        return unfollow_tab

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
