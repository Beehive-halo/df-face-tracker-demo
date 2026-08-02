import pantilthat


class Servos:

    def __init__(self):

        self.pan = 0
        self.tilt = 0

        pantilthat.pan(0)
        pantilthat.tilt(0)

    def move(self, pan, tilt):

        self.pan = max(-90, min(90, pan))
        self.tilt = max(-45, min(45, tilt))

        pantilthat.pan(self.pan)
        pantilthat.tilt(self.tilt)

    def centre(self):

        pantilthat.pan(0)
        pantilthat.tilt(0)
