FRAME_WIDTH = 640
FRAME_HEIGHT = 480

CASCADE_FILE = "haarcascade_frontalface_default.xml"

# Keep False until face detection works
USE_SERVOS = False


# Servo limits
PAN_MIN = -90
PAN_MAX = 90

TILT_MIN = 0
TILT_MAX = 180

# Default startup position
DEFAULT_PAN = 0
DEFAULT_TILT = 90

# Tracking tuning
KP_PAN = 0.02
KP_TILT = 0.02

DEAD_ZONE = 30
