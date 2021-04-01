from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication
import sys


class Second(QMainWindow):
    def __init__(self):
        super(Second, self).__init__()


class First(QMainWindow):
    def __init__(self, parent=None):
        super(First, self).__init__(parent)
        self.pushButton = QPushButton("click me")

        self.setCentralWidget(self.pushButton)

        self.pushButton.clicked.connect(self.ok)

    def ok(self):
        # self.window = QtWidgets.QMainWindow()
        self.window = Second()
        self.window.show()


def main():
    app = QApplication(sys.argv)
    main = First()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()