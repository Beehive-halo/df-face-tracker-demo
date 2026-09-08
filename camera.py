import time

from libcamera import Transform
from picamera2 import Picamera2

from config import (
    CAMERA_FPS,
    CAMERA_HFLIP,
    CAMERA_READ_ATTEMPTS,
    CAMERA_RETRY_SECONDS,
    CAMERA_VFLIP,
    CAMERA_WARMUP_SECONDS,
    FRAME_HEIGHT,
    FRAME_WIDTH,
)


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
            transform=Transform(
                hflip=CAMERA_HFLIP,
                vflip=CAMERA_VFLIP,
            ),
        )

        self.picam2.configure(config)
        self.picam2.start()
        time.sleep(CAMERA_WARMUP_SECONDS)

    def read(self):
        last_error = None

        for attempt in range(CAMERA_READ_ATTEMPTS):
            try:
                return True, self.picam2.capture_array("main")
            except Exception as exc:
                last_error = exc
                if attempt + 1 < CAMERA_READ_ATTEMPTS:
                    time.sleep(CAMERA_RETRY_SECONDS)

        print(f"Camera capture failed after {CAMERA_READ_ATTEMPTS} attempts: {last_error}")
        return False, None

    def release(self):
        try:
            self.picam2.stop()
        except Exception:
            pass
