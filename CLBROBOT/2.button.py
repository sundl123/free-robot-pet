#!/usr/bin/env python
"""
* @par Copyright (C): 2010-2020, hunan CLB Tech
* @file         button
* @version      V2.0
* @details
* @par History

@author: zhulin
"""
import RPi.GPIO as GPIO
import time

BtnPin = 19
Gpin    = 5
Rpin    = 6

def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)       # Numbers GPIOs by physical location
    GPIO.setup(Gpin, GPIO.OUT)     # Set Green Led Pin mode to output
    GPIO.setup(Rpin, GPIO.OUT)     # Set Red Led Pin mode to output
    GPIO.setup(BtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Set BtnPin's mode is input, and pull up to high level(3.3V) 

    
if __name__ == '__main__':     # Program start from here
    setup()
    try:
        while True:
            if GPIO.input(BtnPin) == True:
                time.sleep(0.01)
                if GPIO.input(BtnPin)==True:
                    GPIO.output(Rpin,1)
                    GPIO.output(Gpin,0)
            elif GPIO.input(BtnPin) == False:
                 time.sleep(0.01)
                 if  GPIO.input(BtnPin) == False:
                    while GPIO.input(BtnPin) ==True:
                        pass
                    GPIO.output(Rpin,0)
                    GPIO.output(Gpin,1)                                              
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        GPIO.cleanup()


