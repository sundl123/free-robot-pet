import time
import os
import subprocess
from config.config import get_config


def get_current_temperature(location: str, unit: str) -> dict:
    return {'temperature': 25, 'unit': '摄氏度'}


def get_current_temperature_wrapper(function_args) -> dict:
    return get_current_temperature(location=function_args['location'], unit=function_args['unit'])


def control_light_wrapper(function_args) -> dict:
    return control_light(on=function_args['on'])


def control_light(on: bool) -> dict:
    mock = get_config()["miiot"]["mock"]
    ip = get_config()["miiot"]["light"]["ip"]
    token = get_config()["miiot"]["light"]["token"]

    cmd_str = f'miiocli yeelight --ip {ip} --token {token}'

    if on:
        cmd_str = f'{cmd_str} on'
    else:
        cmd_str = f'{cmd_str} off'

    if mock:
        print(f'mock execute: {cmd_str}')
        return {"is_successful": True}

    print(f'executing command: \"{cmd_str}\"')
    completed_process = subprocess.run(cmd_str, shell=True, capture_output=True, text=True)
    output = completed_process.stdout
    return_code = completed_process.returncode

    if return_code != 0 or "Error" in output:
        print(f'Return code: {return_code}, Output of the command: {output}')
        return {"is_successful": False}

    return {"is_successful": True}


def control_curtain_wrapper(function_args) -> dict:
    return control_curtain(open_the_curtain=function_args['open_the_curtain'])


def control_curtain(open_the_curtain: bool) -> dict:
    mock = get_config()["miiot"]["mock"]

    ip = get_config()["miiot"]["curtain_white"]["ip"]
    token = get_config()["miiot"]["curtain_white"]["token"]
    is_successful = control_one_curtain(mock, ip, token, open_the_curtain)
    if not is_successful:
        return {"is_successful": False}

    ip = get_config()["miiot"]["curtain_gray"]["ip"]
    token = get_config()["miiot"]["curtain_gray"]["token"]
    control_one_curtain(mock, ip, token, open_the_curtain)
    if not is_successful:
        return {"is_successful": False}

    return {"is_successful": True}


def control_one_curtain(mock: bool, ip: str, token: str, open_the_curtain: bool) -> bool:
    cmd_str = f'miiocli curtainmiot --ip {ip} --token {token}'

    if open_the_curtain:
        cmd_str = f'{cmd_str} set_motor_control open'
    else:
        cmd_str = f'{cmd_str} set_motor_control close'

    if mock:
        print(f'mock execute: {cmd_str}')
        return True

    print(f'executing command: \"{cmd_str}\"')
    completed_process = subprocess.run(cmd_str, shell=True, capture_output=True, text=True)
    output = completed_process.stdout
    return_code = completed_process.returncode

    if return_code != 0 or "Error" in output:
        print(f'Return code: {return_code}, Output of the command: {output}')
        return False

    return True


def play_music_wrapper(function_args) -> dict:
    return play_music(chatbot=function_args['chatbot'], on=function_args['on'])


def play_music(chatbot, on) -> dict:
    chatbot.speak("小爱同学")
    time.sleep(1)

    if on:
        chatbot.speak("播放音乐")
    else:
        chatbot.speak("关闭音乐")
    time.sleep(2)

    return {"is_successful": True}


common_function = {
    "get_current_temperature": {
        "implementation": get_current_temperature_wrapper,
        "documentation": {
            'name': 'get_current_temperature',
            'description': "获取指定城市的气温",
            'parameters': {
                'type': 'object',
                'properties': {
                    'location': {
                        'type': 'string',
                        'description': "城市名称",
                    },
                    'unit': {
                        'type': 'string',
                        'enum': [
                            '摄氏度',
                            '华氏度',
                        ],
                    },
                },
                'required': [
                    'location',
                    'unit',
                ],
            },
            'responses': {
                'type': 'object',
                'properties': {
                    'temperature': {
                        'type': 'integer',
                        'description': "城市气温",
                    },
                    'unit': {
                        'type': 'string',
                        'enum': [
                            '摄氏度',
                            '华氏度',
                        ],
                    },
                },
            },
        },
    },
    "play_music": {
        "implementation": play_music_wrapper,
        "documentation": {
            'name': 'play_music',
            'description': "控制智能音箱开启/关闭音乐的播放",
            'parameters': {
                'type': 'object',
                'properties': {
                    'on': {
                        'type': 'boolean',
                        'description': "是否播放音乐，设置为True为播放音乐，设置为False为关闭音乐",
                    },
                },
                'required': [
                    'on',
                ],
            },
            'responses': {
                'type': 'object',
                'properties': {
                    'is_successful': {
                        'type': 'boolean',
                        'description': "操作是否执行成功，True代表成功,False代表失败",
                    },
                },
            },
        },
    },
    "control_light": {
        "implementation": control_light_wrapper,
        "documentation": {
            'name': 'control_light',
            'description': "通过智能家居控制台灯的打开与关闭",
            'parameters': {
                'type': 'object',
                'properties': {
                    'on': {
                        'type': 'boolean',
                        'description': "是否打开台灯，设置为True为打开台灯，设置为False为关闭台灯",
                    },
                },
                'required': [
                    'on',
                ],
            },
            'responses': {
                'type': 'object',
                'properties': {
                    'is_successful': {
                        'type': 'boolean',
                        'description': "操作是否执行成功，True代表成功,False代表失败",
                    },
                },
            },
        },
    },
    "control_curtain": {
        "implementation": control_curtain_wrapper,
        "documentation": {
            'name': 'control_curtain',
            'description': "通过智能家居控制客厅窗帘的打开与关闭",
            'parameters': {
                'type': 'object',
                'properties': {
                    'open_the_curtain': {
                        'type': 'boolean',
                        'description': "是否打开窗帘，设置为True为打开窗帘，设置为False为关闭窗帘",
                    },
                },
                'required': [
                    'open',
                ],
            },
            'responses': {
                'type': 'object',
                'properties': {
                    'is_successful': {
                        'type': 'boolean',
                        'description': "控制窗帘的指令是否成功，True代表成功,False代表失败",
                    },
                },
            },
        },
    },
}
