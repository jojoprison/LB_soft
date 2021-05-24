from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QApplication, QMainWindow, QCheckBox, QComboBox, QDateTimeEdit,
                             QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
                             QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
                             QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
                             QVBoxLayout, QWidget, QTableWidgetItem)
from past.builtins import xrange

from instagram.ui.like_comment import InstagramLikeCommentWindow
from instagram.ui.follow_unfollow import InstagramFollowUnfollow
from instagram.ui.direct import InstagramDirect
from instagram.ui.strategy import InstagramStrategy


# наследуем от QMainWindow
class InstagramMainWindow(QMainWindow):
    bot = None

    # вызываем конструктор супер класса обычного виндова
    def __init__(self):
        # вызываем конструктор без родителя чтобы не скрывалась иконка приложения из таскбара
        super(InstagramMainWindow, self).__init__()

        self.setWindowTitle('Instagram Bot')

        # self.setGeometry(300, 250, 350, 200)
        self.resize(1000, 600)

        username_info_label = QLabel('Аккаунт:')
        username_label = QLabel('instagram_username')

        topLayout = QHBoxLayout()
        topLayout.addStretch(1)
        topLayout.addWidget(username_info_label)
        topLayout.addWidget(username_label)

        # создаем все части окна
        self.create_buttons_group_box()
        self.create_limits_info_group_box()
        self.create_start_group_box()
        self.create_log_group_box()

        mainLayout = QGridLayout()
        # формируем шапку
        mainLayout.addLayout(topLayout, 0, 0, 1, 2)
        mainLayout.addWidget(self.buttons_group_box, 1, 0)
        mainLayout.addWidget(self.limits_group_box, 1, 1)
        mainLayout.addWidget(self.log_group_box, 2, 0)
        mainLayout.addWidget(self.start_group_box, 2, 1)
        # коофицент растяжение колонки (растягивается сначала та, у которой он больше)
        mainLayout.setRowStretch(1, 2)
        mainLayout.setRowStretch(2, 1)
        # коофицент растяжение колонки (растягивается сначала та, у которой он больше)
        mainLayout.setColumnStretch(0, 2)
        mainLayout.setColumnStretch(1, 1)

        self.setCentralWidget(QtWidgets.QWidget(self))
        self.centralWidget().setLayout(mainLayout)

        # TODO для вкладок
        # self.tabs = QtWidgets.QTabWidget()
        # self.tasks_tab()
        # self.tabs.addTab(self.central_widget, "Factors")

    def create_buttons_group_box(self):
        self.buttons_group_box = QGroupBox('Выберите задачу для выполнения:')

        like_comment_button = QPushButton('Лайки/комментарии')
        # будет подсвечиваться и выбираться про нажатии Enter
        like_comment_button.setDefault(True)
        # добавляем функционал на кнопку
        like_comment_button.clicked.connect(lambda: self.open_like_comment_window())

        follow_unfollow_button = QPushButton('Подписки/отписки')
        follow_unfollow_button.clicked.connect(lambda: self.open_follow_unfollow_window())

        # posting_button = QPushButton('Постинг')
        strategy_button = QPushButton('Настройка стратегии')
        strategy_button.clicked.connect(lambda: self.open_strategy_window())

        main_limit_label = QtWidgets.QLabel('Общий лимит действий')
        main_limit_line = QtWidgets.QLineEdit('600')
        main_limit_line.setPlaceholderText('Введите общий лимит действий')

        # TODO добавить при дебаге
        # direct_msg_button = QPushButton('Директ')
        # direct_msg_button.clicked.connect(lambda: self.open_direct_window())

        layout = QVBoxLayout()
        layout.addWidget(like_comment_button)
        layout.addWidget(follow_unfollow_button)
        # layout.addWidget(posting_button)
        # layout.addWidget(direct_msg_button)
        layout.addWidget(strategy_button)
        layout.addWidget(main_limit_label)
        layout.addWidget(main_limit_line)
        layout.addStretch(1)
        self.buttons_group_box.setLayout(layout)

    def create_limits_info_group_box(self):
        self.limits_group_box = QGroupBox('Лимиты по заданиям:')

        like_limit = QtWidgets.QLabel('Лимиты лайков')
        comment_limit = QtWidgets.QLabel('Лимиты комментов')
        follow_limit = QtWidgets.QLabel('Лимиты подписок')
        unfollow_limit = QtWidgets.QLabel('Лимиты комментов')

        # TODO добавить при дебаге
        # direct_msg_button = QPushButton('Директ')
        # direct_msg_button.clicked.connect(lambda: self.open_direct_window())

        layout = QVBoxLayout()
        layout.addWidget(like_limit)
        layout.addWidget(comment_limit)
        # layout.addWidget(posting_button)
        # layout.addWidget(direct_msg_button)
        layout.addWidget(follow_limit)
        layout.addWidget(unfollow_limit)
        layout.addStretch(1)

        self.limits_group_box.setLayout(layout)

    def create_start_group_box(self):
        self.start_group_box = QGroupBox()

        start_button = QPushButton('Запустить бота')
        start_button.clicked.connect(lambda: self.get_inner_field())

        layout = QVBoxLayout()
        layout.addWidget(start_button)
        layout.addStretch(1)
        self.start_group_box.setLayout(layout)

    def create_log_group_box(self):
        self.log_group_box = QGroupBox('Логи:')

        log_area = QtWidgets.QTextBrowser()

        log_area.setPlainText('LBLBLBLB')

        # tab2hbox = QHBoxLayout()
        # tab2hbox.setContentsMargins(5, 5, 5, 5)
        # tab2hbox.addWidget(log_area)

        layout = QVBoxLayout()
        layout.addWidget(log_area)
        layout.addStretch(1)

        self.log_group_box.setLayout(layout)

    def add_functions(self):
        self.instagram_login_button.clicked.connect(lambda: self.login_app(
            self.instagram_login.text(),
            self.instagram_password.text()))

    def open_like_comment_window(self):
        self.like_comment_window = InstagramLikeCommentWindow(self.bot)
        self.like_comment_window.show()

    def open_follow_unfollow_window(self):
        self.follow_unfollow_window = InstagramFollowUnfollow(self.bot)
        self.follow_unfollow_window.show()

    def open_direct_window(self):
        self.direct_window = InstagramDirect(self.bot)
        self.direct_window.show()

    def open_strategy_window(self):
        self.strategy_window = InstagramStrategy(self.bot)
        self.strategy_window.show()

    def get_inner_field(self):
        print(self.like_comment_window.users_comment.text())
