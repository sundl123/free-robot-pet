from robot import Robot
from external_apis import common_function
from vision import face, gpt4v

robot_function = {
    "get_current_temperature": common_function["get_current_temperature"],
    "play_music": common_function["play_music"],
    "control_curtain": common_function["control_curtain"],
    "control_light": common_function["control_light"],
    "face_recognition": face.function_description["face_recognition"],
    "tell_me_what_you_see": gpt4v.function_description["tell_me_what_you_see"]
}


class RobotCommandLine(Robot):
    robot_function = robot_function

    def listen(self):
        user_input = input("请输入您的消息（按回车键确认）: ").encode('utf-8').decode('utf-8')
        return user_input

    def speak(self, text):
        print(f'{text}')


