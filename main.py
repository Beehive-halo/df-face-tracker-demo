import os
import time
import cv2

from camera import Camera
from vision import Vision
from controller import Controller
from servos import Servos
from config import *

camera = Camera()
vision = Vision()
controller = Controller()
servos = Servos()

HAS_DISPLAY = (
    os.environ.get("DISPLAY") is not None or
    os.environ.get("WAYLAND_DISPLAY") is not None
)

if HAS_DISPLAY:

    cv2.namedWindow(
        "Face Tracker",
        cv2.WINDOW_NORMAL
    )

    if FULLSCREEN:
        cv2.setWindowProperty(
            "Face Tracker",
            cv2.WND_PROP_FULLSCREEN,
            cv2.WINDOW_FULLSCREEN
        )

last_time = time.time()

try:

    while True:

        ret, frame = camera.read()

        if not ret:
            print("Camera read failed.")
            break

        h, w = frame.shape[:2]

        now = time.time()
        fps = 1 / (now - last_time)
        last_time = now

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

            cv2.drawMarker(
                frame,
                (w // 2, h // 2),
                SCREEN_CENTER,
                cv2.MARKER_CROSS,
                20,
                2
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

            if USE_SERVOS:
                servos.move(
                    data["pan"],
                    data["tilt"]
                )

            tracking = "YES"

        else:

            tracking = "NO"

            data = {
                "pan": controller.pan,
                "tilt": controller.tilt
            }

            cv2.drawMarker(
                frame,
                (w // 2, h // 2),
                SCREEN_CENTER,
                cv2.MARKER_CROSS,
                20,
                2
            )

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

        if HAS_DISPLAY:

            cv2.imshow(
                "Face Tracker",
                frame
            )

            key = cv2.waitKey(1) & 0xFF

            if key == 27:
                break

        else:

            # Headless mode - no display
            time.sleep(0.01)

except KeyboardInterrupt:
    print("\nStopping...")

finally:

    servos.centre()
    camera.release()

    if HAS_DISPLAY:
        cv2.destroyAllWindows()
