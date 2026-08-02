from config import *


class Controller:


    def __init__(self):

        self.pan = 0
        self.tilt = 0



    def update(
        self,
        face_x,
        face_y,
        width,
        height
    ):

        error_x = face_x - width//2
        error_y = face_y - height//2


        if abs(error_x) > DEAD_ZONE:

            self.pan -= error_x * KP_PAN


        if abs(error_y) > DEAD_ZONE:

            self.tilt += error_y * KP_TILT


        self.pan = max(
            PAN_MIN,
            min(PAN_MAX,self.pan)
        )


        self.tilt = max(
            TILT_MIN,
            min(TILT_MAX,self.tilt)
        )


        return {

            "pan":self.pan,
            "tilt":self.tilt,
            "error_x":error_x,
            "error_y":error_y

        }
