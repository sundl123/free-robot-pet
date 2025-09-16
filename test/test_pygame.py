"""
Created on Mon Jun 24 14:47:35 2019

@author: erio
"""
import pyaudio
import wave


#录音
input_filename = "record.wav"  # 麦克风采集的语音输入
input_filepath = "./"  # 输入文件的path
in_pathrec = input_filepath + input_filename         #通俗解释就是wav文件路径

def get_audio(filepath):
        CHUNK = 256                 #定义数据流块
        FORMAT = pyaudio.paInt16    #量化位数（音量级划分）
        CHANNELS = 1               # 声道数;声道数：可以是单声道或者是双声道
        RATE = 16000                # 采样率;采样率：一秒内对声音信号的采集次数，常用的有8kHz, 16kHz, 32kHz, 48kHz, 11.025kHz, 22.05kHz, 44.1kHz
        RECORD_SECONDS = 10          #录音秒数
        WAVE_OUTPUT_FILENAME = filepath     #wav文件路径
        p = pyaudio.PyAudio()               #实例化

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
       # print("*"*10, "开始录音：请在5秒内输入语音")
        frames = []                                                 #定义一个列表
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):      #循环，采样率11025 / 256 * 5
            data = stream.read(CHUNK)                               #读取chunk个字节 保存到data中
            frames.append(data)                                     #向列表frames中添加数据data
      #  print(frames)
      #  print("*" * 10, "录音结束\n")

        stream.stop_stream()
        stream.close()          #关闭
        p.terminate()           #终结

        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')                  #打开wav文件创建一个音频对象wf，开始写WAV文件
        wf.setnchannels(CHANNELS)                                   #配置声道数
        wf.setsampwidth(p.get_sample_size(FORMAT))                  #配置量化位数
        wf.setframerate(RATE)                                       #配置采样率
        wf.writeframes(b''.join(frames))                            #转换为二进制数据写入文件
        wf.close()              #关闭

get_audio(in_pathrec)