from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QPainter, QColor, QPen, QStandardItemModel, QStandardItem
import sys, example,mainwindow,signup
import   threading,cv2
import example  
#from pyqt_switch import PyQtSwitch
import pyrealsense2 as rs
import numpy as np
import mediapipe as mp
import math
import matplotlib 
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as  plt
import time
import serial
from scipy.signal import argrelextrema
import traceback
class LabelEventFilter(QObject):
    def __init__(self,main_window,parent=None):
        super().__init__(parent)
        self.main_window = main_window
        
    def eventFilter(self, obj, event):
        if event.type() == event.MouseButtonPress:  # 捕获鼠标点击事件
            if event.button() == Qt.LeftButton:  # 判断是否为左键点击
                self.main_window.manual_position=0
                #if hasattr(self.main_window, "pushButton_16"):
                self.main_window.pushButton_16.setText("Comfirm")  # 修改按钮文本
                #self.main_window.pushButton_16.setText("Comfirm")  # 修改按钮文本
                self.main_window.label_10.setStyleSheet("color: black;font-size: 24px;") 
                self.main_window.label_9.setStyleSheet("color: red;font-size: 24px;") 
                print("check")
                
            return True
        return super().eventFilter(obj, event)
class LabelEventFilter2(QObject):
    def __init__(self,main_window,parent=None):
        super().__init__(parent)
        self.main_window = main_window
        
    def eventFilter(self, obj, event):
        if event.type() == event.MouseButtonPress:  # 捕获鼠标点击事件
            if event.button() == Qt.LeftButton:  # 判断是否为左键点击
                self.main_window.manual_position=1
                #if hasattr(self.main_window, "pushButton_16"):
                self.main_window.pushButton_16.setText("Comfirm")  # 修改按钮文本
                #self.main_window.pushButton_16.setText("Comfirm")  # 修改按钮文本
                self.main_window.label_9.setStyleSheet("color: black;font-size: 24px;") 
                self.main_window.label_10.setStyleSheet("color: red;font-size: 24px;") 
                print("check")
                
            return True
        return super().eventFilter(obj, event)
class LabelEventFilter_speed(QObject):
    def __init__(self,main_window,parent=None):
        super().__init__(parent)
        self.main_window = main_window
        
    def eventFilter(self, obj, event):
        if event.type() == event.MouseButtonPress:  # 捕获鼠标点击事件
            if event.button() == Qt.LeftButton:  # 判断是否为左键点击
                self.main_window.first_speed=0
                self.main_window.manual_speed=True
                #if hasattr(self.main_window, "pushButton_16"):
                self.main_window.label_8.setStyleSheet("color: red;font-size: 72px;") 
                self.main_window.label_7.setStyleSheet("color: black;font-size: 72px;") 
                print("check")
                
            return True
        return super().eventFilter(obj, event)
class LabelEventFilter_slope(QObject):
    def __init__(self,main_window,parent=None):
        super().__init__(parent)
        self.main_window = main_window
        
    def eventFilter(self, obj, event):
        if event.type() == event.MouseButtonPress:  # 捕获鼠标点击事件
            if event.button() == Qt.LeftButton:  # 判断是否为左键点击
                self.main_window.manual_speed=False
                self.main_window.first_speed=0
                #if hasattr(self.main_window, "pushButton_16"):
                self.main_window.label_7.setStyleSheet("color: red;font-size: 72px;") 
                self.main_window.label_8.setStyleSheet("color: black;font-size: 72px;") 
                print("check")
                
            return True
        return super().eventFilter(obj, event)

class MyLabel(QLabel):  # 自定义 QLabel 类
    def __init__(self, parent=None):
        super().__init__(parent)
        self.square_pos = None  # 存储点击位置，默认为 None
        self.pixmap = QPixmap()  # 存储图像
        self.check_image = True 
        self.ROI_width=50
        self.countdown_value = None
        self.Footcount_value=None
        self.status=0
        self.roi_depth=0
        self.x=320
        self.y=240
        self.user_status="safe"
       
        
    def image_status(self):
        #self.origin_user_status=self.user_status
        if self.user_status=="far":
            return -2
        elif self.user_status=="danger":
            return -1
        elif self.user_status=="near":
            return 1
        else:
            return 0


    def setImage(self, image: QImage):
        """设置图像并更新 QLabel"""
        self.pixmap = QPixmap.fromImage(image)
        #self.update()  # 请求重绘
    def setCountdown(self, value: int):
        """设置倒计时的值"""
        self.countdown_value = value
        self.update()  # 请求重绘
    def setFootstep(self, value,status):
        """设置倒计时的值"""
        self.countdown_value = value
        self.status=status
        self.update()  # 请求重绘

    def mousePressEvent(self, event):
        """处理鼠标点击事件"""
        if event.button() == Qt.LeftButton:  # 判断是否是左键点击
            self.square_pos = event.pos()  # 记录鼠标点击位置
            self.update()  # 请求重绘
            
            self.check_image = False

    def paintEvent(self, event):
        """绘制图像和正方形"""
        super().paintEvent(event)  # 保证 QLabel 的默认绘制
        
        if self.check_image:
            # 绘制图像
            #print("image")
            painter = QPainter(self)
            painter.drawPixmap(0, 0, self.pixmap)  # 绘制图
            roi_depth = self.roi_depth 
            self.parent().label_6.setText(f"{roi_depth*100:.1f} cm")
            
            # 默认绘制正方形，位于 (320, 240) 位置（中心）
            if roi_depth < (float(self.parent().z_near_value)/100):  # 比较单位保持一致
                self.user_status="near"
                pen = QPen(Qt.red, 5)  # 如果过近，显示红色
            elif roi_depth > (float(self.parent().z_far_value)/100) :
                self.user_status="far"
                pen = QPen(Qt.red, 5)  # 如果过远，
            elif roi_depth > ((float(self.parent().z_far_value)-((float(self.parent().z_far_value)-float(self.parent().z_near_value))*0.3))/100):
                self.user_status="danger"
                pen = QPen(Qt.yellow, 5)  # 如果过远，显示蓝色
            else:
                self.user_status="safe"
                pen = QPen(Qt.green, 5)  # 如果在范围内，显示绿色
            painter.setPen(pen)
            # 绘制 50x50 的正方形，中心位置为 (320, 240)
            painter.drawRect(int(320-self.ROI_width/2) ,int( 240-self.ROI_width/2) , self.ROI_width, self.ROI_width)  # 使正方形位于中心
        if self.countdown_value is not None:
            painter3 = QPainter(self)
            painter3.setPen(QPen(Qt.red))
            font = QFont()
            font.setPointSize(48)
            #font.setBold(True)
            painter3.setFont(font)
            if self.status==2:
                painter3.drawText(self.width() - 500, 40, f"{self.countdown_value:.3f}")  # 在右上角显示倒计时数字   
            if self.status==1:
                painter3.drawText(self.width() - 200, 40, f"{self.countdown_value:.3f}")  # 在右上角显示倒计时数字   

        # 绘制正方形（如果有点击的位置）
        if self.square_pos:
            painter2 = QPainter(self)
            roi_depth = self.roi_depth 
            self.parent().label_6.setText(f"{roi_depth*100:.1f} cm")
           
            painter2.drawPixmap(0, 0, self.pixmap)  # 绘制图
            if roi_depth < (float(self.parent().z_near_value)/100):  # 比较单位保持一致
                self.user_status="near"
                pen = QPen(Qt.red, 5)  # 如果过近，显示红色
            elif roi_depth > (float(self.parent().z_far_value)/100) :
                self.user_status="far"
                pen = QPen(Qt.red, 5)  # 如果过远，
            elif roi_depth > ((float(self.parent().z_far_value)-((float(self.parent().z_far_value)-float(self.parent().z_near_value))*0.3))/100):
                self.user_status="danger"
                pen = QPen(Qt.yellow, 5)  # 如果过远，显示蓝色
            else:
                self.user_status="safe"
                pen = QPen(Qt.green, 5)  # 如果在范围内，显示绿色
            painter2.setPen(pen)
            # 绘制 10x10 的方形
            #print("color2")
            self.x=self.square_pos.x()
            self.y=self.square_pos.y()
            painter2.drawRect(int(self.square_pos.x()-self.ROI_width/2), int(self.square_pos.y()-self.ROI_width/2),self.ROI_width,self.ROI_width)
        else:
            if (self.check_image)==False:
                roi_depth = self.roi_depth 
                self.parent().label_6.setText(f"{roi_depth*100:.1f} cm")
                painter2 = QPainter(self)
                painter2.drawPixmap(0, 0, self.pixmap)  # 绘制图
                if roi_depth < (float(self.parent().z_near_value)/100):  # 比较单位保持一致
                    self.user_status="near"
                    pen = QPen(Qt.red, 5)  # 如果过近，显示红色
                elif roi_depth > (float(self.parent().z_far_value)/100) :
                    self.user_status="far"
                    pen = QPen(Qt.red, 5)  # 如果过远，
                elif roi_depth > ((float(self.parent().z_far_value)-((float(self.parent().z_far_value)-float(self.parent().z_near_value))*0.3))/100):
                    self.user_status="danger"
                    pen = QPen(Qt.yellow, 5)  # 如果过远，显示蓝色
                else:
                    self.user_status="safe"
                    pen = QPen(Qt.green, 5)  # 如果在范围内，显示绿色
                painter.setPen(pen)
                # 绘制 10x10 的方形
                painter2.drawRect(int(self.x-self.ROI_width/2), int(self.y-self.ROI_width/2),self.ROI_width,self.ROI_width)
            
        

            
    def increase_roi(self):
        self.ROI_width+=10
        self.update()  # 请求重绘
    def decrease_roi(self):
        self.ROI_width-=10
        self.update()  # 请求重绘
    def calculate_roi(self, depth_image):
        h, w = 480,640
        
        if self.square_pos is None:  # 如果沒有鼠標點擊，使用默認中心位置
            x, y = w // 2, h // 2
        else:
            x, y = self.square_pos.x(), self.square_pos.y()  # 使用鼠標點擊的位置

        # 計算 ROI 範圍
        roi_x = max(int(x - self.ROI_width / 2.0), 0)
        roi_y = max(int(y - self.ROI_width / 2.0), 0)
        roi_x2 = min(roi_x + self.ROI_width, w)
        roi_y2 = min(roi_y + self.ROI_width, h)
        #print(roi_x,roi_x2,roi_y,roi_y2)
        # 計算 ROI 中的平均深度值
        depth_roi_sum = 0
        depth_roi_count = 0

        for y_ in range(roi_y, roi_y2):
            for x_ in range(roi_x, roi_x2):
                z_value =  depth_image.get_distance(x_, y_)
                if z_value:
                    depth_roi_sum += z_value
                    depth_roi_count += 1
        #print(depth_roi_sum)
        if depth_roi_count > 0:
            avg_depth = depth_roi_sum / depth_roi_count
        else:
            avg_depth = 0  # 如果 ROI 中沒有有效的深度數據，設為 0
        self.roi_depth=avg_depth
        return avg_depth
    def calculate_roi_mediapipe(self, depth_image,x,y):
        h, w = 480,640
        ROI_width=20
        # 計算 ROI 範圍
        roi_x = max(int(x -ROI_width / 2.0), 0)
        roi_y = max(int(y - ROI_width / 2.0), 0)
        roi_x2 = min(roi_x +ROI_width, w)
        roi_y2 = min(roi_y + ROI_width, h)
        #print(roi_x,roi_x2,roi_y,roi_y2)
        # 計算 ROI 中的平均深度值
        depth_roi_sum = 0
        depth_roi_count = 0

        for y_ in range(roi_y, roi_y2):
            for x_ in range(roi_x, roi_x2):
                z_value =  depth_image.get_distance(x_, y_)
                if z_value:
                    depth_roi_sum += z_value
                    depth_roi_count += 1
        #print(depth_roi_sum)
        if depth_roi_count > 0:
            #avg_depth = depth_roi_sum / depth_roi_count
            avg_depth = depth_image.get_distance(x, y)
        else:
            avg_depth = 0  # 如果 ROI 中沒有有效的深度數據，設為 0
        self.roi_depth=avg_depth
        
        return avg_depth
    
    def calculate_roi_mediapipe_calibrate(self,depth_image,x,y):
        h, w = 480,640
        ROI_width=6
        x_calibrate=((x-321.1242370605469)*depth_image.get_distance(x, y))/610.4790649414062
        y_calibrate=((y-246.25962829589844)*depth_image.get_distance(x, y))/610.4264526367188
        #print(x)
        roi_x = max(int(x -ROI_width / 2.0), 0)
        roi_y = max(int(y - ROI_width / 2.0), 0)
        roi_x2 = min(roi_x +ROI_width, w)
        roi_y2 = min(roi_y + ROI_width, h)
        #x_calibrate=(x-320)/100
        #y_calibrate=(y-240)/100
        #print(x_calibrate)
        #print("x")
        #print(x_calibrate)
        #print(depth_image.get_distance(x, y))
        depth_roi_sum = 0
        depth_roi_count = 0

        for y_ in range(roi_y, roi_y2):
            for x_ in range(roi_x, roi_x2):
                z_value =  depth_image.get_distance(x_, y_)
                if z_value>0:
                    depth_roi_sum += z_value
                    depth_roi_count += 1
        #print(depth_roi_sum)
        if depth_roi_count > 0:
            avg_depth = depth_roi_sum / depth_roi_count
            #avg_depth = depth_image.get_distance(x, y)
        else:
            avg_depth = 0  # 如果 ROI 中沒有有效的深度數據，設為 0
        roi_depth=avg_depth

        avg_depth= math.sqrt(roi_depth**2-((x_calibrate)**2+(y_calibrate)**2))
        #avg_depth= math.sqrt((depth_image.get_distance(x, y)**2)-(((x-320)**2)+((y-240)**2)))
        #print(avg_depth)
        return x_calibrate,y_calibrate,avg_depth
    

class ExampleWindow(QDialog, example.Ui_Dialog):
    def __init__(self):
        super().__init__()
        
        self.setupUi(self)
        self.label =  MyLabel(self)  # 假設要顯示影像的 QLabel
        self.label.setGeometry(10, 130, 640, 480)  # 設置 QLabel 的大小和位置
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 740, 200) 
        self.graphicsView.setScene(self.scene)
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        #self.setFixedSize(500, 400)

        # Draw axes
        
        #self.draw_x_axis_time_labels()
        
        #self.draw_y_axis_float_labels()
        #self.draw_grid()
        #self.draw_line(50)
        self.graphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ocv = False  # 控制 opencv 類型的變數
        self.comboBox.addItem("Auto Speed")
        self.comboBox.addItem("Fixed Speed")
        self.comboBox.addItem("Customize")
        self.comboBox_2.addItem("None")
        self.comboBox_2.addItem("Drop_Foot")#32 28 26
        self.comboBox_2.addItem("Toe")#32 30 34 (34 new dot with 26x 32y 32z)
        self.comboBox_2.addItem("Foot_step")# 12 24 26
        self.comboBox_2.addItem("body_step")#12 11 23 24
        self.comboBox_2.addItem("Under_Pronation")# 26 28 30 25 27 29
        self.pushButton.clicked.connect(self.add)
        self.pushButton_2.clicked.connect(self.minus)
        """
        switch = PyQtSwitch()
        switch.toggled.connect(self.__toggled)
        switch.setAnimation(True)
        self.__label = QLabel()
        self.__label.setText('Speed')
        lay = QFormLayout()
        lay.addRow(self.__label, switch)
        self.setLayout(lay)
        self.groupBox_5.setLayout(lay)
        
        switch2 = PyQtSwitch()
        switch2.toggled.connect(self.__toggled2)
        switch2.setAnimation(True)
        self.__label2 = QLabel()
        self.__label2.setText('Auto')
        lay2 = QFormLayout()
        lay2.addRow(self.__label2, switch2)
        self.setLayout(lay2)
        self.groupBox_6.setLayout(lay2)
        """ 
        self.count=10
        self.depth_items = []
        self.model=QStandardItemModel(1,4)
        self.model.setHorizontalHeaderLabels(["Time","Speed","Slope","Delete"])
        self.tableView.setModel(self.model)
        self.row_table=0
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        

        # 绘制图表线条
        
        self.pushButton_16.clicked.connect(self.adjust_position)
        self.pushButton_16.setText("Start")
        self.pushButton_17.clicked.connect(self.cancel_adjust_position)
        self.pushButton_17.setText("Cancel")
        self.pushButton_15.clicked.connect(self.on_button_clicked)
        self.pushButton_15.setText("clear")
        self.pushButton_14.clicked.connect(self.on_button_clicked)
        self.pushButton_26.clicked.connect(self.on_button_clicked)
        self.pushButton_7.clicked.connect(self.on_button_clicked)
        self.pushButton_10.clicked.connect(self.on_button_clicked)
        self.pushButton_12.clicked.connect(self.on_button_clicked)
        self.pushButton_8.clicked.connect(self.on_button_clicked)
        self.pushButton_9.clicked.connect(self.on_button_clicked)
        self.pushButton_11.clicked.connect(self.on_button_clicked)
        self.pushButton_13.clicked.connect(self.on_button_clicked)
        self.pushButton_24.clicked.connect(self.on_button_clicked)
        self.pushButton_25.clicked.connect(self.on_button_clicked)
        self.pushButton_6.clicked.connect(self.increase_speed)
        self.pushButton_5.clicked.connect(self.decrease_speed)
        self.pushButton_21.clicked.connect(self.start_train)
        self.pushButton_22.clicked.connect(self.pause_timer)
        self.pushButton_23.clicked.connect(self.add_table_value)
        self.pushButton_20.clicked.connect(self.delete_checked_rows)
        self.pushButton_19.clicked.connect(self.export_customize_data)
        self.filter_label_9 = LabelEventFilter(self)
        self.label_9.installEventFilter(self.filter_label_9)
        self.filter_label_10 = LabelEventFilter2(self)
        self.label_10.installEventFilter(self.filter_label_10)
        self.filter_label_8 = LabelEventFilter_speed(self)
        self.label_8.installEventFilter( self.filter_label_8)
        self.filter_label_7 = LabelEventFilter_slope(self)
        self.label_7.installEventFilter(self.filter_label_7)


        self.comboBox_3.addItems([str(i) for i in range(60)])
        self.comboBox_4.addItems([str(i) for i in range(60)])
        self.selected_text = self.comboBox.itemText(0)
        self.comboBox.currentIndexChanged.connect(self.on_selection)  # 綁定事件
        self.selected_text_mediapipe = self.comboBox_2.itemText(0)
        self.comboBox_2.currentIndexChanged.connect(self.on_selection_mediapipe)  # 綁定事件
        
        
        
        
        self.mediapipe=False
        self.adjust_position_function =True
        self.label_7.setText("0.0")
        self.label_7.setStyleSheet("font-size: 72px;") 
        self.label_7.setAlignment(Qt.AlignBottom)
        self.label_8.setText("0.0")
        self.label_8.setStyleSheet("font-size: 72px;") 
        self.label_8.setAlignment(Qt.AlignBottom)
        self.z_near_value=160
        self.z_far_value=300
        self.first_speed=0
        self.second_speed=0
        self.input_speed=False
        self.countdown_timer_training = QTimer(self)
        self.is_paused = False
        self_speed=0.0
        self.current_offset =0
        self.start_time = QTime(0, 0)
        self.draw_y_axis(self.z_near_value,self.z_far_value)
        self.draw_x_axis()
        self.update_x_axis_check=False
        self.y2=self.z_far_value
        self.y1=self.z_near_value
        self.line_items=[]
        self.trill_speed_command=163
        self.customize_time=[]
        self.customize_speed=[]
        self.customize_slope=[]
        self.customize_count=0
        self.manual_position=0
        self.manual_speed=True
        self.right_x_value_list=[]
        self.right_y_value_list=[]
        self.right_line_degree=[]
        self.right_depth_value_mediapipe_calibrate_list=[]
        self.left_x_value_list=[]
        self.left_y_value_list=[]
        self.left_line_degree=[]
        self.left_depth_value_mediapipe_calibrate_list=[]
        self.left_node_1=0
        self.left_node_2=0
        self.left_node_3=0
        self.right_node_1=0
        self.right_node_2=0
        self.right_node_3=0
        self.foot_step_count=0
        self.foot_step_left=0
        self.gait_record=False
        self.gait_record_finish=False
        self.right_distance_start_left=0
        self.right_distance_start_right=0
        self.right_distance_end_left=0
        self.right_distance_end_right=0
        self.left_distance_start_left=0
        self.left_distance_start_right=0
        self.left_distance_end_left=0
        self.left_distance_end_right=0
        self.count_local_value_left=0
        self.count_local_value_right=0
        self.left_drop_foot_average=[]
        self.foot_step_time_index=0
        self.right_drop_foot_average=[]
        self.left_depth=0
        self.foot_step_time=[]

        
        
        
        self.label_9.setText("The Near Side Distance: "+str(self.z_near_value)+"cm")
        self.label_10.setText("The Far Side Distance: "+str(self.z_far_value)+"cm")
        self.label_9.setStyleSheet("font-size: 24px;") 
        self.label_10.setStyleSheet("font-size: 24px;") 
        #self.draw_line(self.z_near_value,self.z_far_value)  
        
        self.ser = serial.Serial(
        port='/dev/ttyUSB0',        # 串口號，根據實際調整
        baudrate=4800,      # 波特率
        bytesize=serial.EIGHTBITS,  # 數據位
        parity=serial.PARITY_NONE,  # 奇偶校驗
        stopbits=serial.STOPBITS_ONE,  # 停止位
        timeout=10        # 超時設置（秒）
            )
        
        
        
        self.elapsed_time = 0  # 以秒為單位

    
    def draw_x_axis(self):
    # 设置时间格式 (例如: 00:00, 00:10, ...)
        start_time = QTime(0, 0)  # 从 00:00 开始
        time_interval = 10  # 每个刻度时间间隔 (10分钟)

        # 绘制 X 轴
        axis_pen = QPen(QColor(0, 0, 0))  # 黑色线条
        axis_pen.setWidth(2)
        self.scene.addLine(40, 170, 720, 170, axis_pen)  # 画 X 轴线

        # 添加 X 轴的标签（时间）
        for i in range(0, 691, 50):  # 每隔 50 像素显示一个时间刻度
            time_str = start_time.addSecs(i // 50 * time_interval * 60).toString("hh:mm")  # 计算时间并转换为字符串
            print(time_str)
            text_item = QGraphicsTextItem(time_str)
            text_item.setPos(30 + i, 170)  # 设置标签位置
            self.scene.addItem(text_item)
    def update_x_axis(self,near_line,far_line):
        """动态更新 X 轴标签"""
        #max_x = self.axis_width  # X 轴最大宽度

        self.current_offset += 10  

        # 清空現有 X 軸標籤
        for item in self.scene.items():
            if isinstance(item, QGraphicsTextItem) and item not in self.depth_items:
                self.scene.removeItem(item)
        value_far=int(float(far_line))
        value_near=int(float(near_line))
        y2= value_far+20
        y1=value_near-20
        print(y1)
        y_scale=y2-y1
        value_danger=value_far-( value_far-value_near)*0.3
        #3.3
        # 设置 Y 轴标签 (例如: 20.0 到 50.0)
        for i in range(y1, y2+3, int((y2+10-y1)/5)):  # 每 5 增加一次标签
            label = f"{float(i):.1f}"  # 格式化为浮点数，保留一位小数
            text_item = QGraphicsTextItem(label)
            text_item.setPos(5, ((i-y1)/y_scale)*(-150)+160)  # 设置标签位置，乘以 2 来调整比例
            self.scene.addItem(text_item)

        # 绘制 Y 轴
        axis_pen = QPen(QColor(0, 0, 0))  # 黑色线条
        axis_pen.setWidth(2)
        self.scene.addLine(40, 20, 40, 170, axis_pen)  # 画 Y 轴线
        y_pos_far = ((value_far - y1) / y_scale) * (-150) + 167
        y_pos_near = ((value_near - y1) / y_scale) * (-150) + 167
        y_pos_danger = ((value_danger - y1) / y_scale) * (-150) + 167
        line_pen = QPen(QColor(255, 0, 0))  # 红色线条
        line_pen.setWidth(2)
        line_pen_danger = QPen(QColor(255,255, 0))  # 红色线条
        line_pen_danger.setWidth(2)
        self.scene.addLine(40,y_pos_far,720,y_pos_far,line_pen) 
        
        self.scene.addLine(40,y_pos_near,720,y_pos_near,line_pen)  # 绘制线条
        self.scene.addLine(40, y_pos_danger , 720, y_pos_danger , line_pen_danger)  # 绘制线条
        self.scene.update()

        # 重新繪製 X 軸標籤
        for i in range(0, 691, 50):  # 每隔 50 像素
            elapsed_time = self.current_offset + (i // 50 * 10)  # 每刻度 10 秒
            time_str = self.start_time.addSecs(elapsed_time).toString("mm:ss")
            text_item = QGraphicsTextItem(time_str)
            text_item.setPos(40 + i, 170)  # 標籤位置
            self.scene.addItem(text_item)
            self.scene.update()

            # 绘制新的刻度线（可选）
    def clear_all_depth_items(self):
        """清除所有深度值和繪製的線條"""
        # 清空 depth_items（深度值）
        self.depth_items.clear()
        
        # 清除繪製的線條
        for line_item in self.line_items:
            self.scene.removeItem(line_item)
        
        # 清空 line_items 以便繪製新線條
        self.line_items.clear()
        
        # 更新場景
        self.scene.update()
    def draw_training_data(self, current_depth):
        
        # 計算當前點的位置
        x_pos = 40 + int((self.elapsed_time) *5.31)  # X 軸對應時間的座標
        if(current_depth>self.y2):
            current_depth=self.y2+10
        elif(current_depth<self.y1):
            current_depth=self.y1-10
        y_pos = ((current_depth - self.y1) / (self.y2 - self.y1)) * (-150) + 167  # 映射到 Y 軸

        # 如果已有上一個點，繪製線段連接
        if self.depth_items:
            
            last_point = self.depth_items[-1]  # 取得上一個點
            x_last, y_last = last_point
            line_item = QGraphicsLineItem(x_last, y_last, x_pos, y_pos)  # 繪製線
            line_item.setPen(QPen(QColor(0, 0, 255), 2))  # 藍色線條，寬度為2
            self.scene.addItem(line_item)
            self.line_items.append(line_item)

        # 保存當前點
        self.depth_items.append((x_pos, y_pos))

        # 限制最多顯示 70 個點和線
        if len(self.depth_items) > 70:
            old_point = self.depth_items.pop(0)  # 移除最早的點
            old_line = self.line_items.pop(0) if self.line_items else None  # 移除對應的線
            if old_line:
                self.scene.removeItem(old_line)
        self.scene.update()

    def draw_y_axis(self,near_line,far_line):
        self.scene.clear()
        value_far=int(float(far_line))
        value_near=int(float(near_line))
        self.y2= value_far+20
        self.y1=value_near-20
        print(self.y1)
        y_scale=self.y2-self.y1
        value_danger=value_far-(value_far-value_near)*0.3
        #3.3
        # 设置 Y 轴标签 (例如: 20.0 到 50.0)
        for i in range(self.y1, self.y2+3, int((self.y2+10-self.y1)/5)):  # 每 5 增加一次标签
            label = f"{float(i):.1f}"  # 格式化为浮点数，保留一位小数
            text_item = QGraphicsTextItem(label)
            text_item.setPos(5, ((i-self.y1)/y_scale)*(-150)+160)  # 设置标签位置，乘以 2 来调整比例
            self.scene.addItem(text_item)

        # 绘制 Y 轴
        axis_pen = QPen(QColor(0, 0, 0))  # 黑色线条
        axis_pen.setWidth(2)
        self.scene.addLine(40, 20, 40, 170, axis_pen)  # 画 Y 轴线
        y_pos_far = ((value_far - self.y1) / y_scale) * (-150) + 167
        y_pos_near = ((value_near - self.y1) / y_scale) * (-150) + 167
        y_pos_danger = ((value_danger - self.y1) / y_scale) * (-150) + 167
        line_pen = QPen(QColor(255, 0, 0))  # 红色线条
        line_pen.setWidth(2)
        line_pen_danger = QPen(QColor(255,255, 0))  # 红色线条
        line_pen_danger.setWidth(2)
        self.scene.addLine(40,y_pos_far,720,y_pos_far,line_pen) 
        
        self.scene.addLine(40,y_pos_near,720,y_pos_near,line_pen)  # 绘制线条
        self.scene.addLine(40, y_pos_danger , 720, y_pos_danger , line_pen_danger)  # 绘制线条
        self.scene.update()

   

    
    def add(self):
        self.label.increase_roi()
    def minus(self):
        self.label.decrease_roi()
    def closeEvent(self,event):
        self.ocv = False
        self.pipeline.stop()
        cv2.destroyAllWindows()  
        self.ser.close()

        
        sys.exit(0)
    def adjust_position(self):
        self.depth_values = []  # 存储深度值
        if self.pushButton_16.text()=="Start":
    
            
            self.countdown_timer = QTimer(self)
            self.remaining_time = 5  # 每次倒计时的时间
            self.current_round = 1  # 当前是第几次倒计时
            self.adjust_position_function =True

            def update_countdown():
                if self.adjust_position_function==True:
                    if self.remaining_time > 0:
                        print(f"Round {self.current_round}, Time left: {self.remaining_time} seconds")
                        self.label.setCountdown(self.remaining_time)
                        self.remaining_time -= 1
                        if self.current_round==1:
                            self.label_9.setStyleSheet("color: red;font-size: 24px;") 
                        else:
                            self.label_9.setStyleSheet("color: black;font-size: 24px;") 
                            self.label_10.setStyleSheet("color: red;font-size: 24px;") 
                        
                    else:
                        # 倒计时结束，记录当前 label_6 的值
                        
                        depth_value = self.label_6.text()
                        self.depth_values.append(depth_value)
                        if self.current_round==1:
                            self.label_9.setText("The Near Side Distance: "+depth_value)
                            self.z_near_value=depth_value[:len(depth_value)-2]
                        else:
                            self.label_10.setText("The Far Side Distance: "+depth_value)
                            self.z_far_value=depth_value[:len(depth_value)-2]
                            
                            
                        print(f"Round {self.current_round} Depth value: {depth_value}")

                        if self.current_round < 2:
                            # 准备进行下一次倒计时
                            self.current_round += 1
                            self.remaining_time = 5
                        else:
                            # 两次倒计时完成，停止计时器
                            self.countdown_timer.stop()
                            self.label_10.setStyleSheet("color: black;font-size: 24px;") 
                            print(f"All recorded depth values: {self.depth_values}")
                            self.draw_y_axis(self.z_near_value,self.z_far_value)
                            self.draw_x_axis()
                            self.label.setCountdown(None)

                # 启动计时器
            self.countdown_timer.timeout.connect(update_countdown)
            self.countdown_timer.start(1000)  # 每秒触发一次
        else:
            depth_value = self.label_6.text()
            
            if self.manual_position==0:
                self.label_9.setText("The Near Side Distance: "+depth_value)
                self.z_far_value=depth_value[:len(depth_value)-2]
            else:
                self.label_10.setText("The Near Side Distance: "+depth_value)
                self.z_far_value=depth_value[:len(depth_value)-2]
    def show_foot_step(self,left_y_value_list,left_depth_value_list,right_y_value_list,right_depth_value_list):
        window_size = 3
        def moving_average(data, window_size):
            return np.convolve(data, np.ones(window_size)/window_size, mode='valid')
        
        smoothed_data_y_left = moving_average(left_y_value_list, window_size)
        smoothed_data_y_left=-smoothed_data_y_left
        smoothed_data_z_left = moving_average(left_depth_value_list, window_size)
        local_max_y_left = argrelextrema(smoothed_data_y_left, np.less,order=3)[0]
        local_max_z_left = argrelextrema(smoothed_data_z_left, np.less,order=3)[0]
        #print("y minima ",local_max_y)
        #print("z minima ",local_max_z)
        #elf.foot_step_count=len(local_max_y_left)
        #self.label.setFootstep(self.foot_step_count)
        smoothed_data_y_right = moving_average(right_y_value_list, window_size)
        smoothed_data_y_right=-smoothed_data_y_right
        smoothed_data_z_right = moving_average(right_depth_value_list, window_size)
        local_max_y_right = argrelextrema(smoothed_data_y_right, np.less,order=3)[0]
        local_max_z_right = argrelextrema(smoothed_data_z_right, np.less,order=3)[0]
        #print("y minima ",local_max_y)
        #print("z minima ",local_max_z)
        self.foot_step_count=len(local_max_z_left)+len(local_max_z_right)
        self.label_15.setText(str(self.foot_step_count))
        self.label.setFootstep(self.foot_step_count)
        if  self.foot_step_count==self.foot_step_time_index+1:
            if self.foot_step_count==1:
                self.start_time=time.time()
            else:
                end_time=time.time()
                processing_time=end_time-self.start_time
                self.start_time=time.time()
                self.foot_step_left=processing_time
            self.foot_step_time_index=self.foot_step_count
            self.foot_step_left=int(60/self.foot_step_left)
            self.label_17.setText(str(self.foot_step_left))
    def show_foot_step_distance(self,depth_left,depth_right,left_depth_value_list,right_depth_value_list):
        #local_max_z_left=0
        #local_max_z_right=0
        window_size = 3
        def moving_average(data, window_size):
            return np.convolve(data, np.ones(window_size)/window_size, mode='valid')
        #smoothed_data_y=-smoothed_data_y

        smoothed_data_z_left = moving_average(left_depth_value_list, window_size)
        smoothed_data_z_right = moving_average(right_depth_value_list, window_size)
        local_min_z_left = argrelextrema(smoothed_data_z_left , np.less,order=3)[0]
        local_min_z_right = argrelextrema(smoothed_data_z_right, np.less,order=3)[0]
        local_max_z_left = argrelextrema(smoothed_data_z_left , np.greater,order=3)[0]
        local_max_z_right = argrelextrema(smoothed_data_z_right, np.greater,order=3)[0]
        
        count_left=0
        
        if len(local_max_z_left)< len(local_min_z_left):
                count_left=1
                
                
        
        
        if len(local_min_z_left) > count_left:
            local_min_z_left_index=local_min_z_left[len(local_min_z_left)-1]
            self.right_distance_start_left=smoothed_data_z_left[local_min_z_left_index]
            self.right_distance_start_right= smoothed_data_z_right[local_min_z_left_index]
        if len(local_max_z_left)>0:
            local_max_z_left_index=local_max_z_left[len(local_max_z_left)-1]
            self.right_distance_end_left=smoothed_data_z_left[local_max_z_left_index]
            self.right_distance_end_right= smoothed_data_z_right[local_max_z_left_index]
        if len(local_min_z_left) > 0 and len(local_max_z_left)>0 :
            #left_foot_distance=self.right_distance_end_left- self.right_distance_start_left
            #right_foot_distance=self.right_distance_end_right- self.right_distance_start_right
            left_foot_distance=self.right_distance_start_left- self.right_distance_end_left
            right_foot_distance=self.right_distance_start_right- self.right_distance_end_right
            left_distance=abs(left_foot_distance)+abs(right_foot_distance)
            print("left_distance")
            print(left_distance)
            self.foot_step_count=left_distance
            #self.label.setFootstep(self.foot_step_count,1)
            self.label_19.setText(f"{left_distance:.1f}")
            
        local_min_z_left = np.array([])
        local_max_z_left= np.array([])
        
        if len(local_min_z_right)>0:
            #print(len(local_min_z_right))
            local_min_z_right_index=local_min_z_right[len(local_min_z_right)-1]
            #print(local_min_z_right_index)
            self.left_distance_start_right=smoothed_data_z_right[local_min_z_right_index]
            self.left_distance_start_left= smoothed_data_z_left[local_min_z_right_index]
        if len(local_max_z_right)>0:
            local_max_z_right_index=local_max_z_right[len(local_max_z_right)-1]
            self.left_distance_end_right=smoothed_data_z_right[local_max_z_right_index]
            self.left_distance_end_left= smoothed_data_z_left[local_max_z_right_index]
        if len(local_min_z_right)>0 and len(local_max_z_right)>0:
            #right_foot_distance=self.left_distance_end_right- self.left_distance_start_right
            #left_foot_distance=self.left_distance_end_left- self.left_distance_start_left
            right_foot_distance=self.left_distance_start_right- self.left_distance_end_right
            left_foot_distance=self.left_distance_start_left- self.left_distance_end_left
            print(right_foot_distance)
            print(left_foot_distance)
            right_distance=abs(left_foot_distance)+abs(right_foot_distance)
            print("right_distance")
            #self.foot_step_count=left_foot_distance
            #print(right_distance)
            self.foot_step_left=right_distance
            
            self.label_21.setText(f"{right_distance:.1f}")
        #plt.ion()
        #plt.plot(depth_left,label="left")
        #plt.plot(depth_right,label="right")
        #if len(local_max_z_left) >0 and len(local_min_z_left)>0 :
        
            #plt.scatter(local_max_z_left, smoothed_data_z_left[local_max_z_left], color='purple', label='Max Left', zorder=5)
            #plt.scatter(local_min_z_left, smoothed_data_z_left[local_min_z_left], color='green', label='Min Left', zorder=5)
        #plt.pause(0.01)  # 暂停以更新图像
        
        #plt.legend()
        #plt.show()
        local_min_z_right = np.array([])
        local_max_z_right= np.array([])
    def show_drop_foot_degree(self,left_y_ankle,right_y_ankle,left_degree_ankle,right_degree_ankle):
        window_size = 5
        def moving_average(data, window_size):
            return np.convolve(data, np.ones(window_size)/window_size, mode='valid')
        #smoothed_data_y=-smoothed_data_y

        smoothed_data_y_left = moving_average(left_y_ankle, window_size)
        #smoothed_data_y_left=-smoothed_data_y_left
        smoothed_data_y_right = moving_average(right_y_ankle, window_size)
        #smoothed_data_y_right=-smoothed_data_y_right
        smoothed_data_degree_left = moving_average(left_degree_ankle, window_size)
        smoothed_data_degree_right = moving_average(right_degree_ankle, window_size)

        local_min_y_left = argrelextrema(smoothed_data_y_left , np.less,order=3)[0]
        local_min_y_right = argrelextrema(smoothed_data_y_right, np.less,order=3)[0]
        local_max_y_left = argrelextrema(smoothed_data_y_left , np.greater,order=3)[0]
        local_max_y_right = argrelextrema(smoothed_data_y_right, np.greater,order=3)[0]
        print("local_max_y_left")
        print(len(local_max_y_left))
        #self.count_local_value=0
        if len(local_max_y_left) >self.count_local_value_left :
            if  len(local_min_y_left)>self.count_local_value_left :
                degree=0
                left_drop_foot_average=[]
                local_max_y_left_index=local_max_y_left[len(local_max_y_left)-1]
                local_min_y_left_index=local_min_y_left[len(local_min_y_left)-1]
                print(local_max_y_left_index)
                print(local_min_y_left_index)
                if local_min_y_left_index>local_max_y_left_index:
                        
                        
                        left_drop_foot_average.extend(smoothed_data_degree_left[local_max_y_left_index:local_min_y_left_index])
                        self.left_drop_foot_average.extend(smoothed_data_degree_left[local_max_y_left_index:local_min_y_left_index])
                        for i in left_drop_foot_average:
                            degree=degree+i
                        degree=degree/(len(left_drop_foot_average))
                        print("left_degree")
                        print(degree)
                        self.foot_step_count=degree
                        self.count_local_value_left=len(local_max_y_left)
                elif len(local_min_y_left)>len(local_max_y_left):
                        local_max_y_left_index=local_max_y_left[len(local_max_y_left)-2]
                        local_min_y_left_index=local_min_y_left[len(local_min_y_left)-1]
                        left_drop_foot_average.extend(smoothed_data_degree_left[local_max_y_left_index:local_min_y_left_index])
                        self.left_drop_foot_average.extend(smoothed_data_degree_left[local_max_y_left_index:local_min_y_left_index])
                        for i in left_drop_foot_average:
                            degree=degree+i
                        degree=degree/(len(left_drop_foot_average))
                        print("right_degree")
                        print(degree)
                        self.foot_step_count=degree
                        self.count_local_value_left=len(local_max_y_left)
        
        if len(local_max_y_right) >self.count_local_value_right :
            if  len(local_min_y_right)>self.count_local_value_right :
                degree=0
                right_drop_foot_average=[]
                local_max_y_right_index=local_max_y_right[len(local_max_y_right)-1]
                local_min_y_right_index=local_min_y_right[len(local_min_y_right)-1]
                if local_min_y_right_index>local_max_y_right_index:
                        print("local_max_index")
                        print(local_max_y_right_index)
                        print(local_min_y_right_index)
                        right_drop_foot_average.extend(smoothed_data_degree_right[local_max_y_right_index:local_min_y_right_index])
                        self.right_drop_foot_average.extend(smoothed_data_degree_right[local_max_y_right_index:local_min_y_right_index])
                        for i in right_drop_foot_average:
                            degree=degree+i
                        degree=degree/(len(right_drop_foot_average))
                        print(degree)
                        self.foot_step_left=degree
                        self.count_local_value_right=len(local_max_y_right)
                elif len(local_min_y_right)>len(local_max_y_right):
                        local_max_y_right_index=local_max_y_right[len(local_max_y_right)-1]
                        local_min_y_right_index=local_min_y_right[len(local_min_y_right)]
                        right_drop_foot_average.extend(smoothed_data_degree_right[local_max_y_right_index:local_min_y_right_index])
                        self.right_drop_foot_average.extend(smoothed_data_degree_right[local_max_y_right_index:local_min_y_right_index])
                        for i in right_drop_foot_average:
                            degree=degree+i
                        degree=degree/(len(right_drop_foot_average))
                        print(degree)
                        self.foot_step_left=degree
                        self.count_local_value_right=len(local_max_y_right)
                        
    def calculate_com(self, landmarks, h, w, mass_ratios,confidence_threshold=0.5):
        total_weight = 0
        com_x, com_y = 0, 0

        for index, landmark in enumerate(landmarks):
            # 获取关键点的置信度
            confidence = landmark.visibility

            # 如果置信度高于阈值，才参与计算
            if confidence > confidence_threshold and index in mass_ratios:
                # 转换关键点的图像坐标
                x, y = int(landmark.x * w), int(landmark.y * h)

                # 获取当前关键点的权重
                weight = mass_ratios[index]

                # 加权累积质心坐标
                com_x += x * weight
                com_y += y * weight

                # 累积总权重
                total_weight += weight

        # 计算质心的最终坐标
        if total_weight > 0:
            com_x /= total_weight
            com_y /= total_weight
            return int(com_x), int(com_y)
        else:
            return None  # 如果没有有效关键点，返回 None
    def show_toe_degree(self,depth_value_right_toe,right_degree) :
        window_size = 5
        def moving_average(data, window_size):
            return np.convolve(data, np.ones(window_size)/window_size, mode='valid')
        #smoothed_data_y=-smoothed_data_y

        smoothed_data_z_right = moving_average(depth_value_right_toe, window_size)
        smoothed_data_degree_right = moving_average(right_degree, window_size)
        local_max_y_right = argrelextrema(smoothed_data_z_right , np.greater,order=3)[0]
        index=local_max_y_right[-1]
        toe_right_degree=smoothed_data_degree_right[index]
        self.foot_step_left=toe_right_degree







    def cancel_adjust_position(self):
        if self.pushButton_16.text()=="Start":
            self.adjust_position_function =False
            self.countdown_timer.stop()
            self.label.setCountdown(None)
        else:
            self.pushButton_16.setText("Start")  # 修改按钮文本
            self.label_9.setStyleSheet("color: black;font-size: 24px;") 
            self.label_10.setStyleSheet("color: black;font-size: 24px;") 
    def on_button_clicked(self):
        sender = self.sender()  # 獲取信號發送者
        print(f"你按下了: {sender.text()}")  # 顯示按鈕的文字
        """
        if self.input_speed=="First number":
            self.first_speed=int(sender.text())
        if sender.text()==".":
        """
        
        
        if sender.text()=="clear":
            self.first_speed=0
            self.label_8.setText("0.0")
        elif sender.text()=="enter":
            #adjust_speed
            print(self.first_speed)
            self.input_speed=False
            self.first_speed=0

        else:
            if self.manual_speed:
                self.first_speed=self.first_speed*10+float(sender.text())/10
                self.label_8.setText(str(self.first_speed))
            else :
                self.first_speed=self.first_speed*10+float(sender.text())/10
                self.label_7.setText(str(self.first_speed))
    def increase_speed(self):
        self_speed=float(self.label_8.text())
        self_speed+=0.1
        self.label_8.setText(f"{self_speed:.1f}")
    def decrease_speed(self):
        self_speed=float(self.label_8.text())
        if (self_speed<=0.0):
                self_speed==0.0
        self_speed-=0.1
        self.label_8.setText(f"{self_speed:.1f}")
    
        
    def start_train(self):
        if self.pushButton_21.text() == "Start":
            self.pushButton_21.setText("Cancel")
            self.customize_count=0
            self.gait_record=True
            self.right_x_value_list=[]
            self.right_y_value_list=[]
            self.right_line_degree=[]
            self.right_depth_value_mediapipe_calibrate_list=[]
            self.left_x_value_list=[]
            self.left_y_value_list=[]
            self.left_line_degree=[]
            self.left_depth_value_mediapipe_calibrate_list=[]
            self.foot_step_time=[]
            self.foot_step_count=0
            
            if self.selected_text =="Customize":
                speed_value=self.customize_speed[self.customize_count]
                self.label_8.setText(str(speed_value/10))
                data = bytes([self.trill_speed_command, speed_value]) 
                self.ser.write(data)
                
            else:
                speed_value=int(float(self.label_8.text())*10)
                data = bytes([self.trill_speed_command, speed_value]) 
                self.ser.write(data)
            self.count=10
            self.update_x_axis_check=False
            # 重置時間顯示（如果需要）
            if not self.is_paused:  # 非暫停狀態則重置
                self.elapsed_time = 0
                self.label_11.setText("00:00:00")
            try:
                self.countdown_timer_training.timeout.disconnect(self.update_training_time)
            except TypeError:
                pass  # 如果沒有連接則忽略

            # 啟動計時器
           # self.countdown_timer_training.timeout.disconnect()
            self.countdown_timer_training.timeout.connect(self.update_training_time)
            self.countdown_timer_training.start(1000) # 每秒觸發一次
            self.is_paused = False  # 重置暫停狀態
            
            self.label_15.setText(str(self.foot_step_count))
            self.gait_record_finish=False

        else:
            self.pushButton_21.setText("Start")
            data = bytes([self.trill_speed_command, 0]) 
            self.gait_record=False
            self.ser.write(data)
            self.gait_record_finish=True
            # 停止計時器並重置
            self.count=10
            self.clear_all_depth_items()
            self.countdown_timer_training.stop()
            self.elapsed_time = 0
            self.label_11.setText("00:00:00")  # 重置顯示
            self.is_paused = False  # 清除暫停狀態
            self.depth_items.clear()
            """
            plt.ion()
            #plt.plot(self.right_line_degree,label="right")
            #plt.plot(self.left_line_degree,label="left")
            plt.plot(self.right_y_value_list,label="y")
            plt.plot(sright_depth_value_mediapipe_calibrate_list="z")
            
            plt.legend()
            plt.show()
            """
            if self.selected_text_mediapipe=="Drop_Foot":
                np.save("left_drop_foot_degree.npy",self.left_drop_foot_average)
                np.save("right_drop_foot_degree.npy",self.right_drop_foot_average)
            plt.show()

            np.save("right_degree.npy",self.right_line_degree)
            np.save("right_x.npy",self.right_x_value_list)
            np.save("right_y.npy",self.right_y_value_list)
            np.save("right_depth.npy",self.right_depth_value_mediapipe_calibrate_list)
            np.save("left_degree.npy",self.left_line_degree)
            np.save("left_x.npy",self.left_x_value_list)
            np.save("left_y.npy",self.left_y_value_list)
            np.save("left_depth.npy",self.left_depth_value_mediapipe_calibrate_list)
            np.save("time.npy",self.foot_step_time[1:])
            #self.foot_step_time



    def pause_timer(self):
        if self.countdown_timer_training.isActive():
            # 暫停計時器
            data = bytes([self.trill_speed_command, 0]) 
            
            self.ser.write(data)
            self.countdown_timer_training.stop()
            self.is_paused = True
            self.pushButton_22.setText("Resume")
        else:
            # 恢復計時器
            self.countdown_timer_training.start(1000)
            speed_value=int(float(self.label_8.text())*10)
            data = bytes([self.trill_speed_command, speed_value]) 
            
            self.ser.write(data)
            self.is_paused = False
            self.pushButton_22.setText("Pause")

    def update_training_time(self):
        # 更新時間邏輯
       
        self.elapsed_time += 1

        # 格式化時間為 HH:MM:SS
        hours = self.elapsed_time // 3600
        minutes = (self.elapsed_time % 3600) // 60
        seconds = self.elapsed_time % 60
        
        self.label_11.setText(f"{hours:02}:{minutes:02}:{seconds:02}")
        depth_value = self.label_6.text()
        self.draw_training_data(float(depth_value[:len(depth_value)-2]))
        
        if self.update_x_axis_check:
            self.count+=1
            print(self.count)

        if((int(minutes*60)+int(seconds))>130 and self.count==10) :
            self.update_x_axis_check=True
            self.update_x_axis(self.z_near_value,self.z_far_value)
            self.count=0
            print("update")
       
        if self.selected_text =="Auto Speed":
            print(self.label.image_status())
            if self.label.image_status()==-2:
                
                speed_value=int((float(self.label_8.text())-0.2)*10)
                if speed_value<=0:
                    speed_value=0
                print(speed_value)
                data = bytes([self.trill_speed_command, speed_value]) 
                self.ser.write(data)
                self.label_8.setText(str(speed_value/10))
                
                
            elif self.label.image_status()==-1:
                
                speed_value=int((float(self.label_8.text())-0.1)*10)
                if speed_value<=0:
                    speed_value=0
                data = bytes([self.trill_speed_command, speed_value]) 
                self.ser.write(data)
                self.label_8.setText(str(speed_value/10))
            elif self.label.image_status()==1:
                speed_value=int((float(self.label_8.text())+0.1)*10)
                data = bytes([self.trill_speed_command, speed_value]) 
                self.ser.write(data)
        elif self.selected_text =="Fixed Speed":
            if self.label.image_status()==-2:
                
                speed_value=int((float(self.label_8.text())-0.2)*10)
                
                data = bytes([self.trill_speed_command, 0]) 
                self.ser.write(data)
        elif self.selected_text =="Customize":
            if self.customize_count==self.row_table-1:
                data = bytes([self.trill_speed_command, 0]) 
                self.ser.write(data)
            elif self.elapsed_time==self.customize_time[self.customize_count]:
                self.customize_count+=1
                speed_value=self.customize_speed[self.customize_count]
                self.label_8.setText(str(speed_value/10))
                data = bytes([self.trill_speed_command, speed_value]) 
                self.ser.write(data)
            



    def add_table_value(self):
        combo_value_minute = self.comboBox_3.currentIndex()  
        combo_value_second = self.comboBox_4.currentIndex()  
        qtime = QTime(int(combo_value_minute), int(combo_value_second))  # 創建 QTime 物件
        qtime=qtime.toString('hh:mm')
        print(self.selected_text)
        self.doubleSpinBox.setDecimals(1)
        spin_value = self.doubleSpinBox.value()
        print(spin_value)
        data=[str(qtime),str(spin_value),"0.0"]
        for column in range(4):
            if column==3:
                item = QStandardItem()  # 創建 QStandardItem 用來表示 Checkbox
                item.setCheckable(True)  # 設置為可勾選
                item.setCheckState(Qt.Unchecked)  # 設置勾選狀態
            else:
                item = QStandardItem(data[column])  # 創建普通的資料格子
                #self.model.setItem(0,column, item)  # 設置每個格子的資料
            self.model.setItem(self.row_table,column,item)
        self.row_table+=1
    def delete_checked_rows(self):
        """刪除已勾選的行"""
        rows_to_delete = []
        
        # 遍歷所有行，檢查第四列的勾選框是否選中
        for row in range(self.model.rowCount()):
            checkbox_item = self.model.item(row, 3)  # 獲取第四列的勾選框
            if checkbox_item and checkbox_item.checkState() == Qt.Checked:  # 如果勾選框被選中
                rows_to_delete.append(row)
        
        # 從最後一行開始刪除，防止刪除行時索引錯亂
        for row in reversed(rows_to_delete):
            self.row_table-=1
            self.model.removeRow(row)  # 刪除行
    def on_selection(self,index):
        self.selected_text = self.comboBox.itemText(index)
    def on_selection_mediapipe(self,index):
        self.selected_text_mediapipe = self.comboBox_2.itemText(index)
        if self.selected_text_mediapipe!="None":
            self.mediapipe=True
            if self.selected_text_mediapipe=="Drop_Foot":
                
                self.left_node_1=25
                self.left_node_2=27
                self.left_node_3=31
                self.right_node_1=26
                self.right_node_2=28
                self.right_node_3=32
                self.left_node_4=-1
                self.right_node_4=-1
                """
                self.left_node_1=0
                self.left_node_2=11
                self.left_node_3=12
                self.right_node_1=7
                self.right_node_2=8
                self.right_node_3=9
                """    
            elif self.selected_text_mediapipe=="Toe":
                self.left_node_1=31
                self.left_node_2=29
                self.left_node_3=23
                self.right_node_1=32
                self.right_node_2=30
                self.right_node_3=24
                self.left_node_4=-1
                self.right_node_4=-1
                   
            elif self.selected_text_mediapipe=="Foot_step":
                self.left_node_1=23
                self.left_node_2=27
                self.left_node_3=31
                self.right_node_1=24
                self.right_node_2=28
                self.right_node_3=32
                self.left_node_4=27
                self.right_node_4=28
            elif self.selected_text_mediapipe=="body_step":
                self.left_node_1=11
                self.left_node_2=23
                self.left_node_3=13
                self.right_node_1=12
                self.right_node_2=24
                self.right_node_3=26
                self.left_node_4=-14
                self.right_node_4=-1
            elif self.selected_text_mediapipe=="body_step":
                self.left_node_1=25
                self.left_node_2=27
                self.left_node_3=29
                self.right_node_1=26
                self.right_node_2=28
                self.right_node_3=30
                self.left_node_4=-1
                self.right_node_4=-1
        else:
            self.mediapipe=False
    def export_customize_data(self):
        self.customize_speed=[]
        self.customize_time=[]
        
        column=0
        stack_time=0
        for column in range(2):
            for customize_data in range(self.row_table):
                if column==0:
                    item = self.model.item(customize_data,0)
                    items=item.text()
                    items=items.split(":")
                    self.customize_time.append(stack_time+int(items[0])*60+int(items[1]))
                    stack_time=stack_time+int(items[0])*60+int(items[1])
                elif column==1:
                    item = self.model.item(customize_data,1)
                    items=item.text()
                    self.customize_speed.append(int(float(items)*10))
            print(column)
            #column+=1
        print(self.customize_time)
        print(self.customize_speed)
    
    


    def opencv(self):
        def draw_custom_landmarks(image, landmarks, selected_points, custom_connections):
            h, w, _ = image.shape
            
            # 繪製連線
            for start_idx, end_idx in custom_connections:
                start = landmarks.landmark[start_idx]
                end = landmarks.landmark[end_idx]
                
                # 確保點的可見性
                if start.visibility > 0.3 and end.visibility > 0.3:
                    start_point = (int(start.x * w), int(start.y * h))
                    end_point = (int(end.x * w), int(end.y * h))
                    cv2.line(image, start_point, end_point, (0, 255, 0), 2)
            
            # 繪製點
            
            for idx in selected_points:
                point = landmarks.landmark[idx]
                if point.visibility > 0.3:
                    point_coords = (int(point.x * w), int(point.y * h))
                    cv2.circle(image, point_coords, 5, (255, 0, 0), -1)

        mp_pose = mp.solutions.pose
        pose = mp_pose.Pose()
        
# 初始化绘图工具
        mp_drawing = mp.solutions.drawing_utils
        # Get device product line for setting a supporting resolution
        pipeline_wrapper = rs.pipeline_wrapper( self.pipeline)
        pipeline_profile =  self.config.resolve(pipeline_wrapper)
        device = pipeline_profile.get_device()
        device_product_line = str(device.get_info(rs.camera_info.product_line))
        def calculate_angle(x,y):
            dx = y[0] - x[0]
            dy = y[1] - x[1]

            # 計算角度（弧度轉度數）
            angle = math.atan2(dy, dx)  # 使用 atan2 確保正確的象限
            angle_degrees = math.degrees(angle)

            return angle_degrees
        found_rgb = False
        for s in device.sensors:
            if s.get_info(rs.camera_info.name) == 'RGB Camera':
                found_rgb = True
                break
        if not found_rgb:
            print("The demo requires Depth camera with Color sensor")
            exit(0)

        self.config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16,30)
        self.config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8,30)
        
        # Start streaming
        self.pipeline.start( self.config)
        align_to = rs.stream.color
        align = rs.align(align_to)
        #frame_width=int(self.pipeline.get(cv2.CAP_PROP_FRAME_WIDTH))
        #frame_height=int(self.pipeline.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc =cv2.VideoWriter_fourcc(*'XVID')
        out=cv2.VideoWriter('output.avi',fourcc,10.0,(640,480))
        plt.ion() 
        try:
            o_vector=[]
            start_time=0
            while True:

                # Wait for a coherent pair of frames: depth and color
                frames =  self.pipeline.wait_for_frames()
                aligned_frames = align.process(frames)   
                depth_frame =aligned_frames.get_depth_frame()
                color_frame =aligned_frames.get_color_frame()
                if not depth_frame or not color_frame:
                    continue

                # Convert images to numpy arrays
                depth_image = np.asanyarray(depth_frame.get_data())
                #print("Max",np.max(depth_image))
                color_image = np.asanyarray(color_frame.get_data())
                rgb_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)
                """
                self.comboBox_2.addItem("None")
                self.comboBox_2.addItem("Drop_Foot")#32 28 26
                self.comboBox_2.addItem("Toe")#32 30 34 (34 new dot with 26x 32y 32z)
                self.comboBox_2.addItem("Foot_step")# 12 24 26
                self.comboBox_2.addItem("body_step")#12 11 23 24
                """
                
                #if self.mediapipe and self.gait_record:
                if self.mediapipe: 
                    results = pose.process(rgb_image)
                    if results.pose_landmarks:
                        line_right_shoulder=[]
                        line_right_hip=[]
                        line_right_knee=[]
                        line_left_shoulder=[]
                        line_left_hip=[]
                        line_left_knee=[]
                        selected_points=[]
                        custom_connections=[]
                        line_right_heel=[]
                        line_left_heel=[]
                        pre_o_vector=[]
                        
                        
                        for index,landmark in enumerate(results.pose_landmarks.landmark):
                # 获取每个关键点的置信度
                            confidence = landmark.visibility
                # 过滤置信度低于 0.5 的关键点
                            if confidence > 0.5:
                                h, w, _ = color_image.shape
                                x, y = int(landmark.x * w), int(landmark.y * h)
                                cv2.circle(color_image, (x, y), 5, (0, 255, 0), -1)
                                x_left_value_degree=0
                                x_right_value_degree=0
                                y_left_value_degree=0 
                                y_right_value_degree=0  
                                """
                                if self.selected_text_mediapipe=="body_step": 
                                    mass_ratios = {
                                    0: 0.081,  # 头部
                                    11: 0.11, 12: 0.11, 23: 0.11, 24: 11,  # 躯干
                                    13: 0.05, 14: 0.05,  # 左上肢
                                    25: 0.20, 26: 0.20,  # 左下肢
                                }
                                    print("body_step")#0 8.1% ///  11 12 23 24  43.2% /// 13 14 5% /////  25 26 10% each  
                                    com = self.calculate_com(results.pose_landmarks.landmark, h, w, mass_ratios)
                                """
                                
                                if index==self.left_node_1:
                                    
                                    if(x>=0 and x<640 and y<480 and y>=0):
                                        x_value_left_shoulder,y_value_left_shoulder,depth_value_mediapipe_calibrate_left_shoulder=self.label.calculate_roi_mediapipe_calibrate(depth_frame,x,y)     
                                        line_left_shoulder= [x_value_left_shoulder,y_value_left_shoulder]
                                        #y_left_value_degree=y
                                    #print(depth_value_mediapipe_calibrate)
                                if index==self.right_node_1:
                                    if(x>=0 and x<640 and y<480 and y>=0):
                                        #line_right_shoulder = [x, y]
                                        x_value_right_shoulder,y_value_right_shoulder,depth_value_mediapipe_calibrate_right_shoulder=self.label.calculate_roi_mediapipe_calibrate(depth_frame,x,y) 
                                        line_right_shoulder = [x_value_right_shoulder,y_value_right_shoulder] 
                                        #y_right_value_degree=y 
                                if index==self.left_node_2:
                                    if(x>=0 and x<640 and y<480 and y>=0):
                                        line_left_hip = [x, y]
                                        x_value_left_hip,y_value_left_hip,depth_value_mediapipe_calibrate_left_hip=self.label.calculate_roi_mediapipe_calibrate(depth_frame,x,y)  
                                        line_left_hip = [x_value_left_hip,y_value_left_hip]   
                                        #x_left_value_degree=x                             
                                if index==self.right_node_2:
                                    if(x>=0 and x<640 and y<480 and y>=0):
                                        line_right_hip = [x, y]
                                        x_value_right_hip,y_value_right_hip,depth_value_mediapipe_calibrate_right_hip=self.label.calculate_roi_mediapipe_calibrate(depth_frame,x,y)  
                                        line_right_hip = [x_value_right_hip,y_value_right_hip]
                                        #x_right_value_degree=x
                                if index==self.left_node_3:
                                    if(x>=0 and x<640 and y<480 and y>=0):
                                        #line_left_knee = [x, y]
                                        x_value_left_knee,y_value_left_knee,depth_value_mediapipe_calibrate_left_knee=self.label.calculate_roi_mediapipe_calibrate(depth_frame,x,y) 
                                        line_left_knee = [x_value_left_knee,y_value_left_knee] 
                                if index==self.right_node_3:
                                    if(x>=0 and x<640 and y<480 and y>=0):
                                        #line_right_knee = [x, y]
                                        x_value_right_knee,y_value_right_knee,depth_value_mediapipe_calibrate_right_knee=self.label.calculate_roi_mediapipe_calibrate(depth_frame,x,y)  
                                        line_right_knee = [x_value_right_knee,y_value_right_knee]
                                if self.left_node_4>0 and self.right_node_4>0:
                                    if index==self.left_node_4:
                                        if(x>=0 and x<640 and y<480 and y>=0):
                                        #line_right_knee = [x, y]
                                            x_value_left_heel,y_value_left_heel,depth_value_mediapipe_calibrate_left_heel=self.label.calculate_roi_mediapipe_calibrate(depth_frame,x,y)  
                                            line_left_heel = [x_value_left_heel,y_value_left_heel]
                                    if index==self.right_node_4:
                                        if(x>=0 and x<640 and y<480 and y>=0):
                                            x_value_right_heel,y_value_right_heel,depth_value_mediapipe_calibrate_right_heel=self.label.calculate_roi_mediapipe_calibrate(depth_frame,x,y)  
                                            line_right_heel = [x_value_right_heel,y_value_right_heel]
                                """
                                if  self.left_node_3==34:
                                    x=x_left_value_degree
                                    y=y_left_value_degree
                                    x_value_left_knee,y_value_left_knee,depth_value_mediapipe_calibrate_left_knee=self.label.calculate_roi_mediapipe_calibrate(depth_frame,x,y) 
                                    line_left_knee = [x_value_left_knee,y_value_left_knee] 
                                if  self.right_node_3==35:
                                    x=x_right_value_degree
                                    y=y_right_value_degree
                                    x_value_right_knee,y_value_right_knee,depth_value_mediapipe_calibrate_right_knee=self.label.calculate_roi_mediapipe_calibrate(depth_frame,x,y)  
                                    line_right_knee = [x_value_right_knee,y_value_right_knee]
                                """
                        if self.selected_text_mediapipe=="body_step":
                            mass_ratios = {
                                    0: 0.081,  # 头部
                                    11: 0.11, 12: 0.11, 23: 0.11, 24: 11,  # 躯干
                                    13: 0.05, 14: 0.05,  # 左上肢
                                    25: 0.20, 26: 0.20,  # 左下肢
                                }
                            print("body_step")#0 8.1% ///  11 12 23 24  43.2% /// 13 14 5% /////  25 26 10% each  
                            #com_x,com,y = self.calculate_com(results.pose_landmarks.landmark, h, w, mass_ratios)
                            com = self.calculate_com(results.pose_landmarks.landmark, h, w, mass_ratios)
                            #selected_points.extend([com_x,com_y])
                            #custom_connections.extend([com_x,com_y])
                            selected_points.extend([com])
                            custom_connections.extend([com])
                            """
                            if line_right_shoulder and  line_right_hip and line_right_knee:
                            
                                first_line=[]
                                second_line=[]
                                print("===============================================")
                                first_line.append((line_left_shoulder[0]+line_right_shoulder[0])/2)
                                first_line.append((line_left_shoulder[1]+line_right_shoulder[1])/2)
                                first_line.append((depth_value_mediapipe_calibrate_left_shoulder+depth_value_mediapipe_calibrate_right_hip)/2)
                                second_line.append(line_left_hip[0]-line_right_hip[0])
                                second_line.append(line_left_hip[1]-line_right_hip[1])
                                second_line.append((depth_value_mediapipe_calibrate_left_knee-depth_value_mediapipe_calibrate_right_hip)/2)
                                first_line=np.array(first_line)
                                second_line=np.array(second_line)
                                dot_product = np.dot(first_line, second_line)
                                first_line_length= np.linalg.norm(first_line)
                                second_line_length = np.linalg.norm(second_line)
                                cos_theta = dot_product / (first_line_length * second_line_length)
                                #cos_theta = np.clip(cos_theta, -1.0, 1.0)
                                theta_rad = np.arccos(cos_theta)
                                theta_deg = np.degrees(theta_rad)
                                self.right_x_value_list.append(line_right_shoulder[0]-line_right_hip[0])
                                self.right_y_value_list.append(line_right_shoulder[1]-line_right_hip[1])
                                self.right_y_value_list.append((line_left_shoulder[1]-line_right_shoulder[1])/2)
                                self.right_depth_value_mediapipe_calibrate_list.append(depth_value_mediapipe_calibrate_right_shoulder-depth_value_mediapipe_calibrate_right_hip)
                                self.right_line_degree.append(theta_deg)
                            """    

                        elif self.selected_text_mediapipe=="Toe":
                            x_vector=[]
                           
                            first_line=[]
                            second_line=[]
                            z_vector=[]
                            if line_right_shoulder and  line_right_hip and line_right_knee and line_left_shoulder and  line_left_hip and line_left_knee:
                                    
                                """
                                first_line.append((line_left_knee[0]-line_right_knee[0]))
                                first_line.append((line_left_knee[1]-line_right_knee[1]))
                                first_line.append((depth_value_mediapipe_calibrate_left_knee-depth_value_mediapipe_calibrate_right_knee))
                                second_line.append(line_right_shoulder[0]-line_right_hip[0])
                                second_line.append(line_right_shoulder[1]-line_right_hip[1])
                                second_line.append(depth_value_mediapipe_calibrate_right_shoulder-depth_value_mediapipe_calibrate_right_hip)
                                magnitude_v1 = np.linalg.norm(first_line)
                                magnitude_second_line = np.linalg.norm(second_line)
                                Vy=np.array(second_line)/ magnitude_second_line 
                                V1 = np.array(first_line)/ magnitude_v1 
                                x_vector=V1
                                
                                pre_o_vector.extend([((line_left_knee[0]+line_right_knee[0])/2),((line_left_knee[1]+line_right_knee[1])/2),(depth_value_mediapipe_calibrate_left_knee+depth_value_mediapipe_calibrate_right_knee)/2])
                                if o_vector:

                                    #V2=np.array(pre_o_vector)
                                    print("o_vactor")
                                    vector=np.subtract(o_vector,pre_o_vector).tolist()
                                    magnitude_V2 = np.linalg.norm(vector)
                                    V2=(vector)/magnitude_V2
                                    cross_product = np.cross(V1, V2)
                                    magnitude = np.linalg.norm(cross_product)
                                    y_vector = cross_product / magnitude
                                    z_unit_vector=np.linalg.norm(np.cross(x_vector,y_vector))
                                    z_vector=np.cross(x_vector,y_vector)
                                    z_vector=z_vector/z_unit_vector
                                
                               
                                
                                    print("z_vector")
                                    #second_line_without_y=[second_line[i] for i in [0,2]]
                                    second_line_without_y=Vy 
                                    z_vector_line_without_y=V2
                                    #second_line_without_y=[Vy[i] for i in [0,2]]
                                    #z_vector_line_without_y=[V2[i] for i in [0,2]]
                                    dot_product = np.dot(second_line_without_y, z_vector_line_without_y)
                                    z_vector_length= np.linalg.norm(z_vector_line_without_y)
                                    second_line_length = np.linalg.norm(second_line_without_y)
                                    cos_theta = dot_product / (z_vector_length * second_line_length)
                                    #cos_theta = np.clip(cos_theta, -1.0, 1.0)
                                    theta_rad = np.arccos(cos_theta)
                                    theta_deg = np.degrees(theta_rad)
                                    self.right_line_degree.append(theta_deg)
                                    
                                    dot_product = np.dot(first_line, z_vector)
                                    z_vector_length= np.linalg.norm(z_vector)
                                    first_line_length = np.linalg.norm(first_line)
                                    cos_theta = dot_product / (z_vector_length * first_line_length)
                                    #cos_theta = np.clip(cos_theta, -1.0, 1.0)
                                    theta_rad = np.arccos(cos_theta)
                                    theta_deg = np.degrees(theta_rad)
                                    self.left_line_degree.append(theta_deg)
                                    self.show_toe_degree(depth_value_mediapipe_calibrate_right_hip,theta_deg)
                                o_vector=pre_o_vector
                                """
                        elif self.selected_text_mediapipe=="Foot_step":
                            if line_right_shoulder and  line_right_hip and line_right_knee and line_left_shoulder and  line_left_hip and line_left_knee and line_left_heel and line_right_heel:
                                print("foot_step")
                                end_time=time.time()
                                process_time=end_time-start_time
                                start_time=end_time
                                #左腳腳跟 y z
                                self.left_y_value_list.append(line_left_heel[1])
                                self.left_depth_value_mediapipe_calibrate_list.append(depth_value_mediapipe_calibrate_left_heel) 
                                ##右腳腳跟 y z
                                self.right_y_value_list.append(line_right_heel[1])
                                self.right_depth_value_mediapipe_calibrate_list.append(depth_value_mediapipe_calibrate_right_heel)
                                
                                self.foot_step_time.append(process_time)
                                
                                #y depth heel 
                                #x degree toe
                                self.left_x_value_list.append(line_left_knee[1])
                                self.left_line_degree.append(depth_value_mediapipe_calibrate_left_knee) 
                                
                                self.right_x_value_list.append(line_right_knee[1])
                                self.right_line_degree.append(depth_value_mediapipe_calibrate_right_knee)
                                self.left_depth=depth_value_mediapipe_calibrate_left_heel
                                #self.show_foot_step(self.left_y_value_list,self.left_depth_value_mediapipe_calibrate_list,self.right_y_value_list,self.right_depth_value_mediapipe_calibrate_list)
                                self.show_foot_step_distance(depth_value_mediapipe_calibrate_left_heel,depth_value_mediapipe_calibrate_right_heel,self.left_depth_value_mediapipe_calibrate_list,self.right_depth_value_mediapipe_calibrate_list)
                                """
                                first_line=[]
                                second_line=[]
                                #print("===============================================")
                                first_line.append(line_right_shoulder[0]-line_right_hip[0])
                                first_line.append(line_right_shoulder[1]-line_right_hip[1])
                                first_line.append(depth_value_mediapipe_calibrate_right_shoulder-depth_value_mediapipe_calibrate_right_hip)
                                second_line.append(line_right_knee[0]-line_right_hip[0])
                                second_line.append(line_right_knee[1]-line_right_hip[1])
                                second_line.append(depth_value_mediapipe_calibrate_right_knee-depth_value_mediapipe_calibrate_right_hip)
                                first_line=np.array(first_line)
                                second_line=np.array(second_line)
                                dot_product = np.dot(first_line, second_line)
                                first_line_length= np.linalg.norm(first_line)
                                second_line_length = np.linalg.norm(second_line)
                                cos_theta = dot_product / (first_line_length * second_line_length)
                                #cos_theta = np.clip(cos_theta, -1.0, 1.0)
                                theta_rad = np.arccos(cos_theta)
                                theta_deg = np.degrees(theta_rad)
                                self.right_x_value_list.append((line_left_shoulder[0]-line_right_shoulder[0])/2)
                                self.right_y_value_list.append((line_left_shoulder[1]-line_right_shoulder[1])/2)
                                self.right_depth_value_mediapipe_calibrate_list.append(depth_value_mediapipe_calibrate_right_shoulder-depth_value_mediapipe_calibrate_right_hip)
                                self.right_line_degree.append(theta_deg)      
                                first_line=[]
                                second_line=[]
                                #print("===============================================")
                                first_line.append(line_left_shoulder[0]-line_left_hip[0])
                                first_line.append(line_left_shoulder[1]-line_left_hip[1])
                                first_line.append(depth_value_mediapipe_calibrate_left_shoulder-depth_value_mediapipe_calibrate_left_hip)
                                second_line.append(line_left_knee[0]-line_left_hip[0])
                                second_line.append(line_left_knee[1]-line_left_hip[1])
                                second_line.append(depth_value_mediapipe_calibrate_left_knee-depth_value_mediapipe_calibrate_left_hip)
                                first_line=np.array(first_line)
                                second_line=np.array(second_line)
                                dot_product = np.dot(first_line, second_line)
                                first_line_length= np.linalg.norm(first_line)
                                second_line_length = np.linalg.norm(second_line)
                                cos_theta = dot_product / (first_line_length * second_line_length)
                                #cos_theta = np.clip(cos_theta, -1.0, 1.0)
                                theta_rad = np.arccos(cos_theta)
                                theta_deg = np.degrees(theta_rad)
                                self.left_x_value_list.append(line_left_shoulder[0]-line_left_hip[0])
                                self.left_y_value_list.append(line_left_shoulder[1]-line_left_hip[1])
                                self.left_line_degree.append(theta_deg)
                                self.left_depth_value_mediapipe_calibrate_list.append(depth_value_mediapipe_calibrate_left_shoulder-depth_value_mediapipe_calibrate_left_hip) 
                                """
                        elif self.selected_text_mediapipe=="Drop_Foot":
                            if line_right_shoulder and  line_right_hip and line_right_knee and  line_left_shoulder and  line_left_hip and line_left_knee:
                                first_line=[]
                                second_line=[]
                                #print("===============================================")
                                first_line.append(line_right_shoulder[0]-line_right_hip[0])
                                first_line.append(line_right_shoulder[1]-line_right_hip[1])
                                first_line.append(depth_value_mediapipe_calibrate_right_shoulder-depth_value_mediapipe_calibrate_right_hip)
                                second_line.append(line_right_knee[0]-line_right_hip[0])
                                second_line.append(line_right_knee[1]-line_right_hip[1])
                                second_line.append(depth_value_mediapipe_calibrate_right_knee-depth_value_mediapipe_calibrate_right_hip)
                                first_line=np.array(first_line)
                                second_line=np.array(second_line)
                                dot_product = np.dot(first_line, second_line)
                                first_line_length= np.linalg.norm(first_line)
                                second_line_length = np.linalg.norm(second_line)
                                cos_theta = dot_product / (first_line_length * second_line_length)
                                #cos_theta = np.clip(cos_theta, -1.0, 1.0)
                                theta_rad = np.arccos(cos_theta)
                                theta_deg_right = np.degrees(theta_rad)
                                self.right_x_value_list.append((line_left_shoulder[0]-line_right_shoulder[0])/2)
                                self.right_y_value_list.append(line_right_hip[1])
                                self.right_depth_value_mediapipe_calibrate_list.append(depth_value_mediapipe_calibrate_right_shoulder-depth_value_mediapipe_calibrate_right_hip)
                                self.right_line_degree.append(theta_deg_right)       
                                first_line_left=[]
                                second_line_left=[]
                                #print("===============================================")
                                first_line_left.append(line_left_shoulder[0]-line_left_hip[0])
                                first_line_left.append(line_left_shoulder[1]-line_left_hip[1])
                                first_line_left.append(depth_value_mediapipe_calibrate_left_shoulder-depth_value_mediapipe_calibrate_left_hip)
                                second_line_left.append(line_left_knee[0]-line_left_hip[0])
                                second_line_left.append(line_left_knee[1]-line_left_hip[1])
                                second_line_left.append(depth_value_mediapipe_calibrate_left_knee-depth_value_mediapipe_calibrate_left_hip)
                                first_line=np.array(first_line_left)
                                second_line=np.array(second_line_left)
                                dot_product = np.dot(first_line, second_line)
                                first_line_length= np.linalg.norm(first_line)
                                second_line_length = np.linalg.norm(second_line)
                                cos_theta = dot_product / (first_line_length * second_line_length)
                                #cos_theta = np.clip(cos_theta, -1.0, 1.0)
                                theta_rad = np.arccos(cos_theta)
                                theta_deg_left = np.degrees(theta_rad)
                                self.left_x_value_list.append(line_left_shoulder[0]-line_left_hip[0])
                                self.left_y_value_list.append(line_left_hip[1])# y point with ankle
                                self.left_line_degree.append(theta_deg_left)        
                                self.left_depth_value_mediapipe_calibrate_list.append(depth_value_mediapipe_calibrate_left_shoulder-depth_value_mediapipe_calibrate_left_hip)
                                #self.show_drop_foot_degree(self.left_y_value_list,self.right_y_value_list,self.left_line_degree,self.right_line_degree)#point not list
                                self.show_drop_foot_degree(self.left_depth_value_mediapipe_calibrate_list,self.right_depth_value_mediapipe_calibrate_list,self.left_line_degree,self.right_line_degree)#point not list
                                
                        #selected_points = [12, 11, 0]  # 要繪製的點
                        elif self.selected_text_mediapipe=="Under_Pronation":
                            if line_right_shoulder and  line_right_hip and line_right_knee and  line_left_shoulder and  line_left_hip and line_left_knee:
                                first_line=[]
                                second_line=[]
                                #print("===============================================")
                                first_line.append(line_right_shoulder[0]-line_right_hip[0])
                                first_line.append(line_right_shoulder[1]-line_right_hip[1])
                                first_line.append(depth_value_mediapipe_calibrate_right_shoulder-depth_value_mediapipe_calibrate_right_hip)
                                second_line.append(line_right_knee[0]-line_right_hip[0])
                                second_line.append(line_right_knee[1]-line_right_hip[1])
                                second_line.append(depth_value_mediapipe_calibrate_right_knee-depth_value_mediapipe_calibrate_right_hip)
                                first_line=np.array(first_line)
                                second_line=np.array(second_line)
                                dot_product = np.dot(first_line, second_line)
                                first_line_length= np.linalg.norm(first_line)
                                second_line_length = np.linalg.norm(second_line)
                                cos_theta = dot_product / (first_line_length * second_line_length)
                                #cos_theta = np.clip(cos_theta, -1.0, 1.0)
                                theta_rad = np.arccos(cos_theta)
                                theta_deg_right = np.degrees(theta_rad)
                                self.right_x_value_list.append((line_left_shoulder[0]-line_right_shoulder[0])/2)
                                self.right_y_value_list.append(line_right_hip[1])
                                self.right_depth_value_mediapipe_calibrate_list.append(depth_value_mediapipe_calibrate_right_shoulder-depth_value_mediapipe_calibrate_right_hip)
                                self.right_line_degree.append(theta_deg_right)       

                                first_line_left=[]
                                second_line_left=[]
                                #print("===============================================")
                                first_line_left.append(line_left_shoulder[0]-line_left_hip[0])
                                first_line_left.append(line_left_shoulder[1]-line_left_hip[1])
                                first_line_left.append(depth_value_mediapipe_calibrate_left_shoulder-depth_value_mediapipe_calibrate_left_hip)
                                second_line_left.append(line_left_knee[0]-line_left_hip[0])
                                second_line_left.append(line_left_knee[1]-line_left_hip[1])
                                second_line_left.append(depth_value_mediapipe_calibrate_left_knee-depth_value_mediapipe_calibrate_left_hip)
                                first_line=np.array(first_line_left)
                                second_line=np.array(second_line_left)
                                dot_product = np.dot(first_line, second_line)
                                first_line_length= np.linalg.norm(first_line)
                                second_line_length = np.linalg.norm(second_line)
                                cos_theta = dot_product / (first_line_length * second_line_length)
                                #cos_theta = np.clip(cos_theta, -1.0, 1.0)
                                theta_rad = np.arccos(cos_theta)
                                theta_deg_left = np.degrees(theta_rad)
                                #self.left_x_value_list.append(line_left_shoulder[0]-line_left_hip[0])
                                #self.left_y_value_list.append(line_left_hip[1])# y point with ankle
                                self.left_line_degree.append(theta_deg_left)        
                                self.left_depth_value_mediapipe_calibrate_list.append(depth_value_mediapipe_calibrate_left_shoulder-depth_value_mediapipe_calibrate_left_hip)
                                

                        selected_points.extend([self.left_node_1,self.left_node_2,self.left_node_3,self.right_node_1,self.right_node_2,self.right_node_3])
                        custom_connections.extend([np.array([self.left_node_1,self.left_node_2]),np.array([self.left_node_2,self.left_node_3]),np.array([self.right_node_1,self.right_node_2]),np.array([self.right_node_2,self.right_node_3])])
                        line_right_shoulder=[]
                        line_right_hip=[]
                        line_right_knee=[]
                        line_left_shoulder=[]
                        line_left_hip=[]
                        line_left_knee=[]
                        #custom_connections = [(12, 11),(11, 0),(0,12)]       
            # 绘制关键点连线
                        draw_custom_landmarks(rgb_image, results.pose_landmarks, selected_points, custom_connections)
                        #mp_drawing.draw_landmarks(rgb_image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

                # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
                #depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
                bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
                if self.gait_record:
                    text=f"{float(self.foot_step_count):.2f}"
                    cv2.putText(bgr_image,str(text),(400,400),cv2.FONT_HERSHEY_SIMPLEX,3,(0,255,0),2) 
                    text=f"{float(self.foot_step_left):.2f}"   
                    cv2.putText(bgr_image,str(text),(50,400),cv2.FONT_HERSHEY_SIMPLEX,3,(255,0,0),2)    
                    
                    out.write(bgr_image)
                if self.gait_record_finish and self.gait_record==False:
                    out.release()
                elif self.gait_record_finish:
                    fourcc =cv2.VideoWriter_fourcc(*'XVID')
                    out=cv2.VideoWriter('output2.avi',fourcc,10.0,(640,480))
                    self.gait_record_finish=False
                #depth_colormap_dim = depth_colormap.shape
                color_colormap_dim = color_image.shape
                """
                # If depth and color resolutions are different, resize color image to match depth image for display
                if depth_colormap_dim != color_colormap_dim:
                    resized_color_image = cv2.resize(color_image, dsize=(depth_colormap_dim[1], depth_colormap_dim[0]), interpolation=cv2.INTER_AREA)
                    images = np.hstack((resized_color_image, depth_colormap))
                else:
                    images = np.hstack((color_image, depth_colormap))
                """
                # Show images
                height, width, channel = color_image.shape
                bytesPerline = channel * width
                
                depth_value = self.label.calculate_roi(depth_frame)
                
                #print(depth_value)
                depth_value=depth_value*100
                """
                self.label_6.setText(f"{depth_value:.1f} cm")
                """
                qimg = QImage(rgb_image , width, height, bytesPerline, QImage.Format_RGB888)
                self.label.setPixmap(QPixmap.fromImage(qimg)) 
                
                #cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
                #cv2.imshow('RealSense', images)
                #cv2.waitKey(1)
        except Exception as e:
                #print(f"Eooro in thread:{e}")
                traceback.print_exc()
        finally:

            # Stop streaming
            #self.pipeline.stop()
            sys.exit()
            out.release()
        """cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Cannot open camera")
            exit()
        else:
            self.ocv=True
            
        while self.ocv:
            
            ret, frame = cap.read()
            if not ret:
                print("Cannot receive frame")
                break
            frame = cv2.resize(frame, (640, 480))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channel = frame.shape
            bytesPerline = channel * width
            qimg = QImage(frame, width, height, bytesPerline, QImage.Format_RGB888)
            self.label.setPixmap(QPixmap.fromImage(qimg)) 
       """
    
