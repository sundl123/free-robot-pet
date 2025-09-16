import cv2
import time
import os
import base64


def encode_frame_to_jpeg_base64(frame):
    ret, jpeg = cv2.imencode('.jpg', frame)
    if not ret:
        print("encode jpeg failed. Exiting ...")
        exit()

    image_base64_str = str(base64.b64encode(jpeg), encoding='utf-8')

    save_jpeg_to_file(jpeg)

    return image_base64_str


def save_jpeg_to_file(jpeg):
    temp_image_dir = "temp"
    mkdir(temp_image_dir)

    timestamp = int(time.time())
    image_name = f'{temp_image_dir}/frame_{timestamp}.jpg'
    with open(image_name, 'wb') as f:
        f.write(jpeg)


def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")

    is_exists = os.path.exists(path)

    if not is_exists:
        os.makedirs(path)
        return True
    else:
        return False
