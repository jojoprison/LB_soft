from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtWidgets import (QApplication, QMainWindow, QCheckBox, QComboBox, QDateTimeEdit,
                             QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
                             QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
                             QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
                             QVBoxLayout, QWidget)

import sys
import instagram.instagram_bot as inst_bot


class AppLoginWindow(QMainWindow):
    def __init__(self, parent=None):
        super(AppLoginWindow, self).__init__(parent)

        # задается на все приложение
        QApplication.setStyle(QStyleFactory.create('Fusion'))

        self.setObjectName('login_window')
        self.resize(600, 300)

        text_font = QtGui.QFont()
        text_font.setFamily('Segoe UI Black')
        text_font.setPointSize(11)
        text_font.setBold(True)
        text_font.setWeight(75)

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName('centralwidget')

        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        # слева, сверху, ширина, высота
        self.lineEdit.setGeometry(QtCore.QRect(200, 60, 1, 20))

        self.lineEdit.setFont(text_font)
        self.lineEdit.setAutoFillBackground(False)
        self.lineEdit.setInputMask('')
        self.lineEdit.setObjectName('lineEdit')
        self.lineEdit.setFixedSize(200, 40)

        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        # слева, сверху,
        self.lineEdit_2.setGeometry(QtCore.QRect(200, 100, 100, 30))
        self.lineEdit_2.setFont(text_font)
        self.lineEdit_2.setObjectName('lineEdit_2')
        self.lineEdit_2.setFixedSize(200, 40)
        self.lineEdit_2.setEchoMode(QLineEdit.Password)

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(200, 200, 101, 31))

        self.pushButton.setFont(text_font)
        self.pushButton.setObjectName('pushButton')
        self.setCentralWidget(self.centralwidget)

        self.retranslate_ui(self)
        QtCore.QMetaObject.connectSlotsByName(self)

        self.add_functions()

    def add_functions(self):
        self.pushButton.clicked.connect(lambda: self.login_app(self.lineEdit.text(), self.lineEdit_2.text()))

    def login_app(self, login, password):
        if login and password:
            print(login + ':' + password)

            self.hide()
            # не указывать парента, чтоб в таскбаре создавалась новая иконка приложения
            self.inst_login_window = InstagramLoginWindow()
            self.inst_login_window.show()

    def retranslate_ui(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("login_window", "LB"))
        self.lineEdit.setPlaceholderText(_translate("login_window", "Логин..."))
        self.lineEdit_2.setPlaceholderText(_translate("login_window", "Пароль..."))
        self.pushButton.setText(_translate("login_window", "Войти"))


class InstagramLoginWindow(QMainWindow):
    def __init__(self):
        # вызываем конструктор без родителя чтобы не скрывалась иконка приложения из таскбара
        super(InstagramLoginWindow, self).__init__()

        self.setObjectName('instagram_login_window')
        self.resize(600, 300)

        self.central_widget = QtWidgets.QWidget(self)
        self.central_widget.setObjectName('central_widget')
        self.setCentralWidget(self.central_widget)

        self.instagram_login = QtWidgets.QLineEdit(self.centralWidget())
        # слева, сверху, ширина, высота
        self.instagram_login.setGeometry(QtCore.QRect(200, 60, 1, 20))
        self.instagram_login.setAutoFillBackground(False)
        self.instagram_login.setInputMask('')
        self.instagram_login.setObjectName('instagram_login')
        self.instagram_login.setFixedSize(200, 40)
        self.instagram_login.setPlaceholderText('Инстаграм логин')

        self.instagram_password = QtWidgets.QLineEdit(self.centralWidget())
        self.instagram_password.setEchoMode(QLineEdit.Password)
        self.instagram_password.setGeometry(QtCore.QRect(200, 100, 100, 30))
        self.instagram_password.setObjectName('instagram_password')
        self.instagram_password.setFixedSize(200, 40)
        self.instagram_password.setPlaceholderText('Инстаграм пароль')

        self.instagram_login_button = QtWidgets.QPushButton(self.centralWidget())
        self.instagram_login_button.setGeometry(QtCore.QRect(200, 200, 101, 31))
        self.instagram_login_button.setObjectName('instagram_login_button')
        self.instagram_login_button.setText('Авторизоваться')

        self.add_functions()

        self.inst_window = InstagramBotWindow()

    def add_functions(self):
        self.instagram_login_button.clicked.connect(lambda: self.login_app(
            self.instagram_login.text(),
            self.instagram_password.text()))

    def login_app(self, login, password):
        if login and password:
            print(login + ':' + password)

            self.hide()
            # не указывать парента, чтоб в таскбаре создавалась новая иконка приложения
            self.inst_window.show()


# наследуем от QMainWindow
class InstagramBotWindow(QMainWindow):
    bot = None

    # вызываем конструктор супер класса обычного виндова
    def __init__(self):
        # вызываем конструктор без родителя чтобы не скрывалась иконка приложения из таскбара
        super(InstagramBotWindow, self).__init__()

        self.setWindowTitle('Instagram Bot')

        # self.setGeometry(300, 250, 350, 200)
        self.setObjectName('main_window')
        self.resize(1000, 600)

        username_info_label = QLabel('Аккаунт:')
        username_label = QLabel('instagram_username')

        topLayout = QHBoxLayout()
        topLayout.addStretch(1)
        topLayout.addWidget(username_info_label)
        topLayout.addWidget(username_label)

        # создаем все части окна
        self.create_buttons_group_box()
        self.create_start_group_box()
        self.create_log_group_box()

        mainLayout = QGridLayout()
        # формируем шапку
        mainLayout.addLayout(topLayout, 0, 0, 1, 2)
        mainLayout.addWidget(self.buttons_group_box, 1, 0)
        mainLayout.addWidget(self.start_group_box, 2, 1)
        mainLayout.addWidget(self.log_group_box, 2, 0)
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

        subscribe_unsubscribe_button = QPushButton('Подписки/отписки')
        like_comment_button = QPushButton('Лайки/комментарии')
        # будет подсвечиваться и выбираться про нажатии Enter
        like_comment_button.setDefault(True)
        # добавляем функционал на кнопку
        like_comment_button.clicked.connect(lambda: self.open_like_comment_window())

        posting_button = QPushButton('Постинг')
        strategy_button = QPushButton('Настройка стратегии')
        direct_msg_button = QPushButton('Директ')

        layout = QVBoxLayout()
        layout.addWidget(like_comment_button)
        layout.addWidget(subscribe_unsubscribe_button)
        layout.addWidget(posting_button)
        layout.addWidget(direct_msg_button)
        layout.addWidget(strategy_button)
        layout.addStretch(1)
        self.buttons_group_box.setLayout(layout)

    def create_start_group_box(self):
        self.start_group_box = QGroupBox()

        start_button = QPushButton('Запустить бота')

        layout = QVBoxLayout()
        layout.addWidget(start_button)
        layout.addStretch(1)
        self.start_group_box.setLayout(layout)

    def create_log_group_box(self):
        self.log_group_box = QGroupBox('Логи:')

        log_area = QTextEdit()

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
        self.central_widget.setObjectName('inst_central_widget')
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

    def create_left_tab_widget(self):
        left_tab_widget = QTabWidget()
        left_tab_widget.setSizePolicy(QSizePolicy.Preferred,
                                      QSizePolicy.Ignored)

        left_tab_widget.addTab(self.fill_likes_tab(), 'Лайки')
        left_tab_widget.addTab(self.fill_comments_tab(), 'Комментарии')

        return left_tab_widget

    def fill_likes_tab(self):
        likes_tab = QTabWidget()
        likes_tab.setSizePolicy(QSizePolicy.Preferred,
                                QSizePolicy.Ignored)

        likes_tab.addTab(self.fill_likes_users_tab(), 'Пользлователю')
        likes_tab.addTab(self.fill_subs_tab(), 'Подписчикам')

        return likes_tab

    def fill_likes_users_tab(self):
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

        self.result_label = QtWidgets.QLabel(self)
        self.result_label.move(100, 100)
        self.result_label.adjustSize()

        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.addWidget(self.post_line_edit)
        layout.addWidget(self.comment_line_edit)
        layout.addWidget(self.bot_button)
        layout.addStretch(1)

        tab = QWidget()
        tab.setLayout(layout)

        return tab

    def fill_subs_tab(self):
        account_username = QtWidgets.QLineEdit()
        account_username.setObjectName('account_username')
        account_username.setGeometry(QtCore.QRect(200, 60, 400, 40))
        account_username.setPlaceholderText('Имя аккаунта в Instagram')

        like_account_button = QtWidgets.QPushButton()
        like_account_button.setGeometry(QtCore.QRect(300, 200, 200, 40))
        like_account_button.setObjectName('like_account_button')
        like_account_button.setText('Лайкнуть аккаунт')
        # добавляем функционал на кнопку
        like_account_button.clicked.connect(lambda: self.put_many_likes(
            account_username.text()))

        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.addWidget(account_username)
        layout.addWidget(like_account_button)
        layout.addStretch(1)

        tab = QWidget()
        tab.setLayout(layout)

        return tab

    def fill_comments_tab(self):
        likes_tab = QTabWidget()
        likes_tab.setSizePolicy(QSizePolicy.Preferred,
                                QSizePolicy.Ignored)

        likes_tab.addTab(self.fill_likes_users_tab(), 'Пользлователю')
        likes_tab.addTab(self.fill_subs_tab(), 'Подписчикам')

        return likes_tab

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

    def like_comment_post(self, post, comment):
        if post:
            if not self.bot:
                self.bot = inst_bot.create()
                self.bot.login()

            is_done = self.bot.like_comment_post(post, comment)

            self.bot.close_driver()

            if is_done:
                self.new_text.setText('Готово!')
            else:
                self.new_text.setText('Нудача!')

    def put_many_likes(self, username):
        if not self.bot:
            self.bot = inst_bot.create()
            self.bot.login()

        is_done = self.bot.put_many_likes(username)

        self.bot.close_driver()


class InstagramLikeCommentWindow(QMainWindow):
    bot = None

    # вызываем конструктор супер класса обычного виндова
    def __init__(self, bot):
        # вызываем конструктор без родителя чтобы не скрывалась иконка приложения из таскбара
        super(InstagramLikeCommentWindow, self).__init__()

        self.bot = bot

        self.setWindowTitle('Истаграм Лайк/Коммент')

        # self.setGeometry(300, 250, 350, 200)
        self.setObjectName('main_window')
        self.resize(1000, 600)

        self.central_widget = QtWidgets.QWidget(self)
        self.central_widget.setObjectName('inst_central_widget')
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

    def create_left_tab_widget(self):
        left_tab_widget = QTabWidget()
        left_tab_widget.setSizePolicy(QSizePolicy.Preferred,
                                      QSizePolicy.Ignored)

        left_tab_widget.addTab(self.fill_first_tab(), 'На пост')
        left_tab_widget.addTab(self.fill_second_tab(), 'По профилю')

        return left_tab_widget

    def fill_first_tab(self):
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

        self.result_label = QtWidgets.QLabel(self)
        self.result_label.move(100, 100)
        self.result_label.adjustSize()

        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.addWidget(self.post_line_edit)
        layout.addWidget(self.comment_line_edit)
        layout.addWidget(self.bot_button)
        layout.addStretch(1)

        tab = QWidget()
        tab.setLayout(layout)

        return tab

    def fill_second_tab(self):
        account_username = QtWidgets.QLineEdit()
        account_username.setObjectName('account_username')
        account_username.setGeometry(QtCore.QRect(200, 60, 400, 40))
        account_username.setPlaceholderText('Имя аккаунта в Instagram')

        like_account_button = QtWidgets.QPushButton()
        like_account_button.setGeometry(QtCore.QRect(300, 200, 200, 40))
        like_account_button.setObjectName('like_account_button')
        like_account_button.setText('Лайкнуть аккаунт')
        # добавляем функционал на кнопку
        like_account_button.clicked.connect(lambda: self.put_many_likes(
            account_username.text()))

        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.addWidget(account_username)
        layout.addWidget(like_account_button)
        layout.addStretch(1)

        tab = QWidget()
        tab.setLayout(layout)

        return tab

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

    def like_comment_post(self, post, comment):
        if post:
            if not self.bot:
                self.bot = inst_bot.create()
                self.bot.login()

            is_done = self.bot.like_comment_post(post, comment)

            self.bot.close_driver()

            if is_done:
                self.new_text.setText('Готово!')
            else:
                self.new_text.setText('Нудача!')

    def put_many_likes(self, username):
        if not self.bot:
            self.bot = inst_bot.create()
            self.bot.login()

        is_done = self.bot.put_many_likes(username)

        self.bot.close_driver()


if __name__ == "__main__":
    # 1. Instantiate ApplicationContext
    appctxt = ApplicationContext()
    # app = QtWidgets.QApplication(sys.argv)

    main = AppLoginWindow()
    main.show()

    # 2. Invoke appctxt.app.exec_()
    sys.exit(appctxt.app.exec_())
    # sys.exit(app.exec_())
