import cv2

from config import CASCADE_FILE


class Vision:

    def __init__(self):

        self.detector = cv2.CascadeClassifier(
            CASCADE_FILE
        )

        if self.detector.empty():
            print("ERROR: Cascade failed loading")
        else:
            print("Cascade loaded")


    def detect(self, frame):

        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        faces = self.detector.detectMultiScale(
            gray,
            scaleFactor=1.05,
            minNeighbors=3,
            minSize=(40,40)
        )


        if len(faces) == 0:
            return None


        face = max(
            faces,
            key=lambda f: f[2] * f[3]
        )


        x,y,w,h = face


        return {

            "box": (
                x,
                y,
                w,
                h
            ),

            "center": (
                x + w//2,
                y + h//2
            )

        }
