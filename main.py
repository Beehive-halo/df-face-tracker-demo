import time

import cv2

from camera import Camera
from config import (
    DETECTION_INTERVAL,
    ENABLE_STREAM,
    FRAME_HEIGHT,
    FRAME_WIDTH,
    OPENCV_THREADS,
    SHOW_FPS,
    SHOW_PREVIEW,
    STREAM_FPS,
    STREAM_HOST,
    STREAM_JPEG_QUALITY,
    STREAM_PORT,
    STREAM_SHOW_OVERLAY,
    TARGET_HOLD_FRAMES,
    USE_SERVOS,
)
from controller import Controller
from vision import Vision


def draw_overlay(frame, target, fps, command, stream_clients=None):
    if target:
        x, y, w, h = target["box"]
        cx, cy = target["center"]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
        cv2.circle(frame, (cx, cy), 3, (0, 0, 255), -1)
        status = "TRACKING"
    else:
        status = "SEARCHING"

    cv2.circle(frame, (FRAME_WIDTH // 2, FRAME_HEIGHT // 2), 3, (255, 0, 0), -1)

    cv2.putText(
        frame,
        status,
        (8, 18),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.45,
        (255, 255, 255),
        1,
        cv2.LINE_AA,
    )

    if SHOW_FPS:
        cv2.putText(
            frame,
            f"FPS {fps:.1f}",
            (8, 36),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.4,
            (255, 255, 255),
            1,
            cv2.LINE_AA,
        )

    cv2.putText(
        frame,
        f"Pan {command['pan']:.1f}  Tilt {command['tilt']:.1f}",
        (8, FRAME_HEIGHT - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.4,
        (255, 255, 255),
        1,
        cv2.LINE_AA,
    )

    if stream_clients is not None:
        cv2.putText(
            frame,
            f"Viewers {stream_clients}",
            (FRAME_WIDTH - 82, 18),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.35,
            (255, 255, 255),
            1,
            cv2.LINE_AA,
        )

    return frame


def main():
    camera = None
    servos = None
    streamer = None

    try:
        cv2.setUseOptimized(True)
        cv2.setNumThreads(OPENCV_THREADS)

        camera = Camera()
        vision = Vision()
        controller = Controller()

        if USE_SERVOS:
            from servos import Servos

            servos = Servos()

        if ENABLE_STREAM:
            from stream import StreamServer

            streamer = StreamServer(STREAM_HOST, STREAM_PORT)
            streamer.start()

        print("Tracker started")
        print(f"Resolution: {FRAME_WIDTH}x{FRAME_HEIGHT}")
        print(f"Servo control: {'enabled' if USE_SERVOS else 'disabled'}")

        if streamer is not None:
            print(f"Mac/browser stream: {streamer.display_url()}")
            print("If that name does not resolve, run 'hostname -I' on the Pi and use its IP address.")

        frame_number = 0
        frames_since_detection = TARGET_HOLD_FRAMES + 1
        target = None

        latest_command = {
            "pan": controller.pan,
            "tilt": controller.tilt,
        }

        fps = 0.0
        fps_frames = 0
        fps_started = time.monotonic()
        next_stream_frame = 0.0
        stream_period = 1.0 / max(1, STREAM_FPS)

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
                    latest_command = controller.update(cx, cy, FRAME_WIDTH, FRAME_HEIGHT)

                    if servos is not None:
                        servos.move(latest_command["pan"], latest_command["tilt"])
                else:
                    frames_since_detection += DETECTION_INTERVAL
                    if frames_since_detection > TARGET_HOLD_FRAMES:
                        if target is not None:
                            controller.reset_target()
                        target = None

            now = time.monotonic()
            elapsed = now - fps_started
            if elapsed >= 1.0:
                fps = fps_frames / elapsed
                fps_frames = 0
                fps_started = now

                if SHOW_FPS and not SHOW_PREVIEW:
                    status = "face" if target else "searching"
                    viewers = streamer.client_count if streamer is not None else 0
                    print(
                        f"\r{fps:4.1f} FPS | {status:9s} | viewers {viewers}",
                        end="",
                        flush=True,
                    )

            if streamer is not None and streamer.has_clients and now >= next_stream_frame:
                stream_frame = frame.copy()

                if STREAM_SHOW_OVERLAY:
                    draw_overlay(
                        stream_frame,
                        target,
                        fps,
                        latest_command,
                        stream_clients=streamer.client_count,
                    )

                encoded, jpeg = cv2.imencode(
                    ".jpg",
                    stream_frame,
                    [cv2.IMWRITE_JPEG_QUALITY, STREAM_JPEG_QUALITY],
                )

                if encoded:
                    streamer.publish(jpeg.tobytes())

                next_stream_frame = now + stream_period

            if SHOW_PREVIEW:
                preview_frame = draw_overlay(
                    frame.copy(),
                    target,
                    fps,
                    latest_command,
                )
                cv2.imshow("DF Face Tracker", preview_frame)
                key = cv2.waitKey(1) & 0xFF
                if key in (27, ord("q")):
                    break

    except KeyboardInterrupt:
        pass
    finally:
        print("\nStopping tracker")

        if streamer is not None:
            streamer.stop()

        if servos is not None:
            servos.disable()

        if camera is not None:
            camera.release()

        if SHOW_PREVIEW:
            cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
