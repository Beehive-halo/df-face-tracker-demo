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


print("Tracker started")


try:

    while True:


        ret, frame = camera.read()


        if not ret:

            print("Camera failed")
            break



        result = vision.detect(frame)



        if result:


            cx,cy = result["center"]


            data = controller.update(
                cx,
                cy,
                FRAME_WIDTH,
                FRAME_HEIGHT
            )


            print(
                f"\rFACE FOUND "
                f"Pan:{data['pan']:.1f} "
                f"Tilt:{data['tilt']:.1f}",
                end=""
            )


            if USE_SERVOS:

                servos.move(
                    data["pan"],
                    data["tilt"]
                )


        else:


            print(
                "\rSearching for face...",
                end=""
            )



        time.sleep(0.05)



except KeyboardInterrupt:

    print("\nStopping")


finally:

    servos.centre()

    camera.release()
