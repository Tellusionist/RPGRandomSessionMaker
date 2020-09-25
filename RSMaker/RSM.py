import sys
from random import randint

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox, QMainWindow

from QTemplates import RSM_Main, Chamber
from ui import QtSetup


class MainWindow(QMainWindow, RSM_Main.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        QtSetup.generic_setup(self)

        # unique buttons for this window
        self.btn_gen_chamber.clicked.connect(self.new_chamber)
        self.btn_pull_chamber.clicked.connect(self.pull_chamber)

        # initialize list for other dialoge windows
        self.chambers = list()
        self.passages = list()

    # custom functions for this window
    def new_chamber(self):
        chamber = ChamberWindow(self)
        self.chambers.append(chamber)
        chamber.show()

    def pull_chamber(self):
        chamber = self.chambers[0]
        chamber.show()


class ChamberWindow(QMainWindow, Chamber.Ui_MainWindow):
    def __init__(self, parent=None):
        super(ChamberWindow, self).__init__(parent)
        self.setupUi(self)
        QtSetup.generic_setup(self)

if __name__ == "__main__":  
    # load Ui
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())