import pantilthat
import time

from config import *


class Servos:

    def __init__(self):

        self.pan = DEFAULT_PAN
        self.tilt = DEFAULT_TILT

        self.home()


    def move(self, pan, tilt):

        self.pan = int(pan)
        self.tilt = int(tilt)

        pantilthat.pan(
            self.pan
        )

        pantilthat.tilt(
            self.tilt
        )


    def home(self):

        print("Moving servos to home position...")

        pantilthat.pan(
            DEFAULT_PAN
        )

        pantilthat.tilt(
            DEFAULT_TILT
        )

        time.sleep(0.5)


    def centre(self):

        self.home()
