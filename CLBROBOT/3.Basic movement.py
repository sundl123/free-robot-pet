#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
* @par Copyright (C): 2010-2020, hunan CLB Tech
* @file         Basic_movement
* @version      V2.0
* @details
* @par History

@author: zhulin
"""
from LOBOROBOT import LOBOROBOT  # 载入机器人库
import RPi.GPIO as GPIO

import importlib,sys
importlib.reload(sys)

if __name__ == "__main__":
    clbrobot = LOBOROBOT() # 实例化机器人对象
    try:
        while True:
            clbrobot.t_up(50,3)      # 机器人前进
            clbrobot.t_stop(1) # 机器人停止
            clbrobot.t_down(50,3)    # 机器人后退
            clbrobot.t_stop(1) # 机器人停止
            clbrobot.turnLeft(50,3)  # 机器人左转
            clbrobot.t_stop(1) # 机器人停止
            clbrobot.turnRight(50,3) # 机器人右转
            clbrobot.t_stop(1) # 机器人停止
            clbrobot.moveLeft(50,3)  # 机器人左移
            clbrobot.t_stop(1) # 机器人停止
            clbrobot.moveRight(50,3) # 机器人右移
            clbrobot.t_stop(1) # 机器人停止
            clbrobot.forward_Left(50,3) # 机器人前左斜
            clbrobot.t_stop(1) # 机器人停止
            clbrobot.backward_Right(50,3) # 机器人后右斜
            clbrobot.t_stop(1) # 机器人停止
            clbrobot.forward_Right(50,3)  # 机器人前右斜
            clbrobot.t_stop(1) # 机器人停止
            clbrobot.backward_Left(50,3)  # 机器人后左斜
            clbrobot.t_stop(5)       # 机器人停止            
    except KeyboardInterrupt:
        clbrobot.t_stop(0) # 机器人停止
        GPIO.cleanup()

