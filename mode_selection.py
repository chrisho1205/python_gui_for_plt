from PyQt5 import QtCore, QtGui, QtWidgets
from example2 import Ui_MainWindow
class Modeselection(QtWidgets.QDialog):
    def __init__(self):
        super().__init__(self.parent)
        self.setupUi(self)
        self.main_window= Ui_MainWindow
        self.main_window.pushButton.clicked.connect(self.next_page)
    def next_page(self):
        print("123")