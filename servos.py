import cv2
import numpy as np


class Debug:

    def __init__(self):

        self.width = 400
        self.height = 250

    def show(self, data):

        img = np.zeros((self.height, self.width, 3), dtype=np.uint8)

        lines = [
            f"Pan      : {data['pan']:.1f}",
            f"Tilt     : {data['tilt']:.1f}",
            "",
            f"Error X  : {data['error_x']}",
            f"Error Y  : {data['error_y']}",
            "",
            f"Tracking : {data['tracking']}"
        ]

        y = 40

        for line in lines:
            cv2.putText(
                img,
                line,
                (20, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )

            y += 30

        cv2.imshow("Debug", img)
