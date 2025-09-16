import unittest


def image_to_base64(image_path):
    import base64
    with open(image_path, 'rb') as f:
        image = base64.b64encode(f.read())
        return str(image, encoding='utf-8')


def search_face_image(client, image_path):
    image = image_to_base64(image_path)

    options = {"match_threshold": 80}
    result = client.search(image, image_type='BASE64', group_id_list="family_member", options=options)
    print(result)
    return result


def face_search(self):
    from aip import AipFace

    APP_ID = '44345325'
    API_KEY = 'stS0fSWFIiqlPvykn3dZa9Io'
    SECRET_KEY = 'BxmKYGIf0DNYoGQw9HGrW1Qw7dW5Pqyy'

    client = AipFace(APP_ID, API_KEY, SECRET_KEY)

    result = search_face_image(client, 'test_gpt4v_dog.png')
    self.assertEqual(result['error_msg'], 'match user is not found')

    result = search_face_image(client, 'test_baidu_face_man.png')
    self.assertEqual(result['error_msg'], 'SUCCESS')


class TestBaiduFaceService(unittest.TestCase):
    def test_face_search(self):
        face_search(self)


if __name__ == '__main__':
    unittest.main()
