from PyQt5 import QtCore
from PyQt5.QtWidgets import (QMainWindow, QLineEdit,
                             QPushButton, QWidget)

from instagram.ui.main import InstagramMainWindow
import instagram.instagram_bot_start as inst_bot


class InstagramLoginWindow(QMainWindow):
    def __init__(self):
        # вызываем конструктор без родителя чтобы не скрывалась иконка приложения из таскбара
        super(InstagramLoginWindow, self).__init__()

        self.resize(600, 300)

        self.central_widget = QWidget(self)
        self.central_widget.setObjectName('central_widget')
        self.setCentralWidget(self.central_widget)

        self.instagram_login = QLineEdit(self.centralWidget())
        # слева, сверху, ширина, высота
        self.instagram_login.setGeometry(QtCore.QRect(200, 60, 1, 20))
        self.instagram_login.setAutoFillBackground(False)
        self.instagram_login.setInputMask('')
        self.instagram_login.setObjectName('instagram_login')
        self.instagram_login.setFixedSize(200, 40)
        self.instagram_login.setPlaceholderText('Инстаграм логин')

        self.instagram_password = QLineEdit(self.centralWidget())
        self.instagram_password.setEchoMode(QLineEdit.Password)
        self.instagram_password.setGeometry(QtCore.QRect(200, 100, 100, 30))
        self.instagram_password.setObjectName('instagram_password')
        self.instagram_password.setFixedSize(200, 40)
        self.instagram_password.setPlaceholderText('Инстаграм пароль')

        self.instagram_login_button = QPushButton(self.centralWidget())
        self.instagram_login_button.setGeometry(QtCore.QRect(200, 200, 101, 31))
        self.instagram_login_button.setObjectName('instagram_login_button')
        self.instagram_login_button.setText('Авторизоваться')

        # добавляем функционал на кнопки
        self.add_functions()

    def add_functions(self):
        self.instagram_login_button.clicked.connect(lambda: self.login_app(
            self.instagram_login.text(),
            self.instagram_password.text()))

    def login_app(self, login, password):
        if login and password:
            print(login + ':' + password)

            self.hide()

            bot = inst_bot.create()
            bot.login()

            bot.login()

            bot.get_account_info()

            # не указывать парента, чтоб в таскбаре создавалась новая иконка приложения
            self.inst_window = InstagramMainWindow(bot)
            self.inst_window.show()
