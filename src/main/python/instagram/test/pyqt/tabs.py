import sys

from PyQt5 import QtWidgets, QtCore, QtGui


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.factors_tab = FactorsTab()
        # self.table_tab = TableTab()
        self.box = QtWidgets.QVBoxLayout()
        self.tabs = QtWidgets.QTabWidget()
        self.tabs.addTab(self.factors_tab, "Factors")
        # self.tabs.addTab(self.table_tab, "Table of coding factors")
        self.setCentralWidget(self.tabs)
        self.tabs.setElideMode(QtCore.Qt.ElideLeft)
        self.tabs.setCurrentIndex(0)
        self.tabs.setUsesScrollButtons(True)
        self.tabs.setLayout(self.box)
        # self.add_menu()


class FactorsTab(QtWidgets.QTableView):
    def __init__(self):
        QtWidgets.QTableView.__init__(self, parent=None)
        self.label = QtWidgets.QLabel("Select folder, project file name")
        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addWidget(self.label)
        self.frame_factors = QtWidgets.QTableView()
        self.table = QtGui.QStandardItemModel(0, 2)
        self.lst1 = ['Дискета', 'Бумага для принтера', 'Барабан для принтера']
        self.lst2 = ["10", "3", "10452048"]
        for row in range(0, 3):
            item1 = QtGui.QStandardItem(self.lst1[row])
            item2 = QtGui.QStandardItem(self.lst2[row])
            self.table.appendRow([item1, item2])
        self.table.setHorizontalHeaderLabels(['Factor Name', 'Кол-во'])
        self.frame_factors.setModel(self.table)
        self.vbox.addWidget(self.frame_factors)
        self.setLayout(self.vbox)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    main = MainWindow()
    main.show()

    sys.exit(app.exec_())