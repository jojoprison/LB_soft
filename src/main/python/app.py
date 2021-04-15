import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLineEdit,
                             QStyleFactory)
from fbs_runtime.application_context.PyQt5 import ApplicationContext

from instagram.ui.login import InstagramLoginWindow


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


if __name__ == "__main__":
    # 1. Instantiate ApplicationContext
    appctxt = ApplicationContext()
    # app = QtWidgets.QApplication(sys.argv)

    main = AppLoginWindow()
    main.show()

    # 2. Invoke appctxt.app.exec_()
    sys.exit(appctxt.app.exec_())
    # sys.exit(app.exec_())
