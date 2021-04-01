from PyQt5.QtWidgets import QMessageBox, QApplication, QMainWindow
from PyQt5 import QtCore, QtGui, QtWidgets

import sys


# это наследование
class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.setWindowTitle('Простая программа')
        self.setGeometry(300, 250, 350, 200)

        self.label_result = QtWidgets.QLabel(self)
        self.label_result.setText('lable result')
        self.label_result.move(100, 100)
        self.label_result.adjustSize()

        self.btn = QtWidgets.QPushButton(self)
        self.btn.move(70, 150)
        self.btn.setText('Нажми на меня')
        self.btn.setFixedWidth(200)
        self.btn.clicked.connect(self.dialog)

    # всплывающее окно
    def dialog(self):
        error = QMessageBox()
        error.setWindowTitle('Error')
        error.setText('Сейчас это действие выполнить нельзя')
        error.setIcon(QMessageBox.Warning)
        error.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel | QMessageBox.Reset)

        error.setDefaultButton(QMessageBox.Cancel)

        error.setInformativeText('Два раза действие не выполнить')

        error.setDetailedText('Детали')

        error.buttonClicked.connect(self.dialog_action)

        error.exec_()

    def dialog_action(self, btn):
        if btn.text() == 'OK':
            print('Print OK')
        elif btn.text() == 'Reset':
            self.label_result.setText('')


def application():
    # передаем настройки компа, на котором запуск происходит
    app = QApplication(sys.argv)
    window = Window()

    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    application()