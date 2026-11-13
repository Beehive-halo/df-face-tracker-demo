from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Camera / processing: balanced for the Raspberry Pi 3 A+.
FRAME_WIDTH = 400
FRAME_HEIGHT = 300
CAMERA_FPS = 12
CAMERA_WARMUP_SECONDS = 1.0
CAMERA_READ_ATTEMPTS = 3
CAMERA_RETRY_SECONDS = 0.05
OPENCV_THREADS = 3

# Optional 50 Hz lighting compensation. Leave disabled by default because the
# tested camera image produced more reliable face detection without it.
CAMERA_ANTI_FLICKER = False
CAMERA_FLICKER_PERIOD_US = 10000

# The camera is mounted upside down. Both flips together rotate it 180 degrees.
CAMERA_HFLIP = True
CAMERA_VFLIP = True

# Scan periodically, then retain the target while the servo loop moves smoothly.
DETECTION_INTERVAL = 4
TARGET_HOLD_FRAMES = 16

CASCADE_FILE = str(BASE_DIR / "haarcascade_frontalface_default.xml")

# Haar settings tested at roughly one metre on the Pi 3 A+.
DETECTION_SCALE_FACTOR = 1.12
DETECTION_MIN_NEIGHBORS = 4
DETECTION_MIN_SIZE = (28, 28)

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

# Directions verified on the upside-down physical mount.
PAN_DIRECTION = -1
TILT_DIRECTION = 1

# Tracking controller tuned for smooth movement at 400x300.
DEAD_ZONE_X = 24
DEAD_ZONE_Y = 18
KP_PAN = 0.030
KP_TILT = 0.030
MAX_STEP = 1.2
SMOOTHING = 0.20

# Avoid unnecessary I2C writes / servo chatter.
SERVO_MIN_CHANGE = 1.0
SERVO_SETTLE_SECONDS = 0.4
