from picamera2 import Picamera2
import cv2
import time

from config import FRAME_WIDTH, FRAME_HEIGHT


class Camera:

    def __init__(self):

        self.picam2 = Picamera2()

        config = self.picam2.create_preview_configuration(
            main={
                "size": (FRAME_WIDTH, FRAME_HEIGHT),
                "format": "RGB888"
            }
        )

        self.picam2.configure(config)
        self.picam2.start()

        # Allow camera to warm up
        time.sleep(1)

    def read(self):

        try:
            frame = self.picam2.capture_array()

            # Picamera2 returns RGB, OpenCV expects BGR
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            return True, frame

        except Exception as e:
            print(f"Camera Error: {e}")
            return False, None

    def release(self):

        self.picam2.stop()
