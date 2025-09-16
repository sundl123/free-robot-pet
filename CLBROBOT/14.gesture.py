#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
* @par Copyright (C): 2010-2019, hunan CLB Tech
* @file         11.gesture.py
* @version      V1.0
* @details
* @par History

@author: zhulin
"""
import cv2
import numpy as np
import math

cap = cv2.VideoCapture(0)

# 将视频尺寸减小到300x300，这样rpi处理速度就会更快
cap.set(3,320)
cap.set(4,320)
    
while(1):
        
    try:  # 如果它在窗口中找不到任何东西，因为找不到最大面积的轮廓，就会出现错误
          # 因此，此try错误语句
          
        ret, frame = cap.read()
        frame=cv2.flip(frame,1)
        kernel = np.ones((3,3),np.uint8)
        
        # 定义感兴趣的区域
        roi=frame[0:300, 0:300]
        
        
        cv2.rectangle(frame,(0,0),(300,300),(0,255,0),0)    
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        
        
         
    # 定义HSV中肤色的范围
        lower_skin = np.array([0,20,70], dtype=np.uint8)
        upper_skin = np.array([20,255,255], dtype=np.uint8)
        
     # 提取肤色图像 
        mask = cv2.inRange(hsv, lower_skin, upper_skin)
        
   
        
    # 外推手以填补其中的黑点
        mask = cv2.dilate(mask,kernel,iterations = 4)
        
    # 高斯模糊
        mask = cv2.GaussianBlur(mask,(5,5),100) 
        
        
        
    # 找到轮廓
        _,contours,hierarchy= cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
   # 找到最大面积的轮廓（手）
        cnt = max(contours, key = lambda x: cv2.contourArea(x))
        
    # 大概轮廓
        epsilon = 0.0005*cv2.arcLength(cnt,True)
        approx= cv2.approxPolyDP(cnt,epsilon,True)
       
        
    # 围绕手做凸包
        hull = cv2.convexHull(cnt)
        
     #define area of hull and area of hand
        areahull = cv2.contourArea(hull)
        areacnt = cv2.contourArea(cnt)
      
    # 查找凸包中未被手覆盖的区域的百分比
        arearatio=((areahull-areacnt)/areacnt)*100
    
     # 发现凸包相对于手的缺陷
        hull = cv2.convexHull(approx, returnPoints=False)
        defects = cv2.convexityDefects(approx, hull)
        
    # l = no. of defects
        l=0
        
    # 查找编号的代码 手指造成的缺陷
        for i in range(defects.shape[0]):
            s,e,f,d = defects[i,0]
            start = tuple(approx[s][0])
            end = tuple(approx[e][0])
            far = tuple(approx[f][0])
            pt= (100,180)
            
            
            # 求出三角形所有边的长度
            a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
            b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
            c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
            s = (a+b+c)/2
            ar = math.sqrt(s*(s-a)*(s-b)*(s-c))
            
            # 点与凸包之间的距离
            d=(2*ar)/a
            
            # 在这里应用余弦规则
            angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57
            
        
            # 忽略大于90度的角度并忽略非常靠近凸包的点（它们通常是由于噪声而来）
            if angle <= 90 and d>30:
                l += 1
                cv2.circle(roi, far, 3, [255,0,0], -1)
            
            # 在手周围画线
            cv2.line(roi,start, end, [0,255,0], 2)
            
            
        l+=1
        
        # 打印范围内的相应手势
        font = cv2.FONT_HERSHEY_SIMPLEX
        if l==1:
            if areacnt<2000:
                cv2.putText(frame,'Put hand in the box',(0,50), font, 1, (0,0,255), 3, cv2.LINE_AA)
            else:
                if arearatio<12:
                    cv2.putText(frame,'0',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
                elif arearatio<17.5:
                    cv2.putText(frame,'Best of luck',(0,50), font, 1, (0,0,255), 3, cv2.LINE_AA)
                   
                else:
                    cv2.putText(frame,'1',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
                    
        elif l==2:
            cv2.putText(frame,'2',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
            
        elif l==3:
         
              if arearatio<27:
                    cv2.putText(frame,'3',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
              else:
                    cv2.putText(frame,'ok',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
                    
        elif l==4:
            cv2.putText(frame,'4',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
            
        elif l==5:
            cv2.putText(frame,'5',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
            
        elif l==6:
            cv2.putText(frame,'reposition',(0,50), font, 1, (0,0,255), 3, cv2.LINE_AA)
            
        else :
            cv2.putText(frame,'reposition',(10,50), font, 1, (0,0,255), 3, cv2.LINE_AA)
            
        # 显示窗户
        cv2.imshow('mask',mask)
        cv2.imshow('frame',frame)
    except:
        pass
        
    
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
    
cv2.destroyAllWindows()
cap.release()    
    




