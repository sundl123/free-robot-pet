from __future__ import division
import cv2
import time
import Adafruit_PCA9685
import threading
import importlib, sys

importlib.reload(sys)


SUPPORTED_VIDEO_WIDTH = 320
SUPPORTED_VIDEO_HEIGHT = 240


class RobotServoFace:
    camera_capture = None
    running = False

    def __init__(self, camera_capture):
        self.camera_capture = camera_capture

    def start(self):
        self.running = True

        servo_tid = threading.Thread(target=self.start_robot)  # 多线程
        servo_tid.setDaemon(True)
        servo_tid.start()  # 开启线程

    def start_robot(self):
        # 实例化机器人对象
        servo_pwm = Adafruit_PCA9685.PCA9685(busnum=1)  # 实例话舵机云台
        servo_pwm.set_pwm_freq(50)

        # 设置舵机初始值，可以根据自己的要求调试
        servo_pwm.set_pwm(10, 0, 350)  # 底座舵机
        servo_pwm.set_pwm(9, 0, 300)  # 倾斜舵机  420
        time.sleep(1)

        # 初始化摄像头并设置阙值
        usb_cap = self.camera_capture

        # 设置显示的分辨率，设置为320×240 px
        video_width = SUPPORTED_VIDEO_WIDTH
        video_height = SUPPORTED_VIDEO_HEIGHT
        video_center_x = video_width/2
        video_center_y = video_height/2

        # 引入分类器
        face_cascade = cv2.CascadeClassifier('CLBROBOT/face1.xml')

        # 舵机云台的每个自由度需要4个变量
        pid_lastError_x = 0  # 上一次误差值
        pid_lastError_y = 0

        # 舵机的转动角度
        pid_X_P = 325
        pid_Y_P = 350  # 转动角度 420

        # 机器人舵机旋转
        def Robot_servo():
            while self.running:
                servo_pwm.set_pwm(10, 0, 650 - pid_X_P)
                servo_pwm.set_pwm(9, 0, 650 - pid_Y_P)

        servo_tid = threading.Thread(target=Robot_servo)  # 多线程
        servo_tid.setDaemon(True)
        servo_tid.start()  # 开启线程

        # 循环函数
        while self.running:
            frame = usb_cap.read()  # 加载图像
            height, width = frame.shape[:2]
            if height != SUPPORTED_VIDEO_HEIGHT or width != SUPPORTED_VIDEO_WIDTH:
                frame = cv2.resize(frame, (SUPPORTED_VIDEO_WIDTH, SUPPORTED_VIDEO_HEIGHT))
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            faces = face_cascade.detectMultiScale(gray)

            # 找到人脸画矩形
            if len(faces) > 0:
                # calculate face center coordinate
                (pid_x, pid_y, pid_w, pid_h) = faces[0]
                cv2.rectangle(frame, (pid_x, pid_y), (pid_x + pid_h, pid_y + pid_w), (0, 255, 0), 2)
                result = (pid_x, pid_y, pid_w, pid_h)
                pid_x = result[0] + pid_w / 2
                pid_y = result[1] + pid_h / 2

                # 误差值处理
                pid_thisError_x = pid_x - video_center_x
                pid_thisError_y = pid_y - video_center_y

                # 自行对P和D两个值进行调整，检测两个值的变化对舵机稳定性的影响
                k_proportion = 5
                k_derivative = 1
                pwm_x = pid_thisError_x * k_proportion + k_derivative * (pid_thisError_x - pid_lastError_x)
                pwm_y = pid_thisError_y * k_proportion + k_derivative * (pid_thisError_y - pid_lastError_y)

                # 迭代误差值操作
                pid_lastError_x = pid_thisError_x
                pid_lastError_y = pid_thisError_y

                pid_XP = pwm_x / 100
                pid_YP = pwm_y / 100

                # pid_X_P pid_Y_P 为最终PID值
                pid_X_P = pid_X_P - int(pid_XP)
                pid_Y_P = pid_Y_P - int(pid_YP)

                # 限值舵机在一定的范围之内
                if pid_X_P > 670:
                    pid_X_P = 650
                if pid_X_P < 0:
                    pid_X_P = 0
                if pid_Y_P > 650:
                    pid_Y_P = 650
                if pid_X_P < 0:
                    pid_X_P = 0

            # 显示图像
            cv2.imshow("Robot", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()

    def stop(self):
        self.running = False
