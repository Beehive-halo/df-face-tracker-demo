import cv2
from config import FRAME_WIDTH, FRAME_HEIGHT


class Camera:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    def read(self):
        return self.cap.read()

    def release(self):
        self.cap.release()
