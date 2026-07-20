from config import *

import pantilthat


class Servos:

    def __init__(self):

        self.pan = 0
        self.tilt = 0

        pantilthat.pan(0)
        pantilthat.tilt(0)

    def move(self, target_pan, target_tilt):

        self.pan += (target_pan - self.pan) * 0.25
        self.tilt += (target_tilt - self.tilt) * 0.25

        pantilthat.pan(self.pan)
        pantilthat.tilt(self.tilt)

    def centre(self):

        self.pan = 0
        self.tilt = 0

        pantilthat.pan(0)
        pantilthat.tilt(0)
