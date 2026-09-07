import time

import pantilthat

from config import (
    DEFAULT_PAN,
    DEFAULT_TILT,
    PAN_MAX,
    PAN_MIN,
    SERVO_MIN_CHANGE,
    SERVO_SETTLE_SECONDS,
    TILT_MAX,
    TILT_MIN,
)


def clamp(value, minimum, maximum):
    return max(minimum, min(maximum, value))


class Servos:
    def __init__(self):
        self.pan = float(DEFAULT_PAN)
        self.tilt = float(DEFAULT_TILT)
        self.last_written_pan = None
        self.last_written_tilt = None
        self.centre()

    def move(self, pan, tilt, force=False):
        pan = clamp(float(pan), PAN_MIN, PAN_MAX)
        tilt = clamp(float(tilt), TILT_MIN, TILT_MAX)

        self.pan = pan
        self.tilt = tilt

        if force or self.last_written_pan is None or abs(pan - self.last_written_pan) >= SERVO_MIN_CHANGE:
            pantilthat.pan(int(round(pan)))
            self.last_written_pan = pan

        if force or self.last_written_tilt is None or abs(tilt - self.last_written_tilt) >= SERVO_MIN_CHANGE:
            pantilthat.tilt(int(round(tilt)))
            self.last_written_tilt = tilt

    def centre(self):
        self.move(DEFAULT_PAN, DEFAULT_TILT, force=True)
        time.sleep(SERVO_SETTLE_SECONDS)

    def disable(self):
        try:
            pantilthat.servo_enable(1, False)
            pantilthat.servo_enable(2, False)
        except Exception:
            pass
