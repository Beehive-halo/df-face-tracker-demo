import cv2

# =========================
# Camera
# =========================

USE_PI_CAMERA = True
CAMERA_INDEX = 0

FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# =========================
# Face Detection
# =========================

CASCADE_FILE = "haarcascade_frontalface_default.xml"

# =========================
# Controller
# =========================

KP_PAN = 0.08
KP_TILT = 0.08

DEAD_ZONE = 18

PAN_MIN = -90
PAN_MAX = 90

TILT_MIN = -45
TILT_MAX = 45

# =========================
# Servos
# =========================

USE_SERVOS = True

# =========================
# Display
# =========================

FULLSCREEN = False

# =========================
# Drawing
# =========================

FACE_BOX = (0,255,0)
FACE_CENTER = (0,0,255)
SCREEN_CENTER = (255,255,255)
TRACK_LINE = (255,255,0)
TEXT = (255,255,255)

FONT = cv2.FONT_HERSHEY_SIMPLEX
