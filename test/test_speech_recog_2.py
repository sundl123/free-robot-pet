from aip import AipSpeech

# 申请百度语音识别
APP_ID='40452780'
API_KEY='oOOXB8arFDVrnGBGogRiRdfn'
SECRET_KEY='O38Y2dXvcbUdvyy7vYlgtxrPj8LDTgOI'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


# 读取文件
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


# 识别本地文件
file_path = './16k-48000.m4a'
test1 = client.asr(get_file_content(file_path), 'm4a', 16000, {'dev_pid': 1536, })

print(test1)