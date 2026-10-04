import math
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


# Smoothly approach each requested angle instead of jumping there immediately.
SERVO_MAX_SPEED = 30.0  # degrees per second
SERVO_RESPONSE = 5.0  # higher values follow the target more aggressively
MAX_UPDATE_SECONDS = 0.1


def clamp(value, minimum, maximum):
    return max(minimum, min(maximum, value))


def approach(current, target, maximum_change):
    return current + clamp(target - current, -maximum_change, maximum_change)


class Servos:
    def __init__(self):
        self.pan = float(DEFAULT_PAN)
        self.tilt = float(DEFAULT_TILT)
        self.target_pan = self.pan
        self.target_tilt = self.tilt
        self.last_written_pan = None
        self.last_written_tilt = None
        self.last_update = time.monotonic()
        self.centre()

    def _write(self, force=False):
        if (
            force
            or self.last_written_pan is None
            or abs(self.pan - self.last_written_pan) >= SERVO_MIN_CHANGE
        ):
            pantilthat.pan(int(round(self.pan)))
            self.last_written_pan = self.pan

        if (
            force
            or self.last_written_tilt is None
            or abs(self.tilt - self.last_written_tilt) >= SERVO_MIN_CHANGE
        ):
            pantilthat.tilt(int(round(self.tilt)))
            self.last_written_tilt = self.tilt

    def move(self, pan, tilt, force=False):
        self.target_pan = clamp(float(pan), PAN_MIN, PAN_MAX)
        self.target_tilt = clamp(float(tilt), TILT_MIN, TILT_MAX)

        if force:
            self.pan = self.target_pan
            self.tilt = self.target_tilt
            self._write(force=True)

    def update(self):
        now = time.monotonic()
        elapsed = clamp(now - self.last_update, 0.0, MAX_UPDATE_SECONDS)
        self.last_update = now

        if elapsed <= 0.0:
            return

        # Exponential easing avoids a hard start, while the speed limit prevents
        # large target changes from snapping the camera across the room.
        easing = 1.0 - math.exp(-SERVO_RESPONSE * elapsed)
        max_change = SERVO_MAX_SPEED * elapsed

        desired_pan = self.pan + (self.target_pan - self.pan) * easing
        desired_tilt = self.tilt + (self.target_tilt - self.tilt) * easing

        self.pan = approach(self.pan, desired_pan, max_change)
        self.tilt = approach(self.tilt, desired_tilt, max_change)
        self._write()

    def centre(self):
        self.move(DEFAULT_PAN, DEFAULT_TILT, force=True)
        self.last_update = time.monotonic()
        time.sleep(SERVO_SETTLE_SECONDS)

    def disable(self):
        try:
            pantilthat.servo_enable(1, False)
            pantilthat.servo_enable(2, False)
        except Exception:
            pass
