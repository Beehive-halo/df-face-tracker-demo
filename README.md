# DF Face Tracker Demo

A lightweight face-tracking camera demo designed specifically for a Raspberry Pi 3 A+ using Picamera2, OpenCV Haar detection, and a Pimoroni Pan-Tilt HAT.

## Design goals

- Low CPU use on Raspberry Pi 3 A+
- Low memory overhead
- Simple code that is easy to tune
- Safe optional servo control
- Stable tracking without constant servo chatter
- Optional live browser stream for debugging from another computer

The tracker runs the camera at 320x240 and 15 FPS by default. Haar face detection only runs every few frames, while the most recent target is reused briefly between scans. This avoids doing the most expensive OpenCV operation on every frame.

## Hardware

- Raspberry Pi 3 A+
- Raspberry Pi camera supported by Picamera2
- Pimoroni Pan-Tilt HAT / compatible pan-tilt hardware
- Adequate Raspberry Pi power supply
- A Mac or other device on the same network if you want the live stream

Servos can cause voltage drops. Fix any Raspberry Pi undervoltage warnings before enabling servo tracking.

## Install

Update Raspberry Pi OS first:

```bash
sudo apt update
sudo apt upgrade
```

Install Picamera2 and OpenCV from Raspberry Pi OS packages:

```bash
sudo apt install python3-picamera2 python3-opencv
```

Install the Pan-Tilt Python library if you are using the servos:

```bash
python3 -m pip install pantilthat
```

If your Raspberry Pi OS Python environment blocks system-wide pip installs, use the package/install method recommended for your Pan-Tilt HAT version instead.

## First test: camera only

Leave this in `config.py`:

```python
USE_SERVOS = False
```

Run:

```bash
python3 main.py
```

The default configuration is headless for lower CPU use. You do not need a monitor connected to the Pi.

Set:

```python
SHOW_PREVIEW = True
```

only if you want a local OpenCV debug window on the Pi itself.

## Watch the camera from your Mac

Browser streaming is enabled by default:

```python
ENABLE_STREAM = True
STREAM_PORT = 8000
STREAM_FPS = 5
STREAM_JPEG_QUALITY = 65
STREAM_SHOW_OVERLAY = True
```

Start the tracker on the Pi:

```bash
python3 main.py
```

At startup it prints an address similar to:

```text
Mac/browser stream: http://raspberrypi.local:8000/
```

Open that address in Safari, Chrome, or Firefox on your Mac.

If the `.local` hostname does not work, run this on the Pi:

```bash
hostname -I
```

For example, if it prints `192.168.1.42`, open:

```text
http://192.168.1.42:8000/
```

The Pi and Mac need to be reachable on the same local network.

The browser view can show:

- the live camera frame
- the detected face box
- the target centre
- `TRACKING` / `SEARCHING` state
- tracker FPS
- current pan and tilt command
- number of connected viewers

### Why the stream is only 5 FPS

The tracker itself still captures at 15 FPS. The browser stream is deliberately limited to 5 FPS because creating JPEG images costs CPU time. Face detection and servo tracking remain the priority on a Raspberry Pi 3 A+.

The stream also avoids JPEG encoding completely when nobody is watching it, so leaving `ENABLE_STREAM = True` has very little extra CPU cost until a browser connects.

To reduce streaming load further:

```python
STREAM_FPS = 3
STREAM_JPEG_QUALITY = 55
```

To make it smoother at the cost of more Pi CPU and Wi-Fi bandwidth:

```python
STREAM_FPS = 8
STREAM_JPEG_QUALITY = 70
```

The stream has no login or encryption and is intended for a trusted local network. Do not expose port 8000 directly to the internet.

## Power diagnostics

Run:

```bash
python3 diagnostics.py
```

or directly:

```bash
vcgencmd get_throttled
```

`throttled=0x0` means no current or recorded throttling flags were detected.

## Servo test

Before enabling automatic tracking, test the mount:

```bash
python3 servo_test.py
```

The project uses the Pimoroni angle convention:

- centre: `0`
- negative direction: down/left depending on mount orientation
- positive direction: up/right depending on mount orientation
- native range: roughly `-90` to `90`

The default software limits are intentionally smaller to reduce the chance of the bracket binding mechanically.

## Enable tracking

When camera detection and power are stable, change:

```python
USE_SERVOS = True
```

If an axis moves in the wrong direction, change its direction value in `config.py`:

```python
PAN_DIRECTION = -1
TILT_DIRECTION = 1
```

Swap either `1` and `-1` as required by your physical mount.

## Performance tuning

Important values in `config.py`:

- `FRAME_WIDTH` / `FRAME_HEIGHT`: processing resolution
- `CAMERA_FPS`: camera frame-rate cap
- `DETECTION_INTERVAL`: how often Haar detection runs
- `TARGET_HOLD_FRAMES`: how long the last detected target is kept
- `SHOW_PREVIEW`: local Pi preview; disable for best performance
- `ENABLE_STREAM`: enable the Mac/browser streaming server
- `STREAM_FPS`: maximum browser stream frame rate
- `STREAM_JPEG_QUALITY`: browser stream JPEG quality
- `KP_PAN` / `KP_TILT`: tracking response speed
- `SMOOTHING`: target position filtering
- `SERVO_MIN_CHANGE`: minimum command change before another servo write

For the Raspberry Pi 3 A+, the defaults are intentionally conservative.

## Project structure

```text
main.py          main tracking loop and stream publishing
camera.py        Picamera2 capture
vision.py        Haar face detection
controller.py    smoothing and pan/tilt control
servos.py        Pan-Tilt HAT output
stream.py        lightweight MJPEG HTTP server
config.py        tuning and hardware settings
servo_test.py    manual servo movement test
diagnostics.py   Raspberry Pi power/throttling check
```

## How the browser stream works

`main.py` keeps doing the normal camera and face-detection loop. When a browser connects, `stream.py` runs a small HTTP server in a background thread.

At the configured stream rate, `main.py` makes a copy of the current camera frame, draws the debug information on that copy, compresses it as JPEG, and gives it to the HTTP server. The server sends one JPEG after another using an MJPEG response. A normal browser can display that response as continuously updating video.

The important part for the Pi 3 A+ is that the web server does not capture its own second camera feed and it does not run face detection again. It reuses the tracker's current frame and current detection result.

## Notes

The Haar cascade XML is included in the repository so the demo can run without downloading a model at startup.
