# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled2.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1920, 1075)
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(10, 120, 751, 511))
        self.groupBox.setObjectName("groupBox")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.groupBox)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(660, 420, 77, 71))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_2.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout_2.addWidget(self.pushButton_2)
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.groupBox)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 20, 661, 471))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label.setEnabled(False)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.groupBox_2 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_2.setGeometry(QtCore.QRect(0, 640, 761, 241))
        self.groupBox_2.setObjectName("groupBox_2")
        self.graphicsView = QtWidgets.QGraphicsView(self.groupBox_2)
        self.graphicsView.setGeometry(QtCore.QRect(10, 20, 740, 180))
        self.graphicsView.setViewportUpdateMode(QtWidgets.QGraphicsView.NoViewportUpdate)
        self.graphicsView.setObjectName("graphicsView")
        self.pushButton_3 = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_3.setGeometry(QtCore.QRect(70, 210, 75, 23))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_4.setGeometry(QtCore.QRect(650, 210, 75, 23))
        self.pushButton_4.setObjectName("pushButton_4")
        self.groupBox_3 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 10, 531, 91))
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.groupBox_3)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(240, 10, 271, 81))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_5 = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_3.addWidget(self.label_5)
        self.label_6 = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_3.addWidget(self.label_6)
        self.label_4 = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_3.addWidget(self.label_4)
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(self.groupBox_3)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(0, 19, 171, 71))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_4.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_4.addWidget(self.label_3)
        self.groupBox_4 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_4.setGeometry(QtCore.QRect(780, 40, 321, 91))
        self.groupBox_4.setObjectName("groupBox_4")
        self.comboBox = QtWidgets.QComboBox(self.groupBox_4)
        self.comboBox.setGeometry(QtCore.QRect(20, 30, 181, 22))
        self.comboBox.setEditable(True)
        self.comboBox.setObjectName("comboBox")
        self.groupBox_5 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_5.setGeometry(QtCore.QRect(770, 570, 381, 321))
        self.groupBox_5.setObjectName("groupBox_5")
        self.gridLayoutWidget = QtWidgets.QWidget(self.groupBox_5)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(30, 130, 320, 171))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_8 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_8.setObjectName("pushButton_8")
        self.gridLayout.addWidget(self.pushButton_8, 0, 1, 1, 1)
        self.pushButton_7 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_7.setObjectName("pushButton_7")
        self.gridLayout.addWidget(self.pushButton_7, 2, 0, 1, 1)
        self.pushButton_26 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_26.setObjectName("pushButton_26")
        self.gridLayout.addWidget(self.pushButton_26, 3, 2, 1, 1)
        self.pushButton_14 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_14.setObjectName("pushButton_14")
        self.gridLayout.addWidget(self.pushButton_14, 3, 1, 1, 1)
        self.pushButton_15 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_15.setObjectName("pushButton_15")
        self.gridLayout.addWidget(self.pushButton_15, 3, 0, 1, 1)
        self.pushButton_13 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_13.setObjectName("pushButton_13")
        self.gridLayout.addWidget(self.pushButton_13, 0, 2, 1, 1)
        self.pushButton_24 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_24.setObjectName("pushButton_24")
        self.gridLayout.addWidget(self.pushButton_24, 1, 2, 1, 1)
        self.pushButton_25 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_25.setObjectName("pushButton_25")
        self.gridLayout.addWidget(self.pushButton_25, 2, 2, 1, 1)
        self.pushButton_10 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_10.setObjectName("pushButton_10")
        self.gridLayout.addWidget(self.pushButton_10, 0, 0, 1, 1)
        self.pushButton_9 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_9.setObjectName("pushButton_9")
        self.gridLayout.addWidget(self.pushButton_9, 1, 1, 1, 1)
        self.pushButton_11 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_11.setObjectName("pushButton_11")
        self.gridLayout.addWidget(self.pushButton_11, 2, 1, 1, 1)
        self.pushButton_12 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_12.setObjectName("pushButton_12")
        self.gridLayout.addWidget(self.pushButton_12, 1, 0, 1, 1)
        self.pushButton_5 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_5.setObjectName("pushButton_5")
        self.gridLayout.addWidget(self.pushButton_5, 2, 3, 1, 1)
        self.pushButton_6 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_6.setObjectName("pushButton_6")
        self.gridLayout.addWidget(self.pushButton_6, 1, 3, 1, 1)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.groupBox_5)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(30, 23, 321, 101))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_8 = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_2.addWidget(self.label_8)
        self.label_12 = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.label_12.setTextFormat(QtCore.Qt.AutoText)
        self.label_12.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_2.addWidget(self.label_12)
        self.label_7 = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_2.addWidget(self.label_7)
        self.label_13 = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.label_13.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_2.addWidget(self.label_13)
        self.groupBox_6 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_6.setGeometry(QtCore.QRect(770, 150, 381, 291))
        self.groupBox_6.setObjectName("groupBox_6")
        self.pushButton_16 = QtWidgets.QPushButton(self.groupBox_6)
        self.pushButton_16.setGeometry(QtCore.QRect(30, 190, 101, 41))
        font = QtGui.QFont()
        font.setFamily("Neo Sans")
        font.setPointSize(15)
        self.pushButton_16.setFont(font)
        self.pushButton_16.setObjectName("pushButton_16")
        self.pushButton_17 = QtWidgets.QPushButton(self.groupBox_6)
        self.pushButton_17.setGeometry(QtCore.QRect(250, 190, 101, 41))
        font = QtGui.QFont()
        font.setFamily("Neo Sans")
        font.setPointSize(15)
        self.pushButton_17.setFont(font)
        self.pushButton_17.setObjectName("pushButton_17")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.groupBox_6)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 40, 351, 80))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_9 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_9.setObjectName("label_9")
        self.verticalLayout.addWidget(self.label_9)
        self.label_10 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_10.setObjectName("label_10")
        self.verticalLayout.addWidget(self.label_10)
        self.groupBox_7 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_7.setGeometry(QtCore.QRect(1160, 20, 671, 541))
        self.groupBox_7.setObjectName("groupBox_7")
        self.comboBox_3 = QtWidgets.QComboBox(self.groupBox_7)
        self.comboBox_3.setGeometry(QtCore.QRect(40, 30, 69, 22))
        self.comboBox_3.setObjectName("comboBox_3")
        self.comboBox_4 = QtWidgets.QComboBox(self.groupBox_7)
        self.comboBox_4.setGeometry(QtCore.QRect(150, 30, 69, 22))
        self.comboBox_4.setObjectName("comboBox_4")
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(self.groupBox_7)
        self.doubleSpinBox.setGeometry(QtCore.QRect(40, 90, 201, 22))
        self.doubleSpinBox.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.doubleSpinBox.setSingleStep(0.1)
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.pushButton_23 = QtWidgets.QPushButton(self.groupBox_7)
        self.pushButton_23.setGeometry(QtCore.QRect(390, 90, 75, 23))
        self.pushButton_23.setObjectName("pushButton_23")
        self.tableView = QtWidgets.QTableView(self.groupBox_7)
        self.tableView.setGeometry(QtCore.QRect(20, 140, 631, 331))
        self.tableView.setObjectName("tableView")
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(self.groupBox_7)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(20, 480, 631, 61))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pushButton_18 = QtWidgets.QPushButton(self.horizontalLayoutWidget_3)
        self.pushButton_18.setObjectName("pushButton_18")
        self.horizontalLayout_3.addWidget(self.pushButton_18)
        self.pushButton_19 = QtWidgets.QPushButton(self.horizontalLayoutWidget_3)
        self.pushButton_19.setObjectName("pushButton_19")
        self.horizontalLayout_3.addWidget(self.pushButton_19)
        self.pushButton_20 = QtWidgets.QPushButton(self.horizontalLayoutWidget_3)
        self.pushButton_20.setObjectName("pushButton_20")
        self.horizontalLayout_3.addWidget(self.pushButton_20)
        self.groupBox_8 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_8.setGeometry(QtCore.QRect(1160, 570, 671, 321))
        self.groupBox_8.setObjectName("groupBox_8")
        self.comboBox_2 = QtWidgets.QComboBox(self.groupBox_8)
        self.comboBox_2.setGeometry(QtCore.QRect(30, 50, 591, 22))
        self.comboBox_2.setObjectName("comboBox_2")
        self.groupBox_9 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_9.setGeometry(QtCore.QRect(770, 440, 381, 121))
        self.groupBox_9.setObjectName("groupBox_9")
        self.pushButton_21 = QtWidgets.QPushButton(self.groupBox_9)
        self.pushButton_21.setGeometry(QtCore.QRect(30, 60, 101, 41))
        font = QtGui.QFont()
        font.setFamily("Neo Sans")
        font.setPointSize(15)
        self.pushButton_21.setFont(font)
        self.pushButton_21.setObjectName("pushButton_21")
        self.pushButton_22 = QtWidgets.QPushButton(self.groupBox_9)
        self.pushButton_22.setGeometry(QtCore.QRect(250, 60, 101, 41))
        font = QtGui.QFont()
        font.setFamily("Neo Sans")
        font.setPointSize(15)
        self.pushButton_22.setFont(font)
        self.pushButton_22.setObjectName("pushButton_22")
        self.label_11 = QtWidgets.QLabel(self.groupBox_9)
        self.label_11.setGeometry(QtCore.QRect(130, 10, 171, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.groupBox.setTitle(_translate("Dialog", "GroupBox"))
        self.pushButton.setText(_translate("Dialog", "+"))
        self.pushButton_2.setText(_translate("Dialog", "-"))
        self.label.setText(_translate("Dialog", "image"))
        self.groupBox_2.setTitle(_translate("Dialog", "GroupBox"))
        self.pushButton_3.setText(_translate("Dialog", "store_data"))
        self.pushButton_4.setText(_translate("Dialog", "clear"))
        self.groupBox_3.setTitle(_translate("Dialog", "GroupBox"))
        self.label_5.setText(_translate("Dialog", "distance_near"))
        self.label_6.setText(_translate("Dialog", "now_distance"))
        self.label_4.setText(_translate("Dialog", "distance_far"))
        self.label_2.setText(_translate("Dialog", "name"))
        self.label_3.setText(_translate("Dialog", "time"))
        self.groupBox_4.setTitle(_translate("Dialog", "GroupBox"))
        self.comboBox.setCurrentText(_translate("Dialog", "Auto Speed"))
        self.groupBox_5.setTitle(_translate("Dialog", "GroupBox"))
        self.pushButton_8.setText(_translate("Dialog", "8"))
        self.pushButton_7.setText(_translate("Dialog", "1"))
        self.pushButton_26.setText(_translate("Dialog", "enter"))
        self.pushButton_14.setText(_translate("Dialog", "0"))
        self.pushButton_15.setText(_translate("Dialog", "."))
        self.pushButton_13.setText(_translate("Dialog", "9"))
        self.pushButton_24.setText(_translate("Dialog", "6"))
        self.pushButton_25.setText(_translate("Dialog", "3"))
        self.pushButton_10.setText(_translate("Dialog", "7"))
        self.pushButton_9.setText(_translate("Dialog", "5"))
        self.pushButton_11.setText(_translate("Dialog", "2"))
        self.pushButton_12.setText(_translate("Dialog", "4"))
        self.pushButton_5.setText(_translate("Dialog", "Down"))
        self.pushButton_6.setText(_translate("Dialog", "Up"))
        self.label_8.setText(_translate("Dialog", "0.0"))
        self.label_12.setText(_translate("Dialog", "km/h"))
        self.label_7.setText(_translate("Dialog", "0.0"))
        self.label_13.setText(_translate("Dialog", "%"))
        self.groupBox_6.setTitle(_translate("Dialog", "GroupBox"))
        self.pushButton_16.setText(_translate("Dialog", "Start"))
        self.pushButton_17.setText(_translate("Dialog", "Cancel"))
        self.label_9.setText(_translate("Dialog", "The Near Side Distance:"))
        self.label_10.setText(_translate("Dialog", "The Far Side Distance:"))
        self.groupBox_7.setTitle(_translate("Dialog", "GroupBox"))
        self.pushButton_23.setText(_translate("Dialog", "Add"))
        self.pushButton_18.setText(_translate("Dialog", "Store_data"))
        self.pushButton_19.setText(_translate("Dialog", "Export"))
        self.pushButton_20.setText(_translate("Dialog", "Delete"))
        self.groupBox_8.setTitle(_translate("Dialog", "GroupBox"))
        self.groupBox_9.setTitle(_translate("Dialog", "GroupBox"))
        self.pushButton_21.setText(_translate("Dialog", "Start"))
        self.pushButton_22.setText(_translate("Dialog", "Pause"))
        self.label_11.setText(_translate("Dialog", "00:00:00"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
