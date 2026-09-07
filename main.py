import time

import cv2

from camera import Camera
from config import (
    DETECTION_INTERVAL,
    FRAME_HEIGHT,
    FRAME_WIDTH,
    SHOW_FPS,
    SHOW_PREVIEW,
    TARGET_HOLD_FRAMES,
    USE_SERVOS,
)
from controller import Controller
from vision import Vision


def draw_preview(frame, target, fps):
    if target:
        x, y, w, h = target["box"]
        cx, cy = target["center"]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
        cv2.circle(frame, (cx, cy), 3, (0, 0, 255), -1)

    cv2.circle(frame, (FRAME_WIDTH // 2, FRAME_HEIGHT // 2), 3, (255, 0, 0), -1)

    if SHOW_FPS:
        cv2.putText(
            frame,
            f"FPS {fps:.1f}",
            (8, 18),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.45,
            (255, 255, 255),
            1,
            cv2.LINE_AA,
        )

    cv2.imshow("DF Face Tracker", frame)


def main():
    camera = None
    servos = None

    try:
        camera = Camera()
        vision = Vision()
        controller = Controller()

        if USE_SERVOS:
            from servos import Servos

            servos = Servos()

        print("Tracker started")
        print(f"Resolution: {FRAME_WIDTH}x{FRAME_HEIGHT}")
        print(f"Servo control: {'enabled' if USE_SERVOS else 'disabled'}")

        frame_number = 0
        frames_since_detection = TARGET_HOLD_FRAMES + 1
        target = None

        fps = 0.0
        fps_frames = 0
        fps_started = time.monotonic()

        while True:
            ok, frame = camera.read()
            if not ok:
                break

            frame_number += 1
            fps_frames += 1

            if frame_number % DETECTION_INTERVAL == 0:
                detected = vision.detect(frame)

                if detected is not None:
                    target = detected
                    frames_since_detection = 0

                    cx, cy = target["center"]
                    command = controller.update(cx, cy, FRAME_WIDTH, FRAME_HEIGHT)

                    if servos is not None:
                        servos.move(command["pan"], command["tilt"])
                else:
                    frames_since_detection += DETECTION_INTERVAL
                    if frames_since_detection > TARGET_HOLD_FRAMES:
                        target = None

            now = time.monotonic()
            elapsed = now - fps_started
            if elapsed >= 1.0:
                fps = fps_frames / elapsed
                fps_frames = 0
                fps_started = now

                if SHOW_FPS and not SHOW_PREVIEW:
                    status = "face" if target else "searching"
                    print(f"\r{fps:4.1f} FPS | {status:9s}", end="", flush=True)

            if SHOW_PREVIEW:
                draw_preview(frame, target, fps)
                key = cv2.waitKey(1) & 0xFF
                if key in (27, ord("q")):
                    break

    except KeyboardInterrupt:
        pass
    finally:
        print("\nStopping tracker")

        if servos is not None:
            servos.disable()

        if camera is not None:
            camera.release()

        if SHOW_PREVIEW:
            cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
