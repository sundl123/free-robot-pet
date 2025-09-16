import base64
from aip import AipFace
import common
import camera
from config.config import get_config

APP_ID = get_config()["vision"]["face"]["app_id"]
API_KEY = get_config()["vision"]["face"]["api_key"]
SECRET_KEY = get_config()["vision"]["face"]["secret_key"]
FACE_DB = get_config()["vision"]["face"]["face_db"]
SIMILARITY_THRESH = get_config()["vision"]["face"]["similarity_thresh"]


def face_recognition_wrapper(function_args) -> dict:
    frame = function_args["frame"]
    return face_recognition(frame)


def search_face_with_image(frame):
    image_base64_str = common.encode_frame_to_jpeg_base64(frame)

    client = AipFace(APP_ID, API_KEY, SECRET_KEY)

    options = {"match_threshold": SIMILARITY_THRESH}
    result = client.search(image_base64_str, image_type='BASE64', group_id_list=FACE_DB, options=options)
    print(f'search_face_with_image result: {result}')

    if result['error_msg'] == "SUCCESS":
        face_list = result['result']['user_list']
        face_id = face_list[0]['user_id']
        return face_id

    return "unknown"


def face_recognition(frame) -> dict:
    face_id = search_face_with_image(frame)
    return {'face_id': face_id}


function_description = {
    "face_recognition": {
        "implementation": face_recognition_wrapper,
        "documentation": {
            'name': 'face_recognition',
            'description': "从摄像头获取 1帧画面，进行人脸检测与识别，返回人脸识别结果。当用户咨询以下问题的时候，建议你调用这个函数,示例问题: 1. 你知道我是谁吗? 2. 看看我是谁 3. 你认得我吗? ”",
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
                    'face_id': {
                        'type': 'string',
                        'description': "人脸的 id，如果没有检测到任何人脸，返回 空字符；如果检测到人脸，但是识别失败，返回 unknown",
                    },
                },
            },
        },
    }
}
