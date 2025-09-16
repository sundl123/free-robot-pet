#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import cv2
import numpy as np
from LOBOROBOT import LOBOROBOT # 载入机器人库
import  RPi.GPIO as GPIO
import time  
"""
* @par Copyright (C): 2010-2020, hunan CLB Tech
* @file         OpencvFaceTracking
* @version      V2.0
* @details
* @par History

@author: zhulin
"""

# 按键及LED初始化
BtnPin  = 19
Gpin    = 5
Rpin    = 6

# 从网络摄像头获取输入
cap = cv2.VideoCapture(0)
clbrobot = LOBOROBOT()  # 实例化机器人对象

# Configure min and max servo pulse lengths
servo_min = 150  # Min pulse length out of 4096
servo_max = 600  # Max pulse length out of 4096
# Helper function to make setting a servo pulse width simpler.
# 频率设置为50hz，适用于舵机系统。
clbrobot.set_servo_angle(5,90)  #底座舵机
clbrobot.set_servo_angle(4,75)  #顶部舵机

time.sleep(0.5)

# 将视频尺寸减小到320x240，这样rpi处理速度就会更快
cap.set(3,320)
cap.set(4,240)

#引入分类器
face_cascade = cv2.CascadeClassifier( 'face1.xml' )

# 键盘控制函数         
def keysacn():
    val = GPIO.input(BtnPin)
    while GPIO.input(BtnPin) == False:
        val = GPIO.input(BtnPin)
    while GPIO.input(BtnPin) == True:
        time.sleep(0.01)
        val = GPIO.input(BtnPin)
        if val == True:
            GPIO.output(Rpin,1)
            while GPIO.input(BtnPin) == False:
                GPIO.output(Rpin,0)
        else:
            GPIO.output(Rpin,0)

GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BCM)
GPIO.setup(Gpin, GPIO.OUT)     # 设置绿色Led引脚模式输出
GPIO.setup(Rpin, GPIO.OUT)     # 设置红色Led引脚模式输出
GPIO.setup(BtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # 设置输入BtnPin模式，拉高至高电平(3.3V) 

# 键盘控制函数 
keysacn()

while True:   
    ret,frame = cap.read()
    gray= cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    #对灰度图进行.detectMultiScale()
    faces=face_cascade.detectMultiScale(gray)   
    clbrobot.t_stop(0) # 机器人停止
    if len(faces)>0:
        print('face found!')
        (x,y,w,h) = faces[0]
        cv2.rectangle(frame,(x,y),(x+h,y+w),(0,255,0),2)
        result=(x,y,w,h)
        x=result[0]+w/2
        y=result[1]+h/2
        facebool = True 
        
        for(x,y,w,h) in faces:
            #找到矩形的中心位置
            cv2.rectangle(frame,(x,y),(x+h,y+w),(0,255,0),2)
            result=(x,y,w,h)
            x=result[0]+w/2
            y=result[1]+h/2 
            x_p = int(round(x))
            print x_p
        # 设定一个范围
        x_Lower = 150
        x_Upper = 180
        # 判断X方向范围来判断机器人的运动
        if x_p > x_Lower and x_p < x_Upper:
            clbrobot.t_up(50,0)            # 机器人前进
        elif x_p < x_Lower:
            clbrobot.turnLeft(50,0)       # 机器人左转
        elif x_p > x_Upper:
            clbrobot.turnRight(50,0)     # 机器人右转                
        else:
                clbrobot.t_stop(0)      # 机器人停止
    # 显示窗口画面        
    cv2.imshow("capture", frame)        
    if cv2.waitKey(1) & 0xFF == ord('q'):
            clbrobot.t_stop(0) # 机器人停止
            cap.release()
            GPIO.cleanup()
            cv2.destroyAllWindows() 
            break
        
clbrobot.t_stop(0) # 机器人停止
cap.release()
cv2.destroyAllWindows()       