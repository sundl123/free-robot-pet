import cv2
import threading
from queue import Queue


class CameraCapture:
    cap: cv2.VideoCapture = None

    video_width = 0
    video_height = 0

    def __init__(self, src=0, video_width=0, video_height=0):
        self.init_camera_capture(src, video_width, video_height)

        self.q = Queue(maxsize=1)
        self.stop = False
        threading.Thread(target=self.update, args=()).start()

    def init_camera_capture(self, src=0, video_width=0, video_height=0):
        self.cap = cv2.VideoCapture(src)

        original_frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        original_frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print(f'original video size: {original_frame_width}x{original_frame_height}')

        if video_width > 0:
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, video_width)
        if video_height > 0:
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, video_height)

        final_frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        final_frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print(f'final video size: {final_frame_width}x{final_frame_height}')

        self.video_width = final_frame_width
        self.video_height = final_frame_height

    def get_width(self):
        return self.video_width

    def get_height(self):
        return self.video_height

    def update(self):
        while True:
            if self.stop:
                break
            ret, frame = self.cap.read()
            if not ret:
                continue
            if not self.q.empty():
                try:
                    self.q.get_nowait()   # discard previous (unprocessed) frame
                except Queue.Empty:
                    pass
            self.q.put(frame)

    def read(self):
        return self.q.get()

    def release(self):
        self.stop = True
        self.cap.release()


def grab_a_frame_from_camera():
    usb_cap = cv2.VideoCapture(0)
    if not usb_cap.isOpened():
        print("Could not open camera")
        exit()

    frame = None
    skip_frame_number = 100
    for i in range(skip_frame_number):
        ret, frame = usb_cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            exit()
        cv2.imshow('Camera Test', frame)

        # Break the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    usb_cap.release()
    cv2.destroyAllWindows()

    return frame
