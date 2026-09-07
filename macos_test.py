import argparse
import sys
import time
import webbrowser

import cv2

from config import (
    CASCADE_FILE,
    DETECTION_INTERVAL,
    DETECTION_MIN_NEIGHBORS,
    DETECTION_MIN_SIZE,
    DETECTION_SCALE_FACTOR,
    FRAME_HEIGHT,
    FRAME_WIDTH,
    SHOW_FPS,
    STREAM_JPEG_QUALITY,
)
from stream import StreamServer


def parse_args():
    parser = argparse.ArgumentParser(
        description="macOS webcam test for the DF face tracker."
    )
    parser.add_argument(
        "--camera",
        type=int,
        default=0,
        help="macOS camera index (default: 0).",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Browser stream port (default: 8000).",
    )
    parser.add_argument(
        "--no-window",
        action="store_true",
        help="Disable the local OpenCV preview window.",
    )
    parser.add_argument(
        "--no-stream",
        action="store_true",
        help="Disable the browser MJPEG stream.",
    )
    parser.add_argument(
        "--open-browser",
        action="store_true",
        help="Open the local stream page automatically.",
    )
    return parser.parse_args()


def draw_overlay(frame, target, fps, viewers):
    if target is not None:
        x, y, w, h = target["box"]
        cx, cy = target["center"]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
        cv2.circle(frame, (cx, cy), 3, (0, 0, 255), -1)
        status = "TRACKING"
    else:
        status = "SEARCHING"

    cv2.circle(
        frame,
        (FRAME_WIDTH // 2, FRAME_HEIGHT // 2),
        3,
        (255, 0, 0),
        -1,
    )

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
        f"macOS TEST | viewers {viewers}",
        (8, FRAME_HEIGHT - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.35,
        (255, 255, 255),
        1,
        cv2.LINE_AA,
    )

    return frame


def main():
    args = parse_args()

    detector = cv2.CascadeClassifier(CASCADE_FILE)
    if detector.empty():
        raise RuntimeError(f"Could not load Haar cascade: {CASCADE_FILE}")

    capture = cv2.VideoCapture(args.camera, cv2.CAP_AVFOUNDATION)
    if not capture.isOpened():
        capture.release()
        capture = cv2.VideoCapture(args.camera)

    if not capture.isOpened():
        print(
            "Could not open the Mac camera.\n"
            "Check System Settings > Privacy & Security > Camera and allow "
            "your terminal/IDE to use the camera.",
            file=sys.stderr,
        )
        return 1

    capture.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
    capture.set(cv2.CAP_PROP_FPS, 15)
    capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    streamer = None
    if not args.no_stream:
        streamer = StreamServer("0.0.0.0", args.port)
        streamer.start()
        url = f"http://127.0.0.1:{args.port}/"
        print(f"Browser stream: {url}")
        if args.open_browser:
            webbrowser.open(url)

    print("macOS test started")
    print(f"Camera index: {args.camera}")
    print(f"Processing resolution: {FRAME_WIDTH}x{FRAME_HEIGHT}")
    print("Press Q or Escape in the preview window to quit.")

    frame_number = 0
    target = None
    fps = 0.0
    fps_frames = 0
    fps_started = time.monotonic()

    try:
        while True:
            ok, frame = capture.read()
            if not ok:
                print("Camera frame capture failed.", file=sys.stderr)
                break

            if frame.shape[1] != FRAME_WIDTH or frame.shape[0] != FRAME_HEIGHT:
                frame = cv2.resize(
                    frame,
                    (FRAME_WIDTH, FRAME_HEIGHT),
                    interpolation=cv2.INTER_AREA,
                )

            frame_number += 1
            fps_frames += 1

            if frame_number % DETECTION_INTERVAL == 0:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(
                    gray,
                    scaleFactor=DETECTION_SCALE_FACTOR,
                    minNeighbors=DETECTION_MIN_NEIGHBORS,
                    minSize=DETECTION_MIN_SIZE,
                )

                if len(faces):
                    x, y, w, h = max(faces, key=lambda face: face[2] * face[3])
                    target = {
                        "box": (int(x), int(y), int(w), int(h)),
                        "center": (int(x + w // 2), int(y + h // 2)),
                    }
                else:
                    target = None

            now = time.monotonic()
            elapsed = now - fps_started
            if elapsed >= 1.0:
                fps = fps_frames / elapsed
                fps_frames = 0
                fps_started = now

            viewers = streamer.client_count if streamer is not None else 0
            output = draw_overlay(frame.copy(), target, fps, viewers)

            if streamer is not None and streamer.has_clients:
                encoded, jpeg = cv2.imencode(
                    ".jpg",
                    output,
                    [cv2.IMWRITE_JPEG_QUALITY, STREAM_JPEG_QUALITY],
                )
                if encoded:
                    streamer.publish(jpeg.tobytes())

            if not args.no_window:
                cv2.imshow("DF Face Tracker - macOS Test", output)
                key = cv2.waitKey(1) & 0xFF
                if key in (27, ord("q")):
                    break

            if args.no_window and args.no_stream:
                time.sleep(0.01)

    except KeyboardInterrupt:
        pass
    finally:
        print("\nStopping macOS test")
        if streamer is not None:
            streamer.stop()
        capture.release()
        cv2.destroyAllWindows()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
