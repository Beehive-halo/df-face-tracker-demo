import time
import cv2
import os

from camera import Camera
from vision import Vision
from controller import Controller
from servos import Servos

from config import *


camera = Camera()
vision = Vision()
controller = Controller()
servos = Servos()

last_time = time.time()

HAS_DISPLAY = (
    "DISPLAY" in os.environ
    or "WAYLAND_DISPLAY" in os.environ
)

while True:

    ret, frame = camera.read()

    if not ret:
        break

    h, w = frame.shape[:2]

    current = time.time()
    fps = 1 / (current - last_time)
    last_time = current

    cv2.drawMarker(
        frame,
        (w // 2, h // 2),
        SCREEN_CENTER,
        cv2.MARKER_CROSS,
        20,
        2
    )

    result = vision.detect(frame)

    if result:

        x, y, bw, bh = result["box"]
        cx, cy = result["center"]

        cv2.rectangle(
            frame,
            (x, y),
            (x + bw, y + bh),
            FACE_BOX,
            2
        )

        cv2.circle(
            frame,
            (cx, cy),
            5,
            FACE_CENTER,
            -1
        )

        cv2.line(
            frame,
            (w // 2, h // 2),
            (cx, cy),
            TRACK_LINE,
            2
        )

        data = controller.update(
            cx,
            cy,
            w,
            h
        )

        servos.move(
            data["pan"],
            data["tilt"]
        )

        tracking = "YES"

    else:

        data = {
            "pan": controller.pan,
            "tilt": controller.tilt
        }

        tracking = "NO"

    cv2.putText(
        frame,
        f"Tracking: {tracking}",
        (10, 25),
        FONT,
        0.6,
        TEXT,
        2
    )

    cv2.putText(
        frame,
        f"Pan: {data['pan']:.1f}",
        (10, 50),
        FONT,
        0.6,
        TEXT,
        2
    )

    cv2.putText(
        frame,
        f"Tilt: {data['tilt']:.1f}",
        (10, 75),
        FONT,
        0.6,
        TEXT,
        2
    )

    cv2.putText(
        frame,
        f"FPS: {fps:.1f}",
        (10, 100),
        FONT,
        0.6,
        TEXT,
        2
    )

    if FULLSCREEN:

        cv2.namedWindow(
            "Face Tracker",
            cv2.WINDOW_NORMAL
        )

        cv2.setWindowProperty(
            "Face Tracker",
            cv2.WND_PROP_FULLSCREEN,
            cv2.WINDOW_FULLSCREEN
        )

    cv2.imshow(
        "Face Tracker",
        frame
    )

    if cv2.waitKey(1) == 27:
        break


camera.release()
cv2.destroyAllWindows()
