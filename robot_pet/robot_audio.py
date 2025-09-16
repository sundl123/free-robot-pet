import audio
from robot import Robot
from external_apis import common_function
from wakeup.wakeup import wait_for_wakeup

robot_function = {
    "get_current_temperature": common_function["get_current_temperature"],
    "play_music": common_function["play_music"],
    "control_curtain": common_function["control_curtain"],
    "control_light": common_function["control_light"],
}


class RobotAudio(Robot):
    robot_function = robot_function

    def listen(self):
        user_input = audio.get_user_input_from_audio()
        print(user_input)
        return user_input

    def speak(self, text):
        audio.robot_speech(text)

    def wakeup(self):
        wait_for_wakeup()
        print("this robot has waken up")
