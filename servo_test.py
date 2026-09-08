import time

import pantilthat


def move(pan, tilt, delay=1.0):
    print(f"Pan {pan:>4} | Tilt {tilt:>4}")
    pantilthat.pan(pan)
    pantilthat.tilt(tilt)
    time.sleep(delay)


try:
    move(0, 0)
    move(30, 0)
    move(-30, 0)
    move(0, 0)
    move(0, 20)
    move(0, -20)
    move(0, 0)
finally:
    pantilthat.servo_enable(1, False)
    pantilthat.servo_enable(2, False)
    print("Servo test finished")
