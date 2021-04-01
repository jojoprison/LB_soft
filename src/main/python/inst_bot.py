from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication
import sys
import instagram.main as main


class Ui_MainWindow(QMainWindow):
    def setupUi(self, MainWindow):
        self.main_window = MainWindow

        self.main_window.setObjectName('login_window')
        self.main_window.resize(600, 300)

        text_font = QtGui.QFont()
        text_font.setFamily("Segoe UI Black")
        text_font.setPointSize(11)
        text_font.setBold(True)
        text_font.setWeight(75)

        self.centralwidget = QtWidgets.QWidget(self.main_window)
        self.centralwidget.setObjectName("centralwidget")

        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        # слева, сверху, ширина, высота
        self.lineEdit.setGeometry(QtCore.QRect(200, 60, 1, 20))

        self.lineEdit.setFont(text_font)
        self.lineEdit.setAutoFillBackground(False)
        self.lineEdit.setInputMask("")
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setFixedSize(200, 40)

        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        # слева, сверху,
        self.lineEdit_2.setGeometry(QtCore.QRect(200, 100, 100, 30))
        self.lineEdit_2.setFont(text_font)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setFixedSize(200, 40)

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(200, 200, 101, 31))

        self.pushButton.setFont(text_font)
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(self.main_window)
        QtCore.QMetaObject.connectSlotsByName(self.main_window)

        self.add_functions()
        self.inst_window = InstagramBotWindow(self)

    def add_functions(self):
        self.pushButton.clicked.connect(lambda: self.login_app(self.lineEdit.text(), self.lineEdit_2.text()))

    def login_app(self, login, password):
        if login and password:
            print(login + ':' + password)
            self.inst_window.show()
            self.main_window.hide()

    def retranslateUi(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("login_window", "LB"))
        self.lineEdit.setPlaceholderText(_translate("login_window", "Логин..."))
        self.lineEdit_2.setPlaceholderText(_translate("login_window", "Пароль..."))
        self.pushButton.setText(_translate("login_window", "Войти"))


# наследуем от QMainWindow
class InstagramBotWindow(QMainWindow):
    bot = None

    # вызываем конструктор супер класса обычного виндова с указанием родителя
    def __init__(self, parent=None):
        super(InstagramBotWindow, self).__init__(parent)

        self.setWindowTitle('Instagram Bot')
        # self.setGeometry(300, 250, 350, 200)
        self.setObjectName('main_window')
        self.resize(1000, 600)

        text_font = QtGui.QFont()
        text_font.setFamily("Segoe UI Black")
        text_font.setPointSize(11)
        text_font.setBold(True)
        text_font.setWeight(75)

        self.central_widget = QtWidgets.QWidget(self)
        self.central_widget.setObjectName('inst_central_widget')

        self.post_line_edit = QtWidgets.QLineEdit(self.central_widget)
        self.post_line_edit.setObjectName('post_line_edit')
        # слева, сверху, ширина, высота
        self.post_line_edit.setGeometry(QtCore.QRect(200, 60, 400, 40))
        self.post_line_edit.setFont(text_font)
        self.post_line_edit.setPlaceholderText('Ссылка на пост в Insagram')

        self.comment_line_edit = QtWidgets.QLineEdit(self.central_widget)
        self.comment_line_edit.setObjectName('comment_line_edit')
        self.comment_line_edit.setGeometry(QtCore.QRect(200, 120, 400, 40))
        self.comment_line_edit.setFont(text_font)
        self.comment_line_edit.setPlaceholderText('комментарий...')

        self.bot_button = QtWidgets.QPushButton(self.central_widget)
        self.bot_button.setGeometry(QtCore.QRect(300, 200, 200, 40))
        self.bot_button.setFont(text_font)
        self.bot_button.setObjectName('like_comment_button')
        self.bot_button.setText('Лайк+Коммент')
        # добавляем функционал на кнопку
        self.bot_button.clicked.connect(lambda: self.like_comment_post(
            self.post_line_edit.text(), self.comment_line_edit.text()))

        self.new_text = QtWidgets.QLabel(self)

        self.result_label = QtWidgets.QLabel(self)
        self.result_label.move(100, 100)
        self.result_label.adjustSize()

        self.setCentralWidget(self.central_widget)

        # self.fill_widgets()
        # QtCore.QMetaObject.connectSlotsByName(self)

    # TODO думаю можно без такого заполнителя
    def fill_widgets(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate('main_window', ''))
        self.lineEdit.setPlaceholderText(_translate('main_window', 'blamba'))
        self.bot_button.setText(_translate('main_window', 'LOLO'))

    def login_app(self, login, password):
        if login and password:
            print(login + ':' + password)
            self.inst_window.show()
            self.main_window.hide()

    def like_comment_post(self, post, comment):
        if post:
            self.bot = main.create_bot()
            self.bot.login()

            is_done = self.bot.like_comment_post(post, comment)

            self.bot.close_driver()

            if is_done:
                self.new_text.setText('Готово!')
            else:
                self.new_text.setText('Нудача!')


if __name__ == "__main__":
    # 1. Instantiate ApplicationContext
    appctxt = ApplicationContext()
    # app = QtWidgets.QApplication(sys.argv)

    MainWindow = QtWidgets.QMainWindow()

    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    MainWindow.show()

    # 2. Invoke appctxt.app.exec_()
    sys.exit(appctxt.app.exec_() )
    # sys.exit(app.exec_())
