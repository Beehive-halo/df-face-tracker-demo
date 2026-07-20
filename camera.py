import cv2

from config import *


class Camera:

    def __init__(self):

        if USE_PI_CAMERA:

            self.cap = cv2.VideoCapture(
                CAMERA_INDEX,
                cv2.CAP_V4L2
            )

        else:

            self.cap = cv2.VideoCapture(
                CAMERA_INDEX
            )

        self.cap.set(
            cv2.CAP_PROP_FRAME_WIDTH,
            FRAME_WIDTH
        )

        self.cap.set(
            cv2.CAP_PROP_FRAME_HEIGHT,
            FRAME_HEIGHT
        )

    def read(self):

        return self.cap.read()

    def release(self):

        self.cap.release()
