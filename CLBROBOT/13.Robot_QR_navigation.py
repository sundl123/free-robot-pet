#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
* @par Copyright (C): 2010-2020, hunan CLB Tech
* @file         13.robot_QR_navigatoin.py
* @version      V2.0
* @details
* @par History

@author: zhulin
"""
import cv2
import numpy as np
import zbar
from PIL import Image
from LOBOROBOT import LOBOROBOT # 载入机器人库
from aip import AipSpeech
import pygame
import  RPi.GPIO as GPIO 
import sys 

if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    
clbrobot=LOBOROBOT()  #  载入机器人库
    
#这里需要填你自己的id和密钥
APP_ID='16226519'
API_KEY='5KVxQVES4LSja0u2G4y8m1O9'
SECRET_KEY='KhaXYwGLSmQYgnwHkuXKpV9MO2ta0bQ8'

aipSpeech=AipSpeech(APP_ID,API_KEY,SECRET_KEY)

def robot_speech(content):
    text=content
    result = aipSpeech.synthesis(text = text, 
                             options={'spd':5,'vol':9,'per':0,})
    if not isinstance(result,dict):
        with open('makerobo.mp3','wb') as f:
            f.write(result)  
    else:print(result)
    #我们利用树莓派自带的pygame
    pygame.mixer.init()
    pygame.mixer.music.load('/home/pi/CLBROBOT/makerobo.mp3')
    pygame.mixer.music.play()


# 智能机器人运动状态
enStop = 0
enRun = 1
enBack = 2
enLeft = 3
enRight = 4
car_State = 0
symbolPos = []

last_qr_data = 'no qrcode'
global qr_data

def draw_rect(img, pos, color, width):
    cv2.line(img, pos[0], pos[1], color, width)
    cv2.line(img, pos[0], pos[3], color, width)
    cv2.line(img, pos[2], pos[1], color, width)
    cv2.line(img, pos[2], pos[3], color, width)

def qr_scan_decode(img):
    global qr_data
    global last_qr_data
    pil= Image.fromarray(img).convert('L')  # gray
    width, height = pil.size
    raw = pil.tobytes()
    zarimage = zbar.Image(width, height, 'Y800', raw)
    scanner_Flag = scanner.scan(zarimage)
    if scanner_Flag == 1:
        for symbol in zarimage:
            if not symbol.count:
                print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data
                symbolPos = symbol.location
                draw_rect(img, symbolPos, (0,255,0), 3)
                qr_data = str(symbol.data)
            else:
                qr_data = 'no qrcode'
    else:
        qr_data = 'no qrcode'
    if last_qr_data != qr_data:       
        command_resolve(qr_data)
    last_qr_data = qr_data

def command_resolve(command):
    last_car_state = 0
    if command.find("Run",0,len(command)) != -1 :
        command.zfill(len(command))
        car_state = 1
    elif command.find("Back",0,len(command)) != -1 :
        command.zfill(len(command))
        car_state = 2
    elif command.find("Left",0,len(command)) != -1 :
        command.zfill(len(command))
        car_state = 3
    elif command.find("Right",0,len(command)) != -1:
        command.zfill(len(command))
        car_state = 4
    elif command.find("Stop",0,len(command)) != -1:            
        command.zfill(len(command))
        car_state = 0
    else:
        car_state = 5
        command.zfill(len(command))
    #print car_state
   
    if last_car_state != car_state :
        car_control(car_state)
    last_car_state = car_state

def car_control(car_state):
    
    if car_state == enRun:
        content='机器人前进'
        robot_speech(content)
        clbrobot.t_up(50,1)         # 前进
    elif car_state == enBack :
        content='机器人后退'
        robot_speech(content)
        clbrobot.t_down(50,1)      # 后退
    elif car_state == enLeft :
        content='机器人左转'
        robot_speech(content)        
        clbrobot.turnLeft(50,1)    # 左转
    elif car_state == enRight :
        content='机器人右转'
        robot_speech(content) 
        clbrobot.turnRight(50,1)   # 右转
    elif car_state == enStop:
        content='机器人停止'
        robot_speech(content) 
        clbrobot.t_stop(0)        # 停止
    else:
        content='机器人停止'
        robot_speech(content) 
        clbrobot.t_stop(0)       # 停止

if __name__ == '__main__':
    # 创建一个QR
    scanner = zbar.ImageScanner()
    # 配置QR
    scanner.parse_config('enable')
    font = cv2.FONT_HERSHEY_SIMPLEX
    # 设置Camera
    cap = cv2.VideoCapture(0)
    if cap.isOpened()==0 :
        print("camera iserror")
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

    while(True):
        grabbed, frame = cap.read()
        if not grabbed:
            break
        qr_scan_decode(frame)
    
    #cv2.putText(frame,symbol.data,(20,100),font,1,(0,255,0),4)
    #print car_state

        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == 27: # 按ESC键退出
            clbrobot.t_stop(0)
            break
# 释放Camera和GPIO
    GPIO.release()
    clbrobot.t_stop(0)
    cap.release()
    cv2.destroyAllWindows()
