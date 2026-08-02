import pantilthat


class Servos:


    def __init__(self):

        self.centre()



    def move(
        self,
        pan,
        tilt
    ):

        pantilthat.pan(
            int(pan)
        )

        pantilthat.tilt(
            int(tilt)
        )


    def centre(self):

        pantilthat.pan(0)
        pantilthat.tilt(0)
