from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Camera / processing
FRAME_WIDTH = 320
FRAME_HEIGHT = 240
CAMERA_FPS = 15
CAMERA_WARMUP_SECONDS = 1.0

# The camera is mounted upside down. Both flips together rotate it 180 degrees.
CAMERA_HFLIP = True
CAMERA_VFLIP = True

# Run the expensive Haar scan only every N frames.
DETECTION_INTERVAL = 3
TARGET_HOLD_FRAMES = 6

CASCADE_FILE = str(BASE_DIR / "haarcascade_frontalface_default.xml")

# Haar settings tuned for a low-resolution Pi 3 A+ stream.
DETECTION_SCALE_FACTOR = 1.12
DETECTION_MIN_NEIGHBORS = 5
DETECTION_MIN_SIZE = (32, 32)

# Optional local debug window. Disable for best performance/headless use.
SHOW_PREVIEW = False
SHOW_FPS = True

# Browser stream for another device on the same local network.
# Open the URL printed by main.py on your Mac.
ENABLE_STREAM = True
STREAM_HOST = "0.0.0.0"
STREAM_PORT = 8000
STREAM_FPS = 5
STREAM_JPEG_QUALITY = 65
STREAM_SHOW_OVERLAY = True

# Keep disabled until camera detection and servo power are confirmed stable.
USE_SERVOS = False

# Pimoroni Pan-Tilt HAT uses -90..90 with 0 as centre.
PAN_MIN = -80
PAN_MAX = 80
TILT_MIN = -70
TILT_MAX = 70
DEFAULT_PAN = 0
DEFAULT_TILT = 0

# Compensates tracking for the camera's 180-degree image rotation.
# Reverse either value if your physical mount still moves the wrong direction.
PAN_DIRECTION = 1
TILT_DIRECTION = -1

# Tracking controller.
DEAD_ZONE_X = 16
DEAD_ZONE_Y = 12
KP_PAN = 0.045
KP_TILT = 0.045
MAX_STEP = 3.0
SMOOTHING = 0.35

# Avoid unnecessary I2C writes / servo chatter.
SERVO_MIN_CHANGE = 1.0
SERVO_SETTLE_SECONDS = 0.4
