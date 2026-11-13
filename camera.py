import time

from libcamera import Transform
from picamera2 import Picamera2

from config import (
    CAMERA_ANTI_FLICKER,
    CAMERA_FLICKER_PERIOD_US,
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
        self._apply_anti_flicker()
        self.picam2.start()
        time.sleep(CAMERA_WARMUP_SECONDS)

    def _apply_anti_flicker(self):
        if not CAMERA_ANTI_FLICKER:
            return

        required_controls = {"AeFlickerMode", "AeFlickerPeriod"}
        if not required_controls.issubset(self.picam2.camera_controls):
            print("Camera anti-flicker controls are unavailable; continuing without them.")
            return

        try:
            # Manual mode is enum value 1 in libcamera. For 50 Hz mains,
            # a 10,000 us period cancels the resulting 100 Hz light flicker.
            self.picam2.set_controls(
                {
                    "AeFlickerMode": 1,
                    "AeFlickerPeriod": CAMERA_FLICKER_PERIOD_US,
                }
            )
            print(
                "Camera anti-flicker enabled "
                f"({CAMERA_FLICKER_PERIOD_US} us period)."
            )
        except Exception as exc:
            print(f"Could not enable camera anti-flicker: {exc}")

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
