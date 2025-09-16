from robot import Robot
import audio
import RPi.GPIO as GPIO
from LOBOROBOT import LOBOROBOT
from wakeup.wakeup import wait_for_wakeup
from external_apis import common_function
from vision import face, gpt4v


def control_robot_action_wrapper(function_args) -> dict:
    return control_robot_action(action=function_args['action'])


def control_robot_action(action: str) -> dict:
    print(f'robot is taking an actions: {action}')

    clbrobot = LOBOROBOT()  # 实例化机器人对象
    if action == "前进":
        clbrobot.t_up(50, 3)  # 机器人前进
        clbrobot.t_stop(1)  # 机器人停止
    elif action == "后退":
        clbrobot.t_down(50, 3)  # 机器人后退
        clbrobot.t_stop(1)  # 机器人停止
    elif action == "左转":
        clbrobot.turnLeft(50, 3)  # 机器人左转
        clbrobot.t_stop(1)  # 机器人停止
    elif action == "右转":
        clbrobot.turnRight(50, 3)  # 机器人右转
        clbrobot.t_stop(1)  # 机器人停止
    elif action == "左移":
        clbrobot.moveLeft(50, 3)  # 机器人左移
        clbrobot.t_stop(1)  # 机器人停止
    elif action == "右移":
        clbrobot.moveRight(50, 3)  # 机器人右移
        clbrobot.t_stop(1)  # 机器人停止
    elif action == "前左斜":
        clbrobot.forward_Left(50, 3)  # 机器人前左斜
        clbrobot.t_stop(1)  # 机器人停止
    elif action == "后右斜":
        clbrobot.backward_Right(50, 3)  # 机器人后右斜
        clbrobot.t_stop(1)  # 机器人停止
    elif action == "前右斜":
        clbrobot.forward_Right(50, 3)  # 机器人前右斜
        clbrobot.t_stop(1)  # 机器人停止
    elif action == "后左斜":
        clbrobot.backward_Left(50, 3)  # 机器人后左斜
        clbrobot.t_stop(5)  # 机器人停止
    else:
        print(f'invalid actions: {action}')
        return {"is_successful": False}

    clbrobot.t_stop(0)  # 机器人停止
    GPIO.cleanup()

    return {"is_successful": True}


robot_function = {
    "get_current_temperature": common_function["get_current_temperature"],
    "play_music": common_function["play_music"],
    "control_curtain": common_function["control_curtain"],
    "control_light": common_function["control_light"],
    "face_recognition": face.function_description["face_recognition"],
    "tell_me_what_you_see": gpt4v.function_description["tell_me_what_you_see"],
    "control_robot_action": {
        "implementation": control_robot_action,
        "documentation": {
            'name': 'control_robot_action',
            'description': "控制机器人的移动",
            'parameters': {
                'type': 'object',
                'properties': {
                    'action': {
                        'type': 'string',
                        'description': "动作类型",
                        'enum': [
                            '前进',
                            '后退',
                            '左转',
                            '右转',
                            '左移',
                            '右移',
                            '前左斜',
                            '后右斜',
                            '前右斜',
                            '后左斜',
                        ],
                    },
                },
                'required': [
                    'action',
                ],
            },
            'responses': {
                'type': 'object',
                'properties': {
                    'is_successful': {
                        'type': 'boolean',
                        'description': "机器是否成功执行动作",
                    },
                },
            },
        },
    }
}

BtnPin = 19
Gpin = 5
Rpin = 6

from vision.robot_servo_face import RobotServoFace


class RobotCar(Robot):
    robot_function = robot_function
    robot_servo = None
    camera_capture = None

    def setup(self):
        print("setup up a robot")
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)  # Numbers GPIOs by physical location
        GPIO.setup(Gpin, GPIO.OUT)  # Set Green Led Pin mode to output
        GPIO.setup(Rpin, GPIO.OUT)  # Set Red Led Pin mode to output
        GPIO.setup(BtnPin, GPIO.IN,
                   pull_up_down=GPIO.PUD_UP)  # Set BtnPin's mode is input, and pull up to high level(3.3V)

    def listen(self):
        user_input = audio.get_user_input_from_audio()
        return user_input

    def speak(self, text):
        audio.robot_speech(text)

    def wakeup(self):
        wait_for_wakeup()
        from vision.camera import CameraCapture
        self.camera_capture = CameraCapture()

        self.robot_servo = RobotServoFace(self.camera_capture)
        self.robot_servo.start()

        print("this robot has waken up")

    def sleep(self):
        self.robot_servo.stop()
        self.robot_servo = None

        self.camera_capture.release()
        self.camera_capture = None

        print("this robot has been put to sleep")

    def process_function_call(self, function_name, function_args):
        print(f'process function call, {function_name}, {function_args}')
        func = self.robot_function[function_name]["implementation"]

        if function_name == "play_music":
            function_args['chatbot'] = self
        elif function_name == "face_recognition":
            function_args['frame'] = self.camera_capture.read()
        elif function_name == "tell_me_what_you_see":
            function_args['frame'] = self.camera_capture.read()

        res = func(function_args)

        return res

    def cleanup(self):
        print("clean up a robot")
        GPIO.cleanup()
