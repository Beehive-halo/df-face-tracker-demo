from camera import Camera
from vision import Vision
from controller import Controller
from servos import Servos
from config import *

import time


camera = Camera()
vision = Vision()
controller = Controller()
servos = Servos()

print("Face tracker started.")
print("Press Ctrl+C to quit.")

try:

    while True:

        ret, frame = camera.read()

        if not ret:
            print("Camera error.")
            break

        result = vision.detect(frame)

        if result:

            cx, cy = result["center"]

            data = controller.update(
                cx,
                cy,
                FRAME_WIDTH,
                FRAME_HEIGHT
            )

            if USE_SERVOS:
                servos.move(
                    data["pan"],
                    data["tilt"]
                )

            print(
                f"\rTracking | "
                f"Pan {data['pan']:.1f}°  "
                f"Tilt {data['tilt']:.1f}°",
                end=""
            )

        else:

            print("\rSearching for face...", end="")

        time.sleep(0.02)

except KeyboardInterrupt:

    print("\nStopping...")

finally:

    servos.centre()
    camera.release()
