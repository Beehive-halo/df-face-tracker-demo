import cv2

from config import (
    CASCADE_FILE,
    DETECTION_MIN_NEIGHBORS,
    DETECTION_MIN_SIZE,
    DETECTION_SCALE_FACTOR,
)


class Vision:
    def __init__(self):
        self.detector = cv2.CascadeClassifier(CASCADE_FILE)
        if self.detector.empty():
            raise RuntimeError(f"Failed to load Haar cascade: {CASCADE_FILE}")

    def detect(self, frame):
        # Picamera2 RGB888 buffers work with OpenCV's BGR-oriented operations.
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)

        faces = self.detector.detectMultiScale(
            gray,
            scaleFactor=DETECTION_SCALE_FACTOR,
            minNeighbors=DETECTION_MIN_NEIGHBORS,
            minSize=DETECTION_MIN_SIZE,
        )

        if len(faces) == 0:
            return None

        x, y, w, h = max(faces, key=lambda face: face[2] * face[3])
        return {
            "box": (int(x), int(y), int(w), int(h)),
            "center": (int(x + w // 2), int(y + h // 2)),
        }
