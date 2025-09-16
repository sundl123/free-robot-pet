import base64
import requests
import common
import camera
from config.config import get_config

API_KEY = get_config()["vision"]["gpt4v"]["api_key"]
SECRET_KEY = get_config()["vision"]["gpt4v"]["secret_key"]


def tell_me_what_you_see_wrapper(function_args) -> dict:
    frame = function_args["frame"]
    return tell_me_what_you_see(frame)


def ask_gpt4v_with_image(frame):
    image_base64_str = common.encode_frame_to_jpeg_base64(frame)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "请详细描述图片里面看到的内容"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64_str}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    print(response.json())

    image_description = response.json()['choices'][0]['message']['content']
    return image_description


def tell_me_what_you_see(frame) -> dict:
    image_description = ask_gpt4v_with_image(frame)
    return {'image_description': image_description}


function_description = {
    "tell_me_what_you_see": {
        "implementation": tell_me_what_you_see_wrapper,
        "documentation": {
            'name': 'tell_me_what_you_see',
            'description': "从摄像头抓取 1帧画面，获取画面中内容的文本详细描述",
            'parameters': {
                'type': 'object',
                'properties': {
                    'enable': {
                        'type': 'boolean',
                        'description': "是否执行该函数，请总是设置为 true",
                    },
                },
                'required': [
                    'enable',
                ],
            },
            'responses': {
                'type': 'object',
                'properties': {
                    'image_description': {
                        'type': 'string',
                        'description': "画面内容的详细文本描述信息",
                    },
                },
            },
        },
    }
}
