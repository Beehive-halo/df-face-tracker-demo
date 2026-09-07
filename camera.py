import time

from picamera2 import Picamera2

from config import CAMERA_FPS, CAMERA_WARMUP_SECONDS, FRAME_HEIGHT, FRAME_WIDTH


class Camera:
    def __init__(self):
        self.picam2 = Picamera2()

        config = self.picam2.create_video_configuration(
            main={
                "size": (FRAME_WIDTH, FRAME_HEIGHT),
                "format": "RGB888",
            },
            controls={"FrameRate": CAMERA_FPS},
            buffer_count=2,
        )

        self.picam2.configure(config)
        self.picam2.start()
        time.sleep(CAMERA_WARMUP_SECONDS)

    def read(self):
        try:
            return True, self.picam2.capture_array("main")
        except Exception as exc:
            print(f"Camera capture failed: {exc}")
            return False, None

    def release(self):
        try:
            self.picam2.stop()
        except Exception:
            pass
