#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
* @par Copyright (C): 2010-2020, hunan CLB Tech
* @file         6.openCVLineFollowingRobot
* @version      V2.0
* @details
* @par History

@author: zhulin
"""
import numpy as np
import cv2
from LOBOROBOT import LOBOROBOT # 载入机器人库
import  RPi.GPIO as GPIO
import time  

video_capture = cv2.VideoCapture(0)
video_capture.set(3,160) 
video_capture.set(4,120) 

# 按键及LED初始化
BtnPin  = 19
Gpin    = 5
Rpin    = 6

#初始化舵机
clbrobot = LOBOROBOT()  # 实例化机器人对象

# Configure min and max servo pulse lengths
servo_min = 150  # Min pulse length out of 4096
servo_max = 600  # Max pulse length out of 4096

# 频率设置为50hz，适用于舵机系统。
clbrobot.set_servo_angle(10,90)  # 底座舵机 90 
clbrobot.set_servo_angle(9,145)  # 顶部舵机 145

time.sleep(0.5)


# 按键控制函数
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
while 1:
    # Capture the frames
    ret, frame = video_capture.read()
    # Crop the image
    crop_img =frame[60:120, 0:160]
    # Convert to grayscale
    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    # Gaussian blur
    blur = cv2.GaussianBlur(gray,(5,5),0)
    # Color thresholding
    ret,thresh1 = cv2.threshold(blur,60,255,cv2.THRESH_BINARY_INV)
    # Erode and dilate to remove accidental line detections
    mask = cv2.erode(thresh1, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    
   # Find the contours of the frame
    image,contours,hierarchy = cv2.findContours(mask.copy(), 1, cv2.CHAIN_APPROX_NONE)
    # Find the biggest contour (if detected)
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)
        
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        
        cv2.line(crop_img,(cx,0),(cx,720),(255,0,0),1)
        cv2.line(crop_img,(0,cy),(1280,cy),(255,0,0),1)
        
        cv2.drawContours(crop_img, contours, -1, (0,255,0), 1)
        
        if cx >= 120:
            clbrobot.turnRight(50,0)                 
            print "Turn Left!"
        if cx < 120 and cx > 50:
            clbrobot.t_up(50,0)
            print "On Track!"
        if cx <= 50:
            clbrobot.turnLeft(50,0)   
            print "Turn Right"
    else:
        print "I don't see the line"   
    #Display the resulting frame
    cv2.imshow('frame',crop_img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        clbrobot.t_stop(0)
        GPIO.cleanup()    
        break
