#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
    Created on Tue Nov  6 01:18:45 2018
    * @par Copyright (C): 2010-2019, hunan CLB Tech
    * @file        speech-conpound
    * @version      V1.0
    * @details
    * @par History
    
    @author: zhulin
"""
from aip import AipSpeech
import pygame
from time import time
import os

#通过百度云申请的账号和密码
baidu_APP_ID='16226519'
baidu_API_KEY='5KVxQVES4LSja0u2G4y8m1O9'
baidu_SECRET_KEY='KhaXYwGLSmQYgnwHkuXKpV9MO2ta0bQ8'

baidu_aipSpeech=AipSpeech(baidu_APP_ID,baidu_API_KEY,baidu_SECRET_KEY)
#在可选的参数中对语速，音量，人声进行调整，这里采用‘per’为0的女生听起来会更清晰，因人而异！！！
t1=time()
result = baidu_aipSpeech.synthesis(text = '创乐博科技调用语音接口进行语音合成', 
                             options={'spd':5,'vol':9,'per':1,})
#将合成的语音保存为文件
if not isinstance(result,dict):
    with open('makerobo.mp3','wb') as f:
        f.write(result)
        
else:print(result)
#声音播放，我们可以利用树莓派自带的pygame软件
pygame.mixer.init()
pygame.mixer.music.load('/home/pi/CLBROBOT/makerobo.mp3')
pygame.mixer.music.play()

t2=time()
print(t2-t1)