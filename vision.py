import cv2

from config import CASCADE_FILE


class Vision:

    def __init__(self):

        self.detector = cv2.CascadeClassifier(CASCADE_FILE)

    def detect(self, frame):

        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        faces = self.detector.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(60, 60)
        )

        if len(faces) == 0:
            return None

        x, y, w, h = max(
            faces,
            key=lambda face: face[2] * face[3]
        )

        return {
            "box": (x, y, w, h),
            "center": (
                x + w // 2,
                y + h // 2
            )
        }
