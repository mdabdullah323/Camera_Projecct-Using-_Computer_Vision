""" My Camera Application 
    
    Author : Md.Abdullah

"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QImage, QIcon
import cv2
from PyQt5.QtCore import QTimer
import datetime

class Window(QWidget):
    # Main app Window
    
    def __init__(self):
        super().__init__()
        
        # variables for app window 
        self.window_width = 640
        self.window_height = 400
        
        # image variables 
        
        self.img_width = 640
        self.img_height = 400
        
        """ Others variables"""
        
        self.dt = '0-0-0'
        self.record_flage = False
        """ Load Icon"""
        
        self.camera_icon = QIcon(cap_icon_path)
        self.rec_icon = QIcon(rec_icon_path)
        self.stop_icon = QIcon(stop_icon_path)
        
        # To save the video
        
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        
        """"set up the window """
        
        self.setWindowTitle("My camera App")
        self.setGeometry(200,200, self.window_width, self.window_height)
        self.setFixedSize(self.window_width,self.window_height)  
        
        # Setup Timer
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        
        
        self.ui()                          
        
    def ui(self):
        
        """ Contain All Ui Thinks"""
        
        #layoout
        
        grid = QGridLayout()
        self.setLayout(grid)
        
        
        self.image_label = QLabel(self)
        self.image_label.setGeometry(0, 0, self.img_width, self.img_height)
        
        """ Capture Button """
        self.capture_btn = QPushButton(self)
        self.capture_btn.setIcon(self.camera_icon)
        self.capture_btn.setStyleSheet("border-radius: 30;border : 2px solid black; border-width: 3px")
        self.capture_btn.setFixedSize(60,60)
        self.capture_btn.clicked.connect(self.save_image)
        
        
        """ Record Button """
        self.rec_btn = QPushButton(self)
        #self.rec_btn.setIcon(self.rec_icon)
        self.rec_btn.setStyleSheet("border-radius: 30;border : 2px solid black; border-width: 3px")
        self.rec_btn.setFixedSize(60,60)
        self.rec_btn.clicked.connect(self.record)
        
        
        if not self.timer.isActive():
            self.cap =cv2.VideoCapture(0)
            self.timer.start(20)
        
        
        """ Add thingns to Layout in capture button"""
        grid.addWidget(self.capture_btn, 0,0)
        grid.addWidget(self.image_label, 0,1,2,3)
        grid.addWidget(self.rec_btn, 1,0)
       
        
        
        self.show()
        
        
    def update(self):
    
        """ updates Frame"""
        
        _, self.frame = self.cap.read()
        
        if self.record_flage == True:
            
            self.rec_btn.setIcon(self.stop_icon)
            self.frame = cv2.circle(self.frame, (20,70),5,(0,0,255),10)
        else:
            self.rec_btn.setIcon(self.rec_icon)
        
        frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)#  Blue ,Green,Red-RGb
        
        height,width,chanel = frame.shape
        step = chanel * width
        
        q_frame = QImage(frame.data,width,height,step,QImage.Format_RGB888)
        self.image_label.setPixmap(QPixmap.fromImage(q_frame))
    
    
    def save_image(self):
        """ Save image frome Camera """
        print (" Saving Image")
        self.get_time()
        cv2.imwrite(f"{self.dt}.png",self.frame)
        
        
    def record(self):
        """record Video"""
        
        
        if self.record_flage == True:
            self.record_flage = False
            
        else:
            self.record_flage  = True
            self.get_time()
            
            self.out =cv2.VideoWriter(f"{self.dt}.avi",self.fourcc,20.0,(self.img_width, self.img_height))
        
    def get_time(self):
        now = datetime.datetime.now()
        self.dt = now.strftime("%d-%m-%y,%H-%M-%S")

# Icon variable


cap_icon_path  = 'capture.png'
rec_icon_path = 'video-camera.png'
stop_icon_path = 'stop.png'


#Run
if __name__=='__main__':
    app = QApplication(sys.argv)
    win = Window()
    sys.exit(app.exec_())