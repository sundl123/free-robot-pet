from snowboydecoder import play_audio_file, HotwordDetector
import os
from config.config import get_config

MODEL_NAME = get_config()["voice_wakeup"]["model_name"]

# import model file by arch
import platform
system = platform.system()
print(f'running on system {system}')
if system == "Darwin":
    model_file = f'arch/darwin/{MODEL_NAME}'
else:
    model_file = f'arch/rasperry_pi_4b/{MODEL_NAME}'
top_dir = os.path.dirname(os.path.abspath(__file__))
model = os.path.join(top_dir, model_file)


interrupted = False


def detect_callback():
    global interrupted
    interrupted = True

    play_audio_file()


def interrupt_callback():
    global interrupted
    return interrupted


def wait_for_wakeup():
    global interrupted
    interrupted = False

    detector = HotwordDetector(model, sensitivity=0.5)

    # main loop
    try:
        print('Listening... ')
        detector.start(detected_callback=detect_callback,
                       interrupt_check=interrupt_callback,
                       sleep_time=0.03)
        print("hot word is detected, wake up now")
    except KeyboardInterrupt:
        interrupted = True
        detector.terminate()
        raise KeyboardInterrupt

    detector.terminate()
