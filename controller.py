from config import (
    DEAD_ZONE_X,
    DEAD_ZONE_Y,
    DEFAULT_PAN,
    DEFAULT_TILT,
    KP_PAN,
    KP_TILT,
    MAX_STEP,
    PAN_DIRECTION,
    PAN_MAX,
    PAN_MIN,
    SMOOTHING,
    TILT_DIRECTION,
    TILT_MAX,
    TILT_MIN,
)


def clamp(value, minimum, maximum):
    return max(minimum, min(maximum, value))


class Controller:
    def __init__(self):
        self.pan = float(DEFAULT_PAN)
        self.tilt = float(DEFAULT_TILT)
        self.filtered_x = None
        self.filtered_y = None

    def update(self, face_x, face_y, width, height):
        if self.filtered_x is None:
            self.filtered_x = float(face_x)
            self.filtered_y = float(face_y)
        else:
            self.filtered_x += (face_x - self.filtered_x) * SMOOTHING
            self.filtered_y += (face_y - self.filtered_y) * SMOOTHING

        error_x = self.filtered_x - width / 2.0
        error_y = self.filtered_y - height / 2.0

        if abs(error_x) > DEAD_ZONE_X:
            pan_step = clamp(error_x * KP_PAN * PAN_DIRECTION, -MAX_STEP, MAX_STEP)
            self.pan = clamp(self.pan + pan_step, PAN_MIN, PAN_MAX)

        if abs(error_y) > DEAD_ZONE_Y:
            tilt_step = clamp(error_y * KP_TILT * TILT_DIRECTION, -MAX_STEP, MAX_STEP)
            self.tilt = clamp(self.tilt + tilt_step, TILT_MIN, TILT_MAX)

        return {
            "pan": self.pan,
            "tilt": self.tilt,
            "error_x": error_x,
            "error_y": error_y,
        }
