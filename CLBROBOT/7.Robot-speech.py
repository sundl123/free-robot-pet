#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
    Created on Tue Nov  6 01:18:45 2018
    * @par Copyright (C): 2010-2019, hunan CLB Tech
    * @file        7.Robot-speech.py
    * @version      V1.0
    * @details
    * @par History
    
    @author: zhulin
"""
from aip import AipSpeech
import pygame
from LOBOROBOT import LOBOROBOT # 载入机器人库
import  RPi.GPIO as GPIO
import time
import os
import sys

reload(sys)
sys.setdefaultencoding('utf8')

# 按键及LED初始化
BtnPin  = 19
Gpin    = 5
Rpin    = 6

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

#初始化舵机
clbrobot = LOBOROBOT()  # 实例化机器人对象

# Configure min and max servo pulse lengths
servo_min = 150  # Min pulse length out of 4096
servo_max = 600  # Max pulse length out of 4096

# 频率设置为50hz，适用于舵机系统。
clbrobot.set_servo_angle(10,90)  # 底座舵机
clbrobot.set_servo_angle(9,90)  # 顶部舵机

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
 

try:
    keysacn() # 键盘控制函数
    content='下面运行创乐博AI智能机器人演示程序'
    robot_speech(content)  
    time.sleep(6)
    content='机器人前进'
    robot_speech(content)
    clbrobot.t_up(50,3) # 机器人前进
    clbrobot.t_stop(1) # 机器人停止
    content='机器人后退'
    robot_speech(content)
    clbrobot.t_down(50,3) # 机器人后退
    clbrobot.t_stop(1) # 机器人停止
    content='机器人左转'
    robot_speech(content)   
    clbrobot.turnLeft(50,3)
    clbrobot.t_stop(1) # 机器人停止
    content='机器人右转'
    robot_speech(content)     
    clbrobot.turnRight(50,3)
    clbrobot.t_stop(1) # 机器人停止
    content='机器人左移'
    robot_speech(content) 
    clbrobot.moveLeft(50,3)
    clbrobot.t_stop(1) # 机器人停止

    content='机器人右移'
    robot_speech(content) 
    clbrobot.moveRight(50,3)
    clbrobot.t_stop(1) # 机器人停止
    
    content='机器人前左斜'
    robot_speech(content) 
    clbrobot.forward_Left(50,3)
    clbrobot.t_stop(1) # 机器人停止
    
    content='机器人后右斜'
    robot_speech(content) 
    clbrobot.backward_Right(50,3)
    clbrobot.t_stop(1) # 机器人停止
    
    content='机器人前右斜'
    robot_speech(content) 
    clbrobot.forward_Right(50,3)
    clbrobot.t_stop(1) # 机器人停止
    
    content='机器人后左斜'
    robot_speech(content) 
    clbrobot.backward_Left(50,3)
    clbrobot.t_stop(1) # 机器人停止
    
    content='机器人停止'
    robot_speech(content)     
    clbrobot.t_stop(3)
    
except KeyboardInterrupt:
    clbrobot.t_stop(0)
    GPIO.cleanup()
