from aip import AipSpeech
import pygame
import pyaudio
import wave
import time
import numpy as np
from scipy import signal
import RPi.GPIO as GPIO

APP_ID = '40452780'
API_KEY = 'oOOXB8arFDVrnGBGogRiRdfn'
SECRET_KEY = 'O38Y2dXvcbUdvyy7vYlgtxrPj8LDTgOI'

aipSpeech = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


def robot_speech(content):
    text = content
    result = aipSpeech.synthesis(text=text,
                                 options={'spd': 5, 'vol': 5, 'per': 110, })
    if not isinstance(result, dict):
        with open('test-makerobo.mp3', 'wb') as f:
            f.write(result)
    else:
        print(f'error occured during speech synthesis {result}')
        return
    # 我们利用树莓派自带的pygame
    pygame.mixer.init(frequency=16000, channels=1)
    info = pygame.mixer.get_init()
    print("Audio Info:", info)

    pygame.mixer.music.load('./test-makerobo.mp3')
    pygame.mixer.music.play()

    # Wait for the music to finish playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)  # Adjust the tick rate as needed

    # The music has finished playing
    print("Music has finished playing")


def get_audio(filepath):
    CHUNK = 4096  # 定义数据流块
    FORMAT = pyaudio.paInt16  # 量化位数（音量级划分）
    CHANNELS = 1  # 声道数;声道数：可以是单声道或者是双声道
    RATE = 44100  # 采样率;采样率：一秒内对声音信号的采集次数，常用的有8kHz, 16kHz, 32kHz, 48kHz, 11.025kHz, 22.05kHz, 44.1kHz
    RECORD_SECONDS = 10  # 录音秒数
    WAVE_OUTPUT_FILENAME = filepath  # wav文件路径
    p = pyaudio.PyAudio()  # 实例化

    # Find the desired sound card (e.g., card 3) by its name
    desired_card_name = 'USB PnP Sound Device'
    desired_card_index = None

    device_count = p.get_device_count()
    print(f'get_device_count is {device_count}')
    for i in range(device_count):
        device_info = p.get_device_info_by_index(i)
        print(f'device info for {i} is {device_info}')
        if desired_card_name in device_info['name']:
            desired_card_index = i
            break

    if desired_card_index is not None:
        print(f"Using {desired_card_name} (Card {desired_card_index}) for audio input.")
    else:
        print(f"{desired_card_name} not found. Using the default audio input.")

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    input_device_index=desired_card_index,
                    frames_per_buffer=CHUNK)
    # print("*"*10, "开始录音：请在5秒内输入语音")
    frames = []  # 定义一个列表
    TARGET_SAMPLE_RATE = 16000  # Desired sample rate (8kHz)
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):  # 循环，采样率11025 / 256 * 5
        data = stream.read(CHUNK)
        audio_data = np.frombuffer(data, dtype=np.int16)
        resampled_audio = resample_audio(audio_data, RATE, TARGET_SAMPLE_RATE)

        resampled_data = resampled_audio.astype(np.int16).tobytes()
        frames.append(resampled_data)  # Append resampled data to frames

    stream.stop_stream()
    stream.close()  # 关闭
    p.terminate()  # 终结

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')  # 打开wav文件创建一个音频对象wf，开始写WAV文件
    wf.setnchannels(CHANNELS)  # 配置声道数
    wf.setsampwidth(p.get_sample_size(FORMAT))  # 配置量化位数
    wf.setframerate(TARGET_SAMPLE_RATE)  # 配置采样率
    wf.writeframes(b''.join(frames))  # 转换为二进制数据写入文件
    wf.close()  # 关闭

def resample_audio(audio_data, original_rate, target_rate):
    # Calculate the resampling ratio
    ratio = float(target_rate) / original_rate

    # Use scipy.signal.resample to resample the audio data
    resampled_audio = signal.resample(audio_data, int(len(audio_data) * ratio))

    return resampled_audio

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


def robot_speech_recog(audio_file_path):
    result = aipSpeech.asr(get_file_content(audio_file_path), 'wav', 16000, {'dev_pid': 1536, })
    if result["err_no"] == 0:
        return result["result"]
    else:
        print(f'speech recognition failed, result: {result}')
        return ""


def run_once():
    audio_file_path = "test-audio_input.wav"
    get_audio(audio_file_path)

    recog_text = robot_speech_recog(audio_file_path)
    if recog_text == "":
        print("empty recog result, skip now")
        exit()
    print(f'recog result is {recog_text}')

    content = "接下来我会重复你所说的话"
    robot_speech(content)
    time.sleep(2)

    robot_speech(recog_text)

BtnPin = 19
Gpin = 5
Rpin = 6


def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)  # Numbers GPIOs by physical location
    GPIO.setup(Gpin, GPIO.OUT)  # Set Green Led Pin mode to output
    GPIO.setup(Rpin, GPIO.OUT)  # Set Red Led Pin mode to output
    GPIO.setup(BtnPin, GPIO.IN,
               pull_up_down=GPIO.PUD_UP)  # Set BtnPin's mode is input, and pull up to high level(3.3V)


def run_with_button():
    setup()
    try:
        while True:
            if GPIO.input(BtnPin):  # button state is normal
                time.sleep(0.01)
                if GPIO.input(BtnPin):
                    GPIO.output(Rpin, 1)
                    GPIO.output(Gpin, 0)
                    print("now start recording")
                    run_once()
            elif not GPIO.input(BtnPin):  # button is pressed
                time.sleep(0.01)
                if not GPIO.input(BtnPin):
                    while GPIO.input(BtnPin):
                        pass
                    GPIO.output(Rpin, 0)
                    GPIO.output(Gpin, 1)
                    # stop audio recording
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        GPIO.cleanup()


if __name__ == '__main__':
    run_with_button()
