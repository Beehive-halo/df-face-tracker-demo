from picamera2 import Picamera2
import cv2
import time

from config import *


class Camera:

    def __init__(self):

        self.camera = Picamera2()

        config = self.camera.create_preview_configuration(
            main={
                "size": (FRAME_WIDTH, FRAME_HEIGHT),
                "format": "RGB888"
            }
        )

        self.camera.configure(config)

        self.camera.start()

        time.sleep(2)

    def read(self):

        frame = self.camera.capture_array()

        frame = cv2.cvtColor(
            frame,
            cv2.COLOR_RGB2BGR
        )

        return True, frame

    def release(self):

        self.camera.stop()
