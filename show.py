from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QPainter, QColor, QPen
import sys, example,mainwindow,signup,userpage
import  threading,cv2

from userpage import  ExampleWindow
from PyQt5.QtCore import QLibraryInfo
print(QLibraryInfo.location(QLibraryInfo.PluginsPath))

class myMainWindow_login(QMainWindow,mainwindow.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        #self.pushButton.clicked.connect(self.add)
        self.ocv = True
        self.square_pos = None
        
        
        self.pushButton.clicked.connect(self.show_dialog)
        self.pushButton_2.clicked.connect(self.show_example_window)
    def show_example_window(self):
        # 創建並顯示 Exa mpleWindow
        self.example_window = ExampleWindow()
        video = threading.Thread(target=self.example_window.opencv)
        video.start()
        self.example_window.show()
    def show_dialog(self):
        # 創建並顯示對話框
        self.dialog = myMainWindow_sign()
        self.dialog.exec_()  # 使用 exec_() 讓對話框以模態顯示
class myMainWindow_sign(QDialog,signup.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        #self.pushButton.clicked.connect(self.add)
        
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    """window = myMainWindow()
    video = threading.Thread(target=window.opencv)
    video.start()
    window.show()
    """
    login_page=myMainWindow_login()
    login_page.show()
    sys.exit(app.exec_())