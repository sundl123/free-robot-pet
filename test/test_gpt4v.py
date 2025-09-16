import unittest

api_key = "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"
secret_key = "pangpang"


def analyse_single_image_by_url():
    from openai import OpenAI

    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "请详细描述图片里面看到的内容"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg",
                        },
                    },
                ],
            }
        ],
        max_tokens=300,
    )

    print(response.choices[0])


def analyse_single_image_by_base64():
    import base64
    import requests

    # Function to encode the image
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    # Path to your image
    image_path = "./test_gpt4v_dog.png"

    # Getting the base64 string
    base64_image = encode_image(image_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
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
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    print(response.json())
    print(response)


class TestGPT4V(unittest.TestCase):
    def test_analyse_single_image_by_url(self):
        analyse_single_image_by_url()

    def test_analyse_single_image_by_base64(self):
        analyse_single_image_by_base64()


if __name__ == '__main__':
    unittest.main()
