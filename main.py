from camera import Camera
from vision import Vision
from controller import Controller
from debug import Debug

import cv2


cam = Camera()
vision = Vision()
controller = Controller()
debug = Debug()


while True:

    ret, frame = cam.read()

    if not ret:
        break

    height, width = frame.shape[:2]

    result = vision.detect(frame)

    cv2.circle(
        frame,
        (width // 2, height // 2),
        5,
        (255, 0, 0),
        -1
    )

    if result:

        x, y, w, h = result["box"]
        cx, cy = result["center"]

        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

        cv2.circle(
            frame,
            (cx, cy),
            5,
            (0, 0, 255),
            -1
        )

        cv2.line(
            frame,
            (width // 2, height // 2),
            (cx, cy),
            (255, 255, 0),
            2
        )

        data = controller.update(
            cx,
            cy,
            width,
            height
        )

        data["tracking"] = "YES"

    else:

        data = {
            "pan": controller.pan,
            "tilt": controller.tilt,
            "error_x": 0,
            "error_y": 0,
            "tracking": "NO"
        }


    debug.show(data)

    cv2.imshow(
        "Face Tracker",
        frame
    )


    if cv2.waitKey(1) == 27:
        break


cam.release()
cv2.destroyAllWindows()
