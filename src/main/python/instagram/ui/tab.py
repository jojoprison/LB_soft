from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QGridLayout, QGroupBox, QVBoxLayout, QWidget, QLabel, QSpinBox, QHBoxLayout,
                             QCheckBox, QTableWidget, QPushButton, QTableWidgetItem, QRadioButton)


# класс для создания окон
class Tab:
    # родительское окно, чтобы поверх него создавать новое
    parent_window = None
    # поле с самим объектом создаваемого окна
    tab = None
    # мод окна: like, comment, follow
    mode = None

    # получаем объект окна
    def get_tab(self):
        return self.tab

    def __init__(self, parent_window, mode, is_usernames, func_desc, gbox_desc_limit):

        self.parent_window = parent_window
        self.mode = mode

        # выбираем слово, которое будем вставлять в некоторые описания
        if not self.mode == 'like':
            self.mode_word = 'лайков'
        elif self.mode == 'comment':
            self.mode_word = 'комментариев'
        elif self.mode == 'follow':
            self.mode_word = 'подписок'
        else:
            self.mode_word = 'отписок'

        main_layout = QGridLayout()
        main_layout.addWidget(self.create_main_gbox(func_desc, is_usernames), 0, 0)
        main_layout.addWidget(self.create_limit_gbox(gbox_desc_limit), 0, 1)

        # заносим результат в поле класса и возвращаем его
        self.tab = QWidget()
        self.tab.setLayout(main_layout)
        # main_group_box.setContentsMargins(10, 10, 10, 10)

    # создаем левую часть окна
    def create_main_gbox(self, func_desc, is_usernames):

        # левая часть окна с настройками
        main_group_box = None

        # для отписок создаем отдельное окно
        if self.mode == 'unfollow':
            main_group_box = QGroupBox('Как будем отписываться')

            unfollow_radio_smart = QRadioButton('Умная отписка')
            unfollow_radio_all = QRadioButton('От всех')
            # TODO пришвартовать функционал кнопочек куда нить в другое место
            # unfollow_button.clicked.connect(lambda: self.unfollow_all())
            # unfollow_button.clicked.connect(lambda: self.unfollow_smart())

            layout = QVBoxLayout()
            layout.setContentsMargins(10, 10, 10, 10)
            layout.addWidget(unfollow_radio_smart)
            layout.addWidget(unfollow_radio_all)
            layout.addStretch(1)

            main_group_box.setLayout(layout)
        else:
            # метка, описывающая че в текстарею писать
            func_list_lbl = QtWidgets.QLabel('Список имен аккаунтов в Instagram (в столбик)')

            # список имен пользователей, комментов или хештегов из файла (в столбик)
            args_list_from_file_btn = QtWidgets.QPushButton('Из файла')
            # добавляем функционал на кнопку
            args_list_from_file_btn.clicked.connect(
                lambda: self.parent_window.get_args_list_from_file(self.args_list_text, is_usernames))

            # text_edit со списком агрументов в функцию (в столбик)
            self.args_list_text = QtWidgets.QPlainTextEdit()
            self.args_list_text.setPlaceholderText(func_desc)

            # кол-во действий в день
            count_lbl = None

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

            # заполняем динамические элементы окна
            if self.mode == 'like':
                main_group_box = QGroupBox('Кому будем ставить лайки:')
                count_lbl = QtWidgets.QLabel('Кол-во лайкнутых постов за день')
            elif self.mode == 'comment':
                main_group_box = QGroupBox('Кому будем оставлять комментарии:')
                count_lbl = QtWidgets.QLabel('Кол-во оставляемых за день комментариев')
            elif self.mode == 'follow':
                main_group_box = QGroupBox('На кого будем подписываться:')
                count_lbl = QtWidgets.QLabel('Кол-во подписок за день')

            # добавляем все элементы в лаяут
            layout = QVBoxLayout()
            # отступы со всех сторон
            layout.setContentsMargins(10, 10, 10, 10)
            layout.addWidget(func_list_lbl)
            layout.addWidget(args_list_from_file_btn)
            layout.addWidget(self.args_list_text)
            # добавим дополнительное поле, если окно для комментов
            if self.mode == 'comment':
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

        return main_group_box

    def create_limit_gbox(self, limit_gbox_desc):

        # правая часть окна с лимитами действий
        limit_group_box = QGroupBox(limit_gbox_desc)

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

        pause_block_desc = f'Пауза при блокировке {self.mode_word} (мин.)'

        # надпись, на какой модуль будет ставиться пауза
        pause_when_block_label = QLabel(pause_block_desc)

        # создаем панель интервалов
        self.pause_block = QtWidgets.QLineEdit('200')
        self.pause_block.setPlaceholderText(pause_block_desc)

        day_limit_desc = f'Лимит {self.mode_word} на день'

        # лимит действий в день
        day_limit_label = QLabel(day_limit_desc)

        self.day_limit = QtWidgets.QLineEdit('60')
        self.day_limit.setPlaceholderText(day_limit_desc)

        # время для действий в течение дня
        time_label = QLabel(f'Время для {self.mode_word} в течение дня')

        # создаем и заполняем таблицу с периодами работы
        self.time_table = QTableWidget(1, 3)
        self.fill_time_table(self.time_table)

        table_button = QPushButton('Добавить период')
        table_button.clicked.connect(lambda: self.add_table_element(self.time_table))

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

    def fill_time_table(self, time_table):
        time_table.setItem(0, 0, QTableWidgetItem('12:00'))
        time_table.setItem(0, 1, QTableWidgetItem('13:00'))
        time_table.setItem(0, 2, QTableWidgetItem('5'))

        time_table.setHorizontalHeaderLabels(['Начало', 'Конец', 'Кол-во'])

        # ставим описание при наведении
        if self.mode == 'like':
            time_table.horizontalHeaderItem(0).setToolTip('Во сколько начинать ставить лайки')
            time_table.horizontalHeaderItem(1).setToolTip('Во сколько заканчивать ставить лайки')
            time_table.horizontalHeaderItem(2).setToolTip('Сколько лайков поставить за период')
        elif self.mode == 'comment':
            time_table.horizontalHeaderItem(0).setToolTip('Во сколько начинать ставить комментарии')
            time_table.horizontalHeaderItem(1).setToolTip('Во сколько заканчивать ставить комментарии')
            time_table.horizontalHeaderItem(2).setToolTip('Сколько комментарией поставить за период')
        elif self.mode == 'follow':
            time_table.horizontalHeaderItem(0).setToolTip('Во сколько начинать подписываться')
            time_table.horizontalHeaderItem(1).setToolTip('Во сколько заканчивать подписываться')
            time_table.horizontalHeaderItem(2).setToolTip('Сколько подписок осуществлять за период')
        elif self.mode == 'unfollow':
            time_table.horizontalHeaderItem(0).setToolTip('Во сколько начинать отписываться')
            time_table.horizontalHeaderItem(1).setToolTip('Во сколько заканчивать отписываться')
            time_table.horizontalHeaderItem(2).setToolTip('Сколько отписок осуществлять за период')

        rows_count = time_table.rowCount()
        for row in range(rows_count):
            time_table.setRowHeight(row, 10)

        # включить сорировку
        time_table.setSortingEnabled(True)

    def add_table_element(self, time_table):
        row_count = time_table.rowCount()
        time_table.setRowCount(row_count + 1)
        time_table.setRowHeight(row_count, 10)

    # TODO подумать мб выбрать начальную директорию дрругую
    # username=True - значит пользователи, usernames=False - значит хештеги из файла
    def get_args_list_from_file(self, text_edit_object, is_usernames=True, directory=''):
        if is_usernames:
            desc = 'Выберите файл с именами аккаунтов Instagram'
        else:
            desc = 'Выберите файл со списком хештогов для Instagram'

        file_filter = 'Text files (*.txt)'

        file_name = QtWidgets.QFileDialog.getOpenFileName(
            self.parent_window, desc, directory, file_filter)[0]

        with open(file_name) as file:
            args_list = file.read()

            text_edit_object.setPlainText(args_list)
